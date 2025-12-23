"""Utility functions for asset marketplace operations."""

import re
from pathlib import Path
from typing import Union
from urllib.parse import urlparse

from .exceptions import MarketplaceValidationError


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing or replacing invalid characters.

    Removes characters that are not allowed in filenames on most filesystems,
    including: / \\ : * ? " < > |

    Args:
        filename: The filename to sanitize

    Returns:
        A sanitized filename safe for use on most filesystems

    Raises:
        MarketplaceValidationError: If filename is empty after sanitization

    Examples:
        >>> sanitize_filename("My Asset: Version 2.0")
        'My Asset Version 2.0'
        >>> sanitize_filename("file/with\\\\invalid:chars")
        'filewithinvalidchars'
    """
    if not filename:
        raise MarketplaceValidationError("Filename cannot be empty")

    # Remove or replace invalid characters
    # Windows: / \\ : * ? " < > |
    # Unix: /
    sanitized = re.sub(r'[/\\:*?"<>|]', "", filename)

    # Remove leading/trailing whitespace and dots
    sanitized = sanitized.strip(". ")

    if not sanitized:
        raise MarketplaceValidationError(
            f"Filename '{filename}' contains only invalid characters"
        )

    return sanitized


def validate_url(url: str) -> bool:
    """Validate that a string is a well-formed URL.

    Checks that the URL has a valid scheme (http/https) and network location.

    Args:
        url: The URL to validate

    Returns:
        True if URL is valid, False otherwise

    Examples:
        >>> validate_url("https://example.com/api/asset")
        True
        >>> validate_url("not-a-url")
        False
        >>> validate_url("ftp://example.com")
        False
    """
    if not url:
        return False

    try:
        result = urlparse(url)
        # Check for valid scheme (http/https) and network location
        return all(
            [
                result.scheme in ("http", "https"),
                result.netloc,
            ]
        )
    except (ValueError, AttributeError):
        return False


def safe_create_directory(path: Union[str, Path]) -> None:
    """Create a directory and all necessary parent directories.

    This is a safe wrapper around os.makedirs that handles existing directories
    gracefully and provides better error messages.

    Args:
        path: Path to the directory to create

    Raises:
        MarketplaceValidationError: If path is invalid or cannot be created

    Examples:
        >>> safe_create_directory("/tmp/my/nested/dir")
        >>> safe_create_directory(Path.home() / "downloads")
    """
    if not path:
        raise MarketplaceValidationError("Directory path cannot be empty")

    path_obj = Path(path)

    try:
        path_obj.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise MarketplaceValidationError(
            f"Failed to create directory '{path}': {e}"
        ) from e


def format_bytes(byte_count: int) -> str:
    """Format a byte count into a human-readable string.

    Converts byte counts to the most appropriate unit (B, KB, MB, GB, TB).

    Args:
        byte_count: Number of bytes to format

    Returns:
        Human-readable string with appropriate unit

    Examples:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1536)
        '1.50 KB'
        >>> format_bytes(1048576)
        '1.00 MB'
        >>> format_bytes(5368709120)
        '5.00 GB'
    """
    if byte_count < 0:
        return "0 B"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    size = float(byte_count)

    while size >= 1024.0 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1

    # Format with 2 decimal places, but strip trailing zeros
    if unit_index == 0:  # Bytes - no decimal
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"
