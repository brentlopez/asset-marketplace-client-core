"""Progress callback abstraction for long-running operations."""

from abc import ABC, abstractmethod
from typing import Optional


class ProgressCallback(ABC):
    """Abstract base class for progress callbacks during operations like downloads.

    Platform implementations can provide concrete implementations for
    progress reporting (e.g., CLI progress bars, GUI progress indicators).

    Example:
        >>> class ConsoleProgress(ProgressCallback):
        ...     def on_start(self, total: Optional[int]) -> None:
        ...         print(f"Starting download ({total} bytes)")
        ...
        ...     def on_progress(self, current: int, total: Optional[int]) -> None:
        ...         if total:
        ...             percent = (current / total) * 100
        ...             print(f"Progress: {percent:.1f}%")
        ...
        ...     def on_complete(self) -> None:
        ...         print("Download complete!")
        ...
        ...     def on_error(self, error: Exception) -> None:
        ...         print(f"Error: {error}")
    """

    @abstractmethod
    def on_start(self, total: Optional[int]) -> None:
        """Called when an operation starts.

        Args:
            total: Total size/count if known, None if unknown
        """
        pass

    @abstractmethod
    def on_progress(self, current: int, total: Optional[int]) -> None:
        """Called periodically during operation to report progress.

        Args:
            current: Current progress (bytes downloaded, items processed, etc.)
            total: Total size/count if known, None if unknown
        """
        pass

    @abstractmethod
    def on_complete(self) -> None:
        """Called when operation completes successfully."""
        pass

    @abstractmethod
    def on_error(self, error: Exception) -> None:
        """Called when operation encounters an error.

        Args:
            error: The exception that occurred
        """
        pass
