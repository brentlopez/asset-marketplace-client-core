"""Asynchronous marketplace client abstract base class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Union

from ..models.base import BaseAsset, BaseCollection
from ..models.result import DownloadResult


class AsyncMarketplaceClient(ABC):
    """Abstract base class for asynchronous marketplace API clients.

    Platform-specific implementations extend this class to provide
    concrete implementations for accessing marketplace APIs asynchronously.

    Supports async context manager protocol for automatic resource cleanup.

    Example:
        >>> class MyAsyncMarketplaceClient(AsyncMarketplaceClient):
        ...     def __init__(self, auth: MyAsyncAuthProvider):
        ...         self.auth = auth
        ...
        ...     async def get_collection(self, **kwargs) -> BaseCollection:
        ...         # Implementation
        ...         pass
        ...
        ...     # ... other methods

        >>> async with MyAsyncMarketplaceClient(auth) as client:
        ...     collection = await client.get_collection()
        ...     for asset in collection.assets:
        ...         print(asset.title)
    """

    @abstractmethod
    async def get_collection(self, **kwargs: Any) -> BaseCollection:
        """Retrieve a collection of assets asynchronously.

        Platform implementations define their own query parameters
        (e.g., limit, offset, search, category).

        Args:
            **kwargs: Platform-specific query parameters

        Returns:
            Collection of assets

        Raises:
            MarketplaceError: If collection retrieval fails
        """
        pass

    @abstractmethod
    async def get_asset(self, asset_uid: str) -> BaseAsset:
        """Retrieve a specific asset by unique identifier asynchronously.

        Args:
            asset_uid: Unique identifier for the asset

        Returns:
            Asset details

        Raises:
            MarketplaceNotFoundError: If asset doesn't exist
            MarketplaceError: If asset retrieval fails
        """
        pass

    @abstractmethod
    async def download_asset(
        self,
        asset_uid: str,
        output_dir: Union[str, Path],
        progress_callback: Optional[Any] = None,
        **kwargs: Any,
    ) -> DownloadResult:
        """Download an asset to the specified directory asynchronously.

        Args:
            asset_uid: Unique identifier for the asset to download
            output_dir: Directory where asset files should be saved
            progress_callback: Optional async callback for progress updates
            **kwargs: Platform-specific download parameters

        Returns:
            DownloadResult with details of the operation

        Raises:
            MarketplaceNotFoundError: If asset doesn't exist
            MarketplaceValidationError: If output_dir is invalid
            MarketplaceError: If download fails
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close the client and clean up resources asynchronously.

        Should be called when done with the client to ensure proper
        cleanup of network connections, file handles, etc.

        When using the async context manager, this is called automatically.
        """
        pass

    async def __aenter__(self) -> AsyncMarketplaceClient:
        """Enter async context manager.

        Returns:
            Self for use in async with statement
        """
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit async context manager and clean up resources.

        Args:
            exc_type: Exception type if an error occurred
            exc_val: Exception value if an error occurred
            exc_tb: Exception traceback if an error occurred
        """
        await self.close()
