# Async API Implementation Plan

This document outlines the strategy for adding asynchronous API support to `asset-marketplace-client-core`.

## Goals

1. Add async versions of all core abstractions
2. Maintain Python 3.7+ compatibility (`asyncio` available)
3. Keep sync and async APIs coexisting (no breaking changes)
4. Enable async HTTP libraries (aiohttp, httpx async)
5. Support async progress callbacks

## Design Principles

### Separate but Parallel

- **Sync API:** `MarketplaceClient`, `AuthProvider`, `ProgressCallback`
- **Async API:** `AsyncMarketplaceClient`, `AsyncAuthProvider`, `AsyncProgressCallback`
- **Shared:** `BaseAsset`, `BaseCollection`, `DownloadResult`, exceptions, utils

### No Shared Base Class

Avoid inheritance between sync/async to prevent confusion:
```python
# ❌ Don't do this
class MarketplaceClient(ABC):
    pass

class AsyncMarketplaceClient(MarketplaceClient):  # Confusing!
    pass

# ✅ Do this
class MarketplaceClient(ABC):
    """Synchronous client."""
    pass

class AsyncMarketplaceClient(ABC):
    """Asynchronous client (separate hierarchy)."""
    pass
```

## Proposed API Structure

### New Modules

```
src/asset_marketplace_core/
├── __init__.py
├── client/
│   ├── __init__.py
│   ├── sync.py          # Sync client (MarketplaceClient)
│   └── async_.py        # NEW: Async client (AsyncMarketplaceClient)
├── auth/
│   ├── __init__.py
│   ├── sync.py          # Sync auth (AuthProvider, EndpointConfig)
│   └── async_.py        # NEW: Async auth (AsyncAuthProvider)
├── models/
│   ├── __init__.py
│   ├── base.py          # Shared models
│   ├── progress.py      # Sync progress
│   ├── async_progress.py  # NEW: Async progress
│   └── result.py        # Shared result
├── exceptions.py        # Shared exceptions
└── utils.py             # Shared utils
```

**Note:** Using `async_.py` instead of `async.py` to avoid conflict with Python's `async` keyword.

### Backward Compatibility

When reorganizing into directories, maintain backward compatibility in `__init__.py`:

```python
# asset_marketplace_core/__init__.py

# Backward compatible imports (v0.1.0 style)
from .client.sync import MarketplaceClient
from .auth.sync import AuthProvider, EndpointConfig

# New async imports (v0.2.0)
from .client.async_ import AsyncMarketplaceClient
from .auth.async_ import AsyncAuthProvider

# ... other imports

__all__ = [
    # Sync API (existing)
    "MarketplaceClient",
    "AuthProvider",
    "EndpointConfig",
    # Async API (new)
    "AsyncMarketplaceClient",
    "AsyncAuthProvider",
    # ...
]
```

This ensures existing code using `from asset_marketplace_core import MarketplaceClient` continues to work.

### Async Client ABC

```python
# asset_marketplace_core/client/async_.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from .models.base import BaseAsset, BaseCollection
from .models.async_progress import AsyncProgressCallback
from .models.result import DownloadResult


class AsyncMarketplaceClient(ABC):
    """Abstract base class for asynchronous marketplace API clients.
    
    Supports async context manager protocol for automatic resource cleanup.
    
    Example:
        >>> async with MyAsyncMarketplaceClient(auth) as client:
        ...     collection = await client.get_collection()
        ...     for asset in collection.assets:
        ...         print(asset.title)
    """
    
    @abstractmethod
    async def get_collection(self, **kwargs) -> BaseCollection:
        """Retrieve a collection of assets asynchronously.
        
        Args:
            **kwargs: Platform-specific query parameters
            
        Returns:
            Collection of assets
        """
        pass
    
    @abstractmethod
    async def get_asset(self, asset_uid: str) -> BaseAsset:
        """Retrieve a specific asset by unique identifier.
        
        Args:
            asset_uid: Unique identifier for the asset
            
        Returns:
            Asset details
        """
        pass
    
    @abstractmethod
    async def download_asset(
        self,
        asset_uid: str,
        output_dir: Union[str, Path],
        progress_callback: Optional[AsyncProgressCallback] = None,
        **kwargs
    ) -> DownloadResult:
        """Download an asset to the specified directory.
        
        Args:
            asset_uid: Unique identifier for the asset to download
            output_dir: Directory where asset files should be saved
            progress_callback: Optional async callback for progress updates
            **kwargs: Platform-specific download parameters
            
        Returns:
            DownloadResult with details of the operation
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the client and clean up resources asynchronously."""
        pass
    
    async def __aenter__(self) -> 'AsyncMarketplaceClient':
        """Enter async context manager."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager and clean up resources."""
        await self.close()
```

