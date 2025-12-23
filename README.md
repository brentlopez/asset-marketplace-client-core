# Asset Marketplace Client Core

Platform-agnostic Python library providing base abstractions for asset marketplace API clients.

## Overview

This library provides foundational abstract base classes (ABCs) and data models for building asset marketplace clients. It defines a common interface that can be extended for specific platforms like Fab.com, Unity Asset Store, Unreal Engine Marketplace, or any other asset marketplace.

**Key Features:**
- 🎯 Platform-agnostic abstractions
- 📦 Zero runtime dependencies (stdlib only)
- 🔒 Fully typed (mypy strict mode)
- 🐍 Python 3.7+ support
- 🔄 Context manager support
- 📊 Progress callback system
- 🧩 Extensible design

## Installation

```bash
pip install asset-marketplace-client-core
```

For development:
```bash
pip install asset-marketplace-client-core[dev]
```

## Quick Start

### Extending the Base Classes

```python
from dataclasses import dataclass
from asset_marketplace_core import (
    MarketplaceClient,
    AuthProvider,
    EndpointConfig,
    BaseAsset,
    BaseCollection,
    DownloadResult,
)

# 1. Define your platform-specific endpoints
@dataclass
class MyPlatformEndpoints(EndpointConfig):
    """Platform-specific API endpoints."""
    library_url: str
    asset_url: str
    download_url: str

# 2. Implement authentication
class MyPlatformAuth(AuthProvider):
    """Platform-specific authentication."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_session(self):
        # Return your HTTP client (e.g., requests.Session)
        import requests
        session = requests.Session()
        session.headers['Authorization'] = f'Bearer {self.api_key}'
        return session
    
    def get_endpoints(self) -> MyPlatformEndpoints:
        return MyPlatformEndpoints(
            base_url="https://api.example.com",
            library_url="https://api.example.com/library",
            asset_url="https://api.example.com/assets",
            download_url="https://cdn.example.com/downloads"
        )

# 3. Implement the client
class MyPlatformClient(MarketplaceClient):
    """Platform-specific marketplace client."""
    
    def __init__(self, auth: MyPlatformAuth):
        self.auth = auth
        self.session = auth.get_session()
        self.endpoints = auth.get_endpoints()
    
    def get_collection(self, **kwargs) -> BaseCollection:
        """Fetch user's asset library."""
        response = self.session.get(self.endpoints.library_url, params=kwargs)
        response.raise_for_status()
        
        data = response.json()
        assets = [
            BaseAsset(
                uid=item['id'],
                title=item['name'],
                description=item.get('description'),
                raw_data=item
            )
            for item in data['assets']
        ]
        
        return BaseCollection(assets=assets, total_count=data['total'])
    
    def get_asset(self, asset_uid: str) -> BaseAsset:
        """Fetch specific asset details."""
        url = f"{self.endpoints.asset_url}/{asset_uid}"
        response = self.session.get(url)
        response.raise_for_status()
        
        data = response.json()
        return BaseAsset(
            uid=data['id'],
            title=data['name'],
            description=data.get('description'),
            raw_data=data
        )
    
    def download_asset(self, asset_uid, output_dir, progress_callback=None, **kwargs):
        """Download asset files."""
        # Implementation details...
        return DownloadResult(
            success=True,
            asset_uid=asset_uid,
            files=[f"{output_dir}/asset.zip"]
        )
    
    def close(self):
        """Clean up resources."""
        if hasattr(self, 'session'):
            self.session.close()

# 4. Use your client
with MyPlatformClient(MyPlatformAuth("your-api-key")) as client:
    collection = client.get_collection(limit=10)
    for asset in collection.assets:
        print(f"{asset.title} ({asset.uid})")
```

## Core Components

### MarketplaceClient

Abstract base class for marketplace clients.

**Methods:**
- `get_collection(**kwargs) -> BaseCollection` - Retrieve asset collections
- `get_asset(asset_uid: str) -> BaseAsset` - Retrieve specific asset
- `download_asset(asset_uid, output_dir, progress_callback, **kwargs) -> DownloadResult` - Download asset files
- `close()` - Clean up resources

### AuthProvider

Abstract base class for authentication providers.

**Methods:**
- `get_session() -> Any` - Return configured HTTP client
- `get_endpoints() -> EndpointConfig` - Return API endpoint configuration
- `refresh()` - Optional: refresh credentials
- `close()` - Optional: cleanup

### Data Models

**BaseAsset:**
```python
@dataclass
class BaseAsset:
    uid: str
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)
```

**BaseCollection:**
```python
@dataclass
class BaseCollection:
    assets: List[BaseAsset] = field(default_factory=list)
    total_count: Optional[int] = None
    
    def filter(self, predicate: Callable[[BaseAsset], bool]) -> BaseCollection
    def find_by_uid(self, uid: str) -> Optional[BaseAsset]
```

**DownloadResult:**
```python
@dataclass
class DownloadResult:
    success: bool
    asset_uid: str
    files: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### Progress Callbacks

Implement `ProgressCallback` for custom progress reporting:

```python
from asset_marketplace_core import ProgressCallback

