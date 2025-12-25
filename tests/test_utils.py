"""Tests for utility functions."""

import tempfile
from pathlib import Path

import pytest

from asset_marketplace_core import (
    MarketplaceValidationError,
    format_bytes,
    safe_create_directory,
    sanitize_filename,
    validate_url,
)


def test_sanitize_filename_valid() -> None:
    """Test sanitizing valid filename."""
    assert sanitize_filename("my_file.txt") == "my_file.txt"
    assert sanitize_filename("Asset Name 2024") == "Asset Name 2024"


def test_sanitize_filename_invalid_chars() -> None:
    """Test sanitizing filename with invalid characters."""
    assert sanitize_filename("file/with\\slashes") == "filewithslashes"
    assert sanitize_filename("file:with*special?chars") == "filewithspecialchars"
    assert sanitize_filename('file<with>quotes"') == "filewithquotes"


def test_sanitize_filename_empty() -> None:
    """Test sanitizing empty filename raises error."""
    with pytest.raises(MarketplaceValidationError):
        sanitize_filename("")


def test_sanitize_filename_only_invalid() -> None:
    """Test sanitizing filename with only invalid characters."""
    with pytest.raises(MarketplaceValidationError):
        sanitize_filename("///***???")


def test_validate_url_valid() -> None:
    """Test validating valid URLs."""
    assert validate_url("https://example.com")
    assert validate_url("http://api.example.com/v1/assets")
    assert validate_url("https://cdn.example.com/files/asset.zip")


def test_validate_url_invalid() -> None:
    """Test validating invalid URLs."""
    assert not validate_url("")
    assert not validate_url("not-a-url")
    assert not validate_url("ftp://example.com")
    assert not validate_url("file:///etc/passwd")
    assert not validate_url("javascript:alert('xss')")


def test_safe_create_directory() -> None:
    """Test creating directory safely."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir) / "nested" / "directory"
        safe_create_directory(test_dir)
        assert test_dir.exists()
        assert test_dir.is_dir()


def test_safe_create_directory_exists() -> None:
    """Test creating directory that already exists."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Should not raise even if directory exists
        safe_create_directory(tmpdir)
        safe_create_directory(tmpdir)


def test_safe_create_directory_empty() -> None:
    """Test creating directory with empty path raises error."""
    with pytest.raises(MarketplaceValidationError):
        safe_create_directory("")


def test_format_bytes() -> None:
    """Test formatting byte counts."""
    assert format_bytes(0) == "0 B"
    assert format_bytes(512) == "512 B"
    assert format_bytes(1024) == "1.00 KB"
    assert format_bytes(1536) == "1.50 KB"
    assert format_bytes(1048576) == "1.00 MB"
    assert format_bytes(1073741824) == "1.00 GB"
    assert format_bytes(5368709120) == "5.00 GB"


def test_format_bytes_negative() -> None:
    """Test formatting negative byte count."""
    assert format_bytes(-100) == "0 B"
