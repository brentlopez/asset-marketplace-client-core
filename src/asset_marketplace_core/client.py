"""Marketplace client abstract base class."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from .models.base import BaseAsset, BaseCollection
from .models.progress import ProgressCallback
from .models.result import DownloadResult


class MarketplaceClient(ABC):
    """Abstract base class for marketplace API clients.
    
    Platform-specific implementations extend this class to provide
    concrete implementations for accessing marketplace APIs.
    
    Supports context manager protocol for automatic resource cleanup.
    
    Example:
        >>> class MyMarketplaceClient(MarketplaceClient):
        ...     def __init__(self, auth: MyAuthProvider):
        ...         self.auth = auth
        ...         self.session = auth.get_session()
        ...     
        ...     def get_collection(self, **kwargs) -> BaseCollection:
        ...         # Implementation
        ...         pass
        ...     
        ...     # ... other methods
        
        >>> with MyMarketplaceClient(auth) as client:
        ...     collection = client.get_collection()
        ...     for asset in collection.assets:
        ...         print(asset.title)
    """
    
    @abstractmethod
    def get_collection(self, **kwargs) -> BaseCollection:
        """Retrieve a collection of assets.
        
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
    def get_asset(self, asset_uid: str) -> BaseAsset:
        """Retrieve a specific asset by unique identifier.
        
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
    def download_asset(
        self,
        asset_uid: str,
        output_dir: Union[str, Path],
        progress_callback: Optional[ProgressCallback] = None,
        **kwargs
    ) -> DownloadResult:
        """Download an asset to the specified directory.
        
        Args:
            asset_uid: Unique identifier for the asset to download
            output_dir: Directory where asset files should be saved
            progress_callback: Optional callback for progress updates
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
    def close(self) -> None:
        """Close the client and clean up resources.
        
        Should be called when done with the client to ensure proper
        cleanup of network connections, file handles, etc.
        
        When using the context manager, this is called automatically.
        """
        pass
    
    def __enter__(self) -> 'MarketplaceClient':
        """Enter context manager.
        
        Returns:
            Self for use in with statement
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager and clean up resources.
        
        Args:
            exc_type: Exception type if an error occurred
            exc_val: Exception value if an error occurred
            exc_tb: Exception traceback if an error occurred
        """
        self.close()