### Async Auth Provider

```python
# asset_marketplace_core/auth/async_.py
from abc import ABC, abstractmethod
from typing import Any

from .sync import EndpointConfig


class AsyncAuthProvider(ABC):
    """Abstract base class for asynchronous authentication providers.
    
    Platform implementations must provide async authentication configuration.
    The session object type is intentionally Any to avoid dependencies on
    specific async HTTP libraries (aiohttp, httpx, etc.).
    """
    
    @abstractmethod
    async def get_session(self) -> Any:
        """Get configured async session/client for making authenticated requests.
        
        Returns:
            Configured async session object (e.g., aiohttp.ClientSession, httpx.AsyncClient)
            
        Note:
            The return type is intentionally Any to avoid dependencies.
            Platform implementations should document their specific return type.
        """
        pass
    
    @abstractmethod
    def get_endpoints(self) -> EndpointConfig:
        """Get API endpoint configuration.
        
        Note: Synchronous method - endpoint config doesn't require async.
        
        Returns:
            EndpointConfig instance (or platform-specific subclass)
        """
        pass
    
    async def refresh(self) -> None:
        """Refresh authentication credentials asynchronously if supported."""
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support credential refresh"
        )
    
    async def close(self) -> None:
        """Clean up any resources held by the auth provider asynchronously."""
        pass
```

### Async Progress Callback

```python
# asset_marketplace_core/models/async_progress.py
from abc import ABC, abstractmethod
from typing import Optional


class AsyncProgressCallback(ABC):
    """Abstract base class for async progress callbacks.
    
    Example:
        >>> class AsyncConsoleProgress(AsyncProgressCallback):
        ...     async def on_start(self, total: Optional[int]) -> None:
        ...         print(f"Starting download ({total} bytes)")
        ...     
        ...     async def on_progress(self, current: int, total: Optional[int]) -> None:
        ...         if total:
        ...             percent = (current / total) * 100
        ...             print(f"Progress: {percent:.1f}%")
        ...     
        ...     async def on_complete(self) -> None:
        ...         print("Download complete!")
        ...     
        ...     async def on_error(self, error: Exception) -> None:
        ...         print(f"Error: {error}")
    """
    
    @abstractmethod
    async def on_start(self, total: Optional[int]) -> None:
        """Called when an operation starts."""
        pass
    
    @abstractmethod
    async def on_progress(self, current: int, total: Optional[int]) -> None:
        """Called periodically during operation to report progress."""
        pass
    
    @abstractmethod
    async def on_complete(self) -> None:
        """Called when operation completes successfully."""
        pass
    
    @abstractmethod
    async def on_error(self, error: Exception) -> None:
        """Called when operation encounters an error."""
        pass
```

## Platform Implementation Example

```python
# Example async platform client implementation
from asset_marketplace_core import (
    AsyncMarketplaceClient,
    AsyncAuthProvider,
    BaseAsset,
    BaseCollection,
    DownloadResult,
)
import aiohttp


class MyAsyncAuth(AsyncAuthProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._session = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
        return self._session
    
    def get_endpoints(self) -> MyPlatformEndpoints:
        return MyPlatformEndpoints(base_url="https://api.example.com")
    
    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()


class MyAsyncClient(AsyncMarketplaceClient):
    def __init__(self, auth: MyAsyncAuth):
        self.auth = auth
        self.endpoints = auth.get_endpoints()
    
    async def get_collection(self, **kwargs) -> BaseCollection:
        session = await self.auth.get_session()
        async with session.get(self.endpoints.library_url, params=kwargs) as response:
            response.raise_for_status()
            data = await response.json()
            
            assets = [
                BaseAsset(
                    uid=item['id'],
                    title=item['name'],
                    raw_data=item
                )
                for item in data['assets']
            ]
            
            return BaseCollection(assets=assets, total_count=data['total'])
    
    async def get_asset(self, asset_uid: str) -> BaseAsset:
        session = await self.auth.get_session()
        url = f"{self.endpoints.asset_url}/{asset_uid}"
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            return BaseAsset(uid=data['id'], title=data['name'], raw_data=data)
    
    async def download_asset(self, asset_uid, output_dir, progress_callback=None, **kwargs):
        # Async download implementation
        session = await self.auth.get_session()
        # ... download logic with async progress callbacks
        return DownloadResult(success=True, asset_uid=asset_uid, files=[...])
    
    async def close(self) -> None:
        await self.auth.close()


# Usage
async def main():
    async with MyAsyncClient(MyAsyncAuth("api-key")) as client:
        collection = await client.get_collection(limit=10)
        for asset in collection.assets:
            print(asset.title)

# Run
import asyncio
asyncio.run(main())
```

