# Platform Client Development Guide

This guide explains how to build a platform-specific marketplace client using `asset-marketplace-client-core`.

## Overview

A platform client extends the core abstractions to provide concrete implementations for a specific marketplace (e.g., Fab.com, Unity Asset Store, Unreal Marketplace, etc.). This guide covers the complete development process.

## Quick Start Checklist

- [ ] Install core library: `pip install asset-marketplace-client-core`
- [ ] Create package structure with `src/` layout
- [ ] Implement `MarketplaceClient` ABC
- [ ] Define platform-specific `AuthProvider` subclass
- [ ] Create domain models extending `BaseAsset` and `BaseCollection`
- [ ] Define platform-specific exception types
- [ ] Add API response models
- [ ] Write comprehensive tests
- [ ] Create documentation
- [ ] Set up packaging (pyproject.toml)

## Project Structure

```
my-marketplace-client/
├── pyproject.toml               # Package configuration
├── README.md                    # User documentation
├── LICENSE                      # MIT or other open-source license
├── CHANGELOG.md                 # Version history
├── .gitignore
│
├── src/
│   └── my_marketplace_client/
│       ├── __init__.py          # Public API exports
│       ├── client.py            # Main client (extends MarketplaceClient)
│       ├── auth.py              # Auth provider implementations
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── domain/          # Business/domain models
│       │   │   ├── __init__.py
│       │   │   ├── asset.py     # Platform-specific asset
│       │   │   └── collection.py # Platform-specific collection
│       │   │
│       │   └── api/             # API response types
│       │       ├── __init__.py
│       │       ├── responses.py  # API response models
│       │       └── converters.py # Response → Domain converters
│       │
│       ├── exceptions.py        # Platform-specific exceptions
│       └── utils.py             # Utility functions (optional)
│
└── tests/
    ├── __init__.py
    ├── test_client.py
    ├── test_auth.py
    ├── test_models.py
    └── fixtures/                # Test fixtures
        └── api_responses.json   # Mock API responses
```

## Step 1: Define Your Endpoints

Extend `EndpointConfig` with your platform's API endpoints:

```python
# my_marketplace_client/auth.py
from dataclasses import dataclass
from asset_marketplace_core import EndpointConfig

@dataclass
class MyMarketplaceEndpoints(EndpointConfig):
    """API endpoints for My Marketplace."""
    # Inherit base_url from EndpointConfig
    
    # Add platform-specific endpoints
    library_url: str
    asset_details_url: str
    download_url: str
    
    # Optional: Add helper methods
    def get_asset_url(self, asset_id: str) -> str:
        return f"{self.asset_details_url}/{asset_id}"
```

## Step 2: Implement Auth Provider

Create an auth provider that implements how to authenticate with your platform:

```python
# my_marketplace_client/auth.py
from asset_marketplace_core import AuthProvider
import requests
from typing import Optional

class MyMarketplaceAuth(AuthProvider):
    """
    Authentication provider for My Marketplace.
    
    This example uses API key authentication. Adapt to your platform's
    authentication method (OAuth, cookies, JWT, etc.).
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.example.com"):
        self.api_key = api_key
        self.base_url = base_url
    
    def get_session(self) -> requests.Session:
        """Create authenticated session."""
        session = requests.Session()
        session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
        })
        return session
    
    def get_endpoints(self) -> MyMarketplaceEndpoints:
        """Return API endpoints configuration."""
        return MyMarketplaceEndpoints(
            base_url=self.base_url,
            library_url=f"{self.base_url}/v1/library",
            asset_details_url=f"{self.base_url}/v1/assets",
            download_url=f"{self.base_url}/v1/downloads"
        )
    
    def close(self) -> None:
        """Cleanup (if needed)."""
        pass
```

## Step 3: Define Domain Models

Create platform-specific models that extend the core base classes:

```python
# my_marketplace_client/models/domain/asset.py
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from asset_marketplace_core import BaseAsset

@dataclass
class MyAsset(BaseAsset):
    """Platform-specific asset model."""
    # Inherit: uid, title, description, created_at, updated_at, raw_data
    
    # Add platform-specific fields
    category: Optional[str] = None
    publisher: Optional[str] = None
    price: Optional[float] = None
    rating: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    download_url: Optional[str] = None
    
    # Add platform-specific methods
    def is_free(self) -> bool:
        """Check if asset is free."""
        return self.price == 0.0
    
    def has_tag(self, tag: str) -> bool:
        """Check if asset has a specific tag."""
        return tag.lower() in [t.lower() for t in self.tags]
```

```python
# my_marketplace_client/models/domain/collection.py
from dataclasses import dataclass, field
from typing import List, Optional
from asset_marketplace_core import BaseCollection
from .asset import MyAsset

@dataclass
class MyCollection(BaseCollection):
    """Platform-specific collection."""
    assets: List[MyAsset] = field(default_factory=list)
    
    # Add platform-specific filters
    def filter_by_category(self, category: str) -> 'MyCollection':
        """Filter by category."""
        filtered = [a for a in self.assets if a.category == category]
        return MyCollection(assets=filtered, total_count=len(filtered))
    
    def filter_free_assets(self) -> 'MyCollection':
        """Get only free assets."""
        filtered = [a for a in self.assets if a.is_free()]
        return MyCollection(assets=filtered, total_count=len(filtered))
```

