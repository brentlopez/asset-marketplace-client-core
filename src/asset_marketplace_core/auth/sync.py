"""Authentication and endpoint configuration abstractions."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class EndpointConfig:
    """Base configuration for API endpoints.

    Platform-specific implementations should extend this to add their
    specific endpoint URLs (e.g., library_url, asset_url, download_url).

    Attributes:
        base_url: Base URL for the API (e.g., "https://api.example.com")

    Examples:
        >>> # Platform-specific extension
        >>> @dataclass
        >>> class FabEndpoints(EndpointConfig):
        ...     library_search: str
        ...     asset_formats: str
        ...     download_info: str
    """

    base_url: str


class AuthProvider(ABC):
    """Abstract base class for authentication providers.

    Platform implementations must provide authentication configuration
    and endpoint URLs. The session object type is intentionally left
    as 'Any' to avoid dependencies on specific HTTP libraries.

    Platform implementations will typically return a requests.Session,
    httpx.Client, or similar HTTP client object.
    """

    @abstractmethod
    def get_session(self) -> Any:
        """Get configured session/client for making authenticated requests.

        Returns:
            Configured session object (e.g., requests.Session, httpx.Client)

        Note:
            The return type is intentionally Any to avoid dependencies.
            Platform implementations should document their specific return type.
        """
        pass

    @abstractmethod
    def get_endpoints(self) -> EndpointConfig:
        """Get API endpoint configuration.

        Returns:
            EndpointConfig instance (or platform-specific subclass)
        """
        pass

    def refresh(self) -> None:
        """Refresh authentication credentials if supported.

        Platform implementations can override this to implement token
        refresh or credential renewal. Default implementation does nothing.

        Raises:
            NotImplementedError: If platform doesn't support refresh
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support credential refresh"
        )

    def close(self) -> None:  # noqa: B027
        """Clean up any resources held by the auth provider.

        Platform implementations should override this if they hold
        resources that need cleanup (e.g., open connections, temp files).
        Default implementation does nothing.
        """
        # Default implementation: no cleanup needed
        # Platform implementations can override if needed
