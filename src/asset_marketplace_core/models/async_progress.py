"""Asynchronous progress callback abstraction for long-running operations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class AsyncProgressCallback(ABC):
    """Abstract base class for async progress callbacks during operations.

    Platform implementations can provide concrete implementations for
    async progress reporting (e.g., async CLI, async GUI indicators).

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

        >>> async with MyAsyncClient(auth) as client:
        ...     result = await client.download_asset(
        ...         "asset-123",
        ...         "./downloads",
        ...         progress_callback=AsyncConsoleProgress()
        ...     )
    """

    @abstractmethod
    async def on_start(self, total: Optional[int]) -> None:
        """Called when an operation starts.

        Args:
            total: Total size/count if known, None if unknown
        """
        pass

    @abstractmethod
    async def on_progress(self, current: int, total: Optional[int]) -> None:
        """Called periodically during operation to report progress.

        Args:
            current: Current progress (bytes downloaded, items processed, etc.)
            total: Total size/count if known, None if unknown
        """
        pass

    @abstractmethod
    async def on_complete(self) -> None:
        """Called when operation completes successfully."""
        pass

    @abstractmethod
    async def on_error(self, error: Exception) -> None:
        """Called when operation encounters an error.

        Args:
            error: The exception that occurred
        """
        pass
