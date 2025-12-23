"""Asset Marketplace Client Core Library.

A platform-agnostic library providing base abstractions for asset marketplace clients.
Platforms (Fab, Unity Asset Store, etc.) extend these base classes with their specific implementations.
"""

from .auth import AuthProvider, EndpointConfig
from .client import MarketplaceClient
from .exceptions import (
    MarketplaceError,
    MarketplaceAuthenticationError,
    MarketplaceAPIError,
    MarketplaceNotFoundError,
    MarketplaceNetworkError,
    MarketplaceValidationError,
)
from .models.base import BaseAsset, BaseCollection
from .models.progress import ProgressCallback
from .models.result import DownloadResult
from .utils import (
    sanitize_filename,
    validate_url,
    safe_create_directory,
    format_bytes,
)

__version__ = "0.1.0"

__all__ = [
    # Auth
    "AuthProvider",
    "EndpointConfig",
    # Client
    "MarketplaceClient",
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
    "DownloadResult",
    # Utils
    "sanitize_filename",
    "validate_url",
    "safe_create_directory",
    "format_bytes",
]