## Step 4: Create API Response Models

Model your platform's API responses and provide converters to domain models:

```python
# my_marketplace_client/models/api/responses.py
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class ApiAsset:
    """Raw API response for an asset."""
    id: str
    name: str
    description: str
    category: str
    publisher: str
    price: float
    rating: float
    tags: List[str]
    created_at: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiAsset':
        """Parse from API JSON response."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            category=data.get('category', 'Unknown'),
            publisher=data.get('publisher', 'Unknown'),
            price=float(data.get('price', 0)),
            rating=float(data.get('rating', 0)),
            tags=data.get('tags', []),
            created_at=data.get('created_at', '')
        )
    
    def to_domain(self) -> 'MyAsset':
        """Convert to domain model."""
        from ..domain.asset import MyAsset
        
        return MyAsset(
            uid=self.id,
            title=self.name,
            description=self.description,
            category=self.category,
            publisher=self.publisher,
            price=self.price,
            rating=self.rating,
            tags=self.tags,
            created_at=self._parse_date(self.created_at),
            raw_data=self.__dict__
        )
    
    def _parse_date(self, date_str: str) -> datetime:
        """Parse platform's date format."""
        # Implement your platform's date parsing
        return datetime.fromisoformat(date_str)

@dataclass
class ApiLibraryResponse:
    """API response for library/collection."""
    assets: List[ApiAsset]
    total: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiLibraryResponse':
        """Parse from API JSON response."""
        return cls(
            assets=[ApiAsset.from_dict(item) for item in data['items']],
            total=data['total']
        )
    
    def to_collection(self) -> 'MyCollection':
        """Convert to domain collection."""
        from ..domain.collection import MyCollection
        
        return MyCollection(
            assets=[asset.to_domain() for asset in self.assets],
            total_count=self.total
        )
```

## Step 5: Implement the Client

Extend `MarketplaceClient` with your platform's implementation:

```python
# my_marketplace_client/client.py
from pathlib import Path
from typing import Optional, Union
import requests

from asset_marketplace_core import (
    MarketplaceClient,
    BaseAsset,
    BaseCollection,
    DownloadResult,
    ProgressCallback,
    MarketplaceError,
    MarketplaceNotFoundError,
    MarketplaceAPIError,
    MarketplaceNetworkError,
)

from .auth import MyMarketplaceAuth
from .models.domain import MyAsset, MyCollection
from .models.api import ApiLibraryResponse, ApiAsset
from .exceptions import MyMarketplaceError

class MyMarketplaceClient(MarketplaceClient):
    """Client for My Marketplace API."""
    
    def __init__(self, auth: MyMarketplaceAuth):
        """
        Initialize client with authentication.
        
        Args:
            auth: Authentication provider
        """
        self.auth = auth
        self.session = auth.get_session()
        self.endpoints = auth.get_endpoints()
    
    def get_collection(self, **kwargs) -> BaseCollection:
        """
        Retrieve user's asset library.
        
        Args:
            **kwargs: Platform-specific parameters (limit, offset, category, etc.)
        
        Returns:
            Collection of user's assets
        
        Raises:
            MarketplaceError: If retrieval fails
        """
        try:
            response = self.session.get(
                self.endpoints.library_url,
                params=kwargs
            )
            response.raise_for_status()
            
            # Parse API response
            api_response = ApiLibraryResponse.from_dict(response.json())
            
            # Convert to domain model
            return api_response.to_collection()
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise MarketplaceNotFoundError("Library not found")
            raise MarketplaceAPIError(f"API error: {e}")
        except requests.RequestException as e:
            raise MarketplaceNetworkError(f"Network error: {e}")
    
    def get_asset(self, asset_uid: str) -> BaseAsset:
        """
        Retrieve specific asset by ID.
        
        Args:
            asset_uid: Unique asset identifier
        
        Returns:
            Asset details
        
        Raises:
            MarketplaceNotFoundError: If asset doesn't exist
            MarketplaceError: If retrieval fails
        """
        try:
            url = self.endpoints.get_asset_url(asset_uid)
            response = self.session.get(url)
            response.raise_for_status()
            
            api_asset = ApiAsset.from_dict(response.json())
            return api_asset.to_domain()
            
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                raise MarketplaceNotFoundError(f"Asset {asset_uid} not found")
            raise MarketplaceAPIError(f"Failed to get asset: {e}")
    
    def download_asset(
        self,
        asset_uid: str,
        output_dir: Union[str, Path],
        progress_callback: Optional[ProgressCallback] = None,
        **kwargs
    ) -> DownloadResult:
        """
        Download asset to specified directory.
        
        Args:
            asset_uid: Asset to download
            output_dir: Directory to save files
            progress_callback: Optional progress callback
            **kwargs: Platform-specific parameters
        
        Returns:
            DownloadResult with success status
        
        Raises:
            MarketplaceError: If download fails
        """
        try:
            # Get asset details for download URL
            asset = self.get_asset(asset_uid)
            
            if not hasattr(asset, 'download_url') or not asset.download_url:
                return DownloadResult(
                    success=False,
                    asset_uid=asset_uid,
                    error="No download URL available"
                )
            
            # Download file
            output_path = Path(output_dir) / f"{asset.title}.zip"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            response = self.session.get(asset.download_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            if progress_callback:
                progress_callback.on_start(total_size)
            
            downloaded = 0
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            progress_callback.on_progress(downloaded, total_size)
            
            if progress_callback:
                progress_callback.on_complete()
            
            return DownloadResult(
                success=True,
                asset_uid=asset_uid,
                files=[str(output_path)],
                metadata={'size_bytes': total_size}
            )
            
        except Exception as e:
            if progress_callback:
                progress_callback.on_error(e)
            
            return DownloadResult(
                success=False,
                asset_uid=asset_uid,
                error=str(e)
            )
    
    def close(self) -> None:
        """Clean up resources."""
        if self.session:
            self.session.close()
```

