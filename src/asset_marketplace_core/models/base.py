"""Base data models for assets and collections."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


@dataclass
class BaseAsset:
    """Base representation of a marketplace asset.
    
    Platform-specific implementations should extend this class to add
    their own fields (e.g., publisher, category, price, dependencies).
    
    Attributes:
        uid: Unique identifier for the asset
        title: Human-readable name of the asset
        description: Optional description of the asset
        created_at: Timestamp when asset was created or added to library
        updated_at: Timestamp when asset was last updated
        raw_data: Complete raw API response data for extensibility
    """
    
    uid: str
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BaseCollection:
    """Base collection of marketplace assets.
    
    Platform-specific implementations should extend this class to add
    their own filtering and sorting methods (e.g., filter_by_category,
    sort_by_price).
    
    Attributes:
        assets: List of assets in the collection
        total_count: Total number of assets (may differ from len(assets) for paginated results)
    """
    
    assets: List[BaseAsset] = field(default_factory=list)
    total_count: Optional[int] = None
    
    def __len__(self) -> int:
        """Get number of assets in collection.
        
        Returns:
            Number of assets
        """
        return len(self.assets)
    
    def filter(self, predicate: Callable[[BaseAsset], bool]) -> 'BaseCollection':
        """Filter assets by predicate function.
        
        Args:
            predicate: Function that takes an asset and returns True to include it
            
        Returns:
            New collection with filtered assets
            
        Examples:
            >>> collection.filter(lambda a: a.title.startswith("Epic"))
            >>> collection.filter(lambda a: a.created_at > some_date)
        """
        filtered_assets = [asset for asset in self.assets if predicate(asset)]
        return BaseCollection(
            assets=filtered_assets,
            total_count=len(filtered_assets)
        )
    
    def find_by_uid(self, uid: str) -> Optional[BaseAsset]:
        """Find asset by unique identifier.
        
        Args:
            uid: Asset unique identifier to search for
            
        Returns:
            Asset if found, None otherwise
            
        Examples:
            >>> asset = collection.find_by_uid("12345")
            >>> if asset:
            ...     print(asset.title)
        """
        for asset in self.assets:
            if asset.uid == uid:
                return asset
        return None