class ConsoleProgress(ProgressCallback):
    def on_start(self, total: Optional[int]) -> None:
        print(f"Starting download ({total} bytes)")
    
    def on_progress(self, current: int, total: Optional[int]) -> None:
        if total:
            percent = (current / total) * 100
            print(f"Progress: {percent:.1f}%")
    
    def on_complete(self) -> None:
        print("Download complete!")
    
    def on_error(self, error: Exception) -> None:
        print(f"Error: {error}")

# Use with download
result = client.download_asset(
    "asset-123",
    "./downloads",
    progress_callback=ConsoleProgress()
)
```

### Utility Functions

```python
from asset_marketplace_core import (
    sanitize_filename,
    validate_url,
    safe_create_directory,
    format_bytes,
)

# Sanitize filenames for cross-platform compatibility
safe_name = sanitize_filename("My Asset: Version 2.0")  # "My Asset Version 2.0"

# Validate URLs
is_valid = validate_url("https://api.example.com")  # True

# Safely create directories
safe_create_directory("./downloads/assets")

# Format byte counts
size = format_bytes(1048576)  # "1.00 MB"
```

### Exception Hierarchy

```python
from asset_marketplace_core import (
    MarketplaceError,                 # Base exception
    MarketplaceAuthenticationError,   # Auth failures
    MarketplaceAPIError,              # API errors
    MarketplaceNotFoundError,         # Resource not found
    MarketplaceNetworkError,          # Network issues
    MarketplaceValidationError,       # Input validation
)

try:
    asset = client.get_asset("invalid-id")
except MarketplaceNotFoundError:
    print("Asset not found")
except MarketplaceError as e:
    print(f"Marketplace error: {e}")
```

## Extending for Your Platform

### Platform-Specific Assets

```python
@dataclass
class MyPlatformAsset(BaseAsset):
    """Extend BaseAsset with platform-specific fields."""
    category: Optional[str] = None
    publisher: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    
    def is_free(self) -> bool:
        return self.price == 0.0
```

### Platform-Specific Collections

```python
@dataclass
class MyPlatformCollection(BaseCollection):
    """Extend BaseCollection with platform-specific methods."""
    
    def filter_by_category(self, category: str) -> 'MyPlatformCollection':
        filtered = [a for a in self.assets if getattr(a, 'category', None) == category]
        return MyPlatformCollection(assets=filtered, total_count=len(filtered))
    
    def sort_by_price(self, reverse: bool = False) -> 'MyPlatformCollection':
        sorted_assets = sorted(
            self.assets,
            key=lambda a: getattr(a, 'price', 0),
            reverse=reverse
        )
        return MyPlatformCollection(assets=sorted_assets, total_count=self.total_count)
```

## Design Philosophy

### Why Abstract?

This library intentionally provides only abstractions. Each marketplace has unique:
- Authentication mechanisms (API keys, OAuth, cookies, etc.)
- API structures and endpoints
- Data formats and field names
- Download protocols

By providing a common interface, platform-specific implementations can focus on their unique logic while maintaining consistency.

### Why No Dependencies?

Zero runtime dependencies means:
- ✅ No version conflicts
- ✅ Minimal install size
- ✅ Works with any HTTP library (requests, httpx, aiohttp)
- ✅ Easy to integrate into existing projects

Platform implementations choose their own dependencies.

## Example Implementations

While this core library is abstract, you can build complete platform clients:

```python
# Example structure for a platform client package
my-marketplace-client/
├── my_marketplace_client/
│   ├── __init__.py
│   ├── client.py         # Extends MarketplaceClient
│   ├── auth.py           # Extends AuthProvider
│   ├── models.py         # Extends BaseAsset, BaseCollection
│   └── endpoints.py      # Extends EndpointConfig
├── setup.py
└── requirements.txt      # Include: asset-marketplace-client-core, requests
```

## Documentation

### Core Documentation
- [Platform Client Development Guide](./docs/platform_client_guide.md) - Complete guide to building platform clients
- [Async API Plan](./docs/async_api_plan.md) - Future async/await support roadmap

### Architecture
For a deeper understanding of the system architecture and design patterns, see the related [asset-marketplace-client-system](https://github.com/brentlopez/asset-marketplace-client-system) repository.

## Development

### Setup

```bash
git clone https://github.com/brentlopez/asset-marketplace-client-core
cd asset-marketplace-client-core
pip install -e ".[dev]"
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
black src/
ruff check src/
```

### Testing

```bash
pytest
```

## Contributing

Contributions are welcome! Please:

1. Ensure all type hints are correct (mypy strict mode)
2. Add tests for new functionality
3. Update documentation
4. Follow existing code style (black, ruff)

## License

MIT License - see LICENSE file for details.

## Related Projects

This core library enables platform-specific implementations. Look for packages like:
- `fab-api-client` - Fab.com marketplace client
- `unity-asset-store-client` - Unity Asset Store client
- Or build your own!

## Support

- **Issues:** [GitHub Issues](https://github.com/brentlopez/asset-marketplace-client-core/issues)
- **Discussions:** [GitHub Discussions](https://github.com/brentlopez/asset-marketplace-client-core/discussions)

---

Built with ♥️ for the asset marketplace community