## Step 6: Define Exceptions

Create platform-specific exceptions that inherit from core exceptions:

```python
# my_marketplace_client/exceptions.py
from asset_marketplace_core import (
    MarketplaceError,
    MarketplaceAuthenticationError,
    MarketplaceAPIError,
    MarketplaceNotFoundError,
    MarketplaceNetworkError,
)

class MyMarketplaceError(MarketplaceError):
    """Base exception for My Marketplace."""
    pass

class MyAuthenticationError(MyMarketplaceError, MarketplaceAuthenticationError):
    """Authentication error."""
    pass

class MyAPIError(MyMarketplaceError, MarketplaceAPIError):
    """API error."""
    pass

# Add platform-specific exceptions if needed
class MyRateLimitError(MyMarketplaceError):
    """Rate limit exceeded."""
    pass
```

## Step 7: Package Configuration

Create a modern `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-marketplace-client"
version = "0.1.0"
description = "Python client for My Marketplace API"
readme = "README.md"
requires-python = ">=3.7"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
dependencies = [
    "asset-marketplace-client-core>=0.1.0",
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "mypy>=1.0",
    "black>=23.0",
]

[project.urls]
Homepage = "https://github.com/username/my-marketplace-client"
Repository = "https://github.com/username/my-marketplace-client"

[tool.setuptools.packages.find]
where = ["src"]
```

## Step 8: Usage Example

```python
from my_marketplace_client import MyMarketplaceClient, MyMarketplaceAuth
from my_marketplace_client.models.domain import MyCollection

# Create auth provider
auth = MyMarketplaceAuth(api_key="your-api-key")

# Use with context manager
with MyMarketplaceClient(auth) as client:
    # Get your library
    collection = client.get_collection(limit=50)
    
    # Filter and search
    free_assets = collection.filter_free_assets()
    print(f"Free assets: {len(free_assets)}")
    
    # Get specific asset
    asset = client.get_asset("asset-123")
    print(f"Asset: {asset.title} by {asset.publisher}")
    
    # Download asset
    result = client.download_asset("asset-123", "./downloads")
    if result.success:
        print(f"Downloaded to: {result.files[0]}")
```

## Testing

Create comprehensive tests:

```python
# tests/test_client.py
import pytest
from my_marketplace_client import MyMarketplaceClient, MyMarketplaceAuth

def test_get_collection(mock_session):
    """Test collection retrieval."""
    auth = MyMarketplaceAuth(api_key="test-key")
    client = MyMarketplaceClient(auth)
    
    collection = client.get_collection()
    assert len(collection) > 0
    assert collection.total_count is not None

def test_get_asset(mock_session):
    """Test asset retrieval."""
    auth = MyMarketplaceAuth(api_key="test-key")
    client = MyMarketplaceClient(auth)
    
    asset = client.get_asset("test-asset-id")
    assert asset.uid == "test-asset-id"
    assert asset.title is not None
```

## Best Practices

1. **Separate Concerns:** Keep API types separate from domain models
2. **Error Handling:** Use appropriate exception types from core library
3. **Type Hints:** Add complete type hints for all public APIs
4. **Documentation:** Document all public methods and classes
5. **Testing:** Write unit tests with mocked API responses
6. **Versioning:** Follow semantic versioning
7. **Changelog:** Maintain CHANGELOG.md

## Additional Resources

- [Core Library API Reference](../README.md)
- [Integration Examples](./integration_examples.md)
- [Async API Plan](./async_api_plan.md)

## Authentication Adapters

For platforms that require credential extraction from launcher applications, consider creating a separate **adapter** package that:

1. Implements the auth provider from your platform client
2. Provides the platform-specific credential extraction logic
3. Is distributed separately with appropriate legal disclaimers
4. Respects the platform's terms of service

The adapter package would depend on your platform client (which depends on core), keeping the client library clean and publishable.

**Example structure:**
```
my-marketplace-client/       # Clean, open-source
my-marketplace-adapter/      # Platform-specific auth extraction (separate repo)
```

This separation allows the client library to remain completely clean while providing a convenient authentication solution for users who need it.