## Python 3.7 Compatibility

### Use Standard asyncio

```python
# ✅ Python 3.7+
import asyncio

async def example():
    await asyncio.sleep(1)

asyncio.run(example())  # 3.7+
```

### Type Hints

```python
# ✅ Use typing module for 3.7+
from typing import Optional, List
from __future__ import annotations  # 3.7+ for forward references

async def get_collection(self, **kwargs) -> 'BaseCollection':
    pass
```

### Avoid 3.8+ Features

```python
# ❌ Don't use (3.8+)
async def example(name: str = "default", /):  # Positional-only 3.8+
    pass

# ✅ Use
async def example(name: str = "default"):
    pass
```

## Implementation Phases

### Phase 1: Core Async Abstractions (v0.2.0)
**Timeline:** 2-3 weeks

- [ ] Reorganize current code into `client/sync.py` and `auth/sync.py`
- [ ] Create `client/async_.py` with `AsyncMarketplaceClient`
- [ ] Create `auth/async_.py` with `AsyncAuthProvider`
- [ ] Create `models/async_progress.py` with `AsyncProgressCallback`
- [ ] Update `__init__.py` exports (maintain backward compatibility)
- [ ] Add type stubs (py.typed)
- [ ] Update documentation
- [ ] Add usage examples

### Phase 2: Testing & Documentation (v0.2.1)
**Timeline:** 1-2 weeks

- [ ] Create example async implementations
- [ ] Add async test utilities
- [ ] Document migration from sync to async
- [ ] Update README with async examples

### Phase 3: Platform Migrations (v0.3.0+)
**Timeline:** Per platform

- [ ] Migrate `fab-api-client` to add async support
- [ ] Migrate `uas-api-client` to add async support
- [ ] Create example async adapters

## Benefits

1. **Performance:** Handle multiple concurrent requests efficiently
2. **Scalability:** Better resource utilization for bulk operations
3. **Modern:** Aligns with modern Python async ecosystem
4. **Optional:** Sync API remains unchanged - no breaking changes
5. **Interoperability:** Works with popular async HTTP libraries

## Compatibility Matrix

| Python Version | Sync API | Async API |
|---------------|----------|-----------|
| 3.7           | ✅       | ✅        |
| 3.8           | ✅       | ✅        |
| 3.9           | ✅       | ✅        |
| 3.10+         | ✅       | ✅        |

## Migration Guide for Platform Implementations

### Adding Async to Existing Sync Client

1. **Keep sync implementation** - no breaking changes
2. **Create async variant** - parallel implementation
3. **Share models** - BaseAsset, BaseCollection, etc.
4. **Document both** - clear examples for each

```python
# Both sync and async in same package
from my_platform_client import (
    MyClient,           # Sync
    MyAsyncClient,      # Async
    MyAuth,             # Sync auth
    MyAsyncAuth,        # Async auth
)

# Sync usage
with MyClient(MyAuth("key")) as client:
    assets = client.get_collection()

# Async usage
async with MyAsyncClient(MyAsyncAuth("key")) as client:
    assets = await client.get_collection()
```

## Open Questions

1. **Async utils?** Should utility functions have async versions?
   - Likely NO - file operations can remain sync
2. **Async collection methods?** Should `BaseCollection.filter()` be async?
   - Likely NO - pure Python operations don't benefit from async
3. **Mixed usage?** Can async client use sync auth?
   - Best to keep separate for clarity

## References

- [PEP 492 - Coroutines with async and await syntax](https://www.python.org/dev/peps/pep-0492/)
- [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [httpx Async Client](https://www.python-httpx.org/async/)
