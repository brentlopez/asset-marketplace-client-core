"""Asynchronous authentication abstractions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .sync import EndpointConfig


class AsyncAuthProvider(ABC):
    """Abstract base class for asynchronous authentication providers.

    Platform implementations must provide async authentication configuration
    and endpoint URLs. The session object type is intentionally left
    as 'Any' to avoid dependencies on specific async HTTP libraries
    (aiohttp, httpx, etc.).

    Platform implementations will typically return an aiohttp.ClientSession,
    httpx.AsyncClient, or similar async HTTP client object.

    Example:
        >>> class MyAsyncAuth(AsyncAuthProvider):
        ...     def __init__(self, api_key: str):
        ...         self.api_key = api_key
        ...         self._session = None
        ...
        ...     async def get_session(self):
        ...         if self._session is None:
        ...             import aiohttp
        ...             self._session = aiohttp.ClientSession(
        ...                 headers={'Authorization': f'Bearer {self.api_key}'}
        ...             )
        ...         return self._session
        ...
        ...     def get_endpoints(self) -> EndpointConfig:
        ...         return MyPlatformEndpoints(base_url=\"https://api.example.com\")
        ...
        ...     async def close(self) -> None:
        ...         if self._session and not self._session.closed:
        ...             await self._session.close()
    """

    @abstractmethod
    async def get_session(self) -> Any:
        """Get configured async session/client for making authenticated requests.

        Returns:
            Configured async session object (e.g., aiohttp.ClientSession,
            httpx.AsyncClient)

        Note:
            The return type is intentionally Any to avoid dependencies.
            Platform implementations should document their specific return type.

        Raises:
            MarketplaceAuthenticationError: If authentication setup fails
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
        """Refresh authentication credentials asynchronously if supported.

        Platform implementations can override this to implement token
        refresh or credential renewal. Default implementation raises
        NotImplementedError.

        Raises:
            NotImplementedError: If platform doesn't support refresh
            MarketplaceAuthenticationError: If refresh fails
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support credential refresh"
        )

    async def close(self) -> None:
        """Clean up any resources held by the auth provider asynchronously.

        Platform implementations should override this if they hold
        resources that need cleanup (e.g., open connections, temp files).
        Default implementation does nothing.
        """
        # Default implementation: no cleanup needed
        # Platform implementations can override if needed
        pass
