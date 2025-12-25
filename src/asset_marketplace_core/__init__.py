"""Asset Marketplace Client Core Library.

A platform-agnostic library providing base abstractions for asset marketplace
clients. Platforms (Fab, Unity Asset Store, etc.) extend these base classes
with their specific implementations.
"""

from .auth import AsyncAuthProvider, AuthProvider, EndpointConfig
from .client import AsyncMarketplaceClient, MarketplaceClient
from .exceptions import (
    MarketplaceAPIError,
    MarketplaceAuthenticationError,
    MarketplaceError,
    MarketplaceNetworkError,
    MarketplaceNotFoundError,
    MarketplaceValidationError,
)
from .models import AsyncProgressCallback, ProgressCallback
from .models.base import BaseAsset, BaseCollection
from .models.result import DownloadResult
from .utils import (
    format_bytes,
    safe_create_directory,
    sanitize_filename,
    validate_url,
)

__version__ = "0.2.0"

__all__ = [
    # Sync Auth
    "AuthProvider",
    "EndpointConfig",
    # Async Auth
    "AsyncAuthProvider",
    # Sync Client
    "MarketplaceClient",
    # Async Client
    "AsyncMarketplaceClient",
    # Exceptions
    "MarketplaceError",
    "MarketplaceAuthenticationError",
    "MarketplaceAPIError",
    "MarketplaceNotFoundError",
    "MarketplaceNetworkError",
    "MarketplaceValidationError",
    # Models
    "BaseAsset",
    "BaseCollection",
    "ProgressCallback",
    "AsyncProgressCallback",
    "DownloadResult",
    # Utils
    "sanitize_filename",
    "validate_url",
    "safe_create_directory",
    "format_bytes",
]
