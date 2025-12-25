"""Test backward compatibility of imports after code reorganization."""

import pytest


def test_sync_imports_from_main_package() -> None:
    """Test that sync classes can be imported from main package."""
    from asset_marketplace_core import (
        AuthProvider,
        BaseAsset,
        BaseCollection,
        DownloadResult,
        EndpointConfig,
        MarketplaceClient,
        ProgressCallback,
    )

    # Verify classes are available
    assert AuthProvider is not None
    assert EndpointConfig is not None
    assert MarketplaceClient is not None
    assert BaseAsset is not None
    assert BaseCollection is not None
    assert ProgressCallback is not None
    assert DownloadResult is not None


def test_async_imports_from_main_package() -> None:
    """Test that async classes can be imported from main package."""
    from asset_marketplace_core import (
        AsyncAuthProvider,
        AsyncMarketplaceClient,
        AsyncProgressCallback,
    )

    # Verify async classes are available
    assert AsyncAuthProvider is not None
    assert AsyncMarketplaceClient is not None
    assert AsyncProgressCallback is not None


def test_exception_imports() -> None:
    """Test that exceptions can be imported."""
    from asset_marketplace_core import (
        MarketplaceAPIError,
        MarketplaceAuthenticationError,
        MarketplaceError,
        MarketplaceNetworkError,
        MarketplaceNotFoundError,
        MarketplaceValidationError,
    )

    # Verify exceptions are available
    assert MarketplaceError is not None
    assert MarketplaceAuthenticationError is not None
    assert MarketplaceAPIError is not None
    assert MarketplaceNotFoundError is not None
    assert MarketplaceNetworkError is not None
    assert MarketplaceValidationError is not None


def test_utility_imports() -> None:
    """Test that utility functions can be imported."""
    from asset_marketplace_core import (
        format_bytes,
        safe_create_directory,
        sanitize_filename,
        validate_url,
    )

    # Verify utilities are available
    assert sanitize_filename is not None
    assert validate_url is not None
    assert safe_create_directory is not None
    assert format_bytes is not None


def test_all_exports_present() -> None:
    """Test that __all__ contains expected exports."""
    import asset_marketplace_core

    expected_exports = {
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
    }

    actual_exports = set(asset_marketplace_core.__all__)
    assert expected_exports == actual_exports, f"Missing or extra exports: {expected_exports.symmetric_difference(actual_exports)}"
