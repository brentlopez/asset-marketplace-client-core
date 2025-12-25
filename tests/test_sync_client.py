"""Tests for synchronous MarketplaceClient ABC."""

from pathlib import Path

import pytest

from asset_marketplace_core import (
    BaseAsset,
    BaseCollection,
    DownloadResult,
    MarketplaceClient,
    ProgressCallback,
)


class MockSyncClient(MarketplaceClient):
    """Mock implementation for testing."""

    def __init__(self) -> None:
        self.closed = False

    def get_collection(self, **kwargs) -> BaseCollection:  # type: ignore[no-untyped-def]
        return BaseCollection(
            assets=[BaseAsset(uid="test-1", title="Test Asset")], total_count=1
        )

    def get_asset(self, asset_uid: str) -> BaseAsset:
        return BaseAsset(uid=asset_uid, title=f"Asset {asset_uid}")

    def download_asset(
        self,
        asset_uid: str,
        output_dir: str | Path,
        progress_callback: ProgressCallback | None = None,
        **kwargs,  # type: ignore[no-untyped-def]
    ) -> DownloadResult:
        return DownloadResult(success=True, asset_uid=asset_uid, files=[])

    def close(self) -> None:
        self.closed = True


def test_client_context_manager() -> None:
    """Test that client works as context manager."""
    client = MockSyncClient()
    assert not client.closed

    with client as ctx_client:
        assert ctx_client is client
        assert not client.closed

    assert client.closed


def test_client_methods_callable() -> None:
    """Test that all abstract methods are callable."""
    client = MockSyncClient()

    # Test get_collection
    collection = client.get_collection(limit=10)
    assert isinstance(collection, BaseCollection)
    assert len(collection.assets) == 1

    # Test get_asset
    asset = client.get_asset("test-123")
    assert isinstance(asset, BaseAsset)
    assert asset.uid == "test-123"

    # Test download_asset
    result = client.download_asset("test-123", "/tmp/downloads")
    assert isinstance(result, DownloadResult)
    assert result.success

    # Test close
    client.close()
    assert client.closed


def test_client_abc_cannot_instantiate() -> None:
    """Test that MarketplaceClient ABC cannot be instantiated directly."""
    with pytest.raises(TypeError):
        MarketplaceClient()  # type: ignore[abstract]
