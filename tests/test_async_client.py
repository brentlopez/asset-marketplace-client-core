"""Tests for asynchronous AsyncMarketplaceClient ABC."""

from pathlib import Path

import pytest

from asset_marketplace_core import (
    AsyncMarketplaceClient,
    AsyncProgressCallback,
    BaseAsset,
    BaseCollection,
    DownloadResult,
)


class MockAsyncClient(AsyncMarketplaceClient):
    """Mock async implementation for testing."""

    def __init__(self) -> None:
        self.closed = False

    async def get_collection(self, **kwargs) -> BaseCollection:  # type: ignore[no-untyped-def]
        return BaseCollection(
            assets=[BaseAsset(uid="async-1", title="Async Test Asset")], total_count=1
        )

    async def get_asset(self, asset_uid: str) -> BaseAsset:
        return BaseAsset(uid=asset_uid, title=f"Async Asset {asset_uid}")

    async def download_asset(
        self,
        asset_uid: str,
        output_dir: str | Path,
        progress_callback: AsyncProgressCallback | None = None,
        **kwargs,  # type: ignore[no-untyped-def]
    ) -> DownloadResult:
        return DownloadResult(success=True, asset_uid=asset_uid, files=[])

    async def close(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_async_client_context_manager() -> None:
    """Test that async client works as async context manager."""
    client = MockAsyncClient()
    assert not client.closed

    async with client as ctx_client:
        assert ctx_client is client
        assert not client.closed

    assert client.closed


@pytest.mark.asyncio
async def test_async_client_methods_callable() -> None:
    """Test that all async abstract methods are callable."""
    client = MockAsyncClient()

    # Test get_collection
    collection = await client.get_collection(limit=10)
    assert isinstance(collection, BaseCollection)
    assert len(collection.assets) == 1
    assert collection.assets[0].uid == "async-1"

    # Test get_asset
    asset = await client.get_asset("async-123")
    assert isinstance(asset, BaseAsset)
    assert asset.uid == "async-123"

    # Test download_asset
    result = await client.download_asset("async-123", "/tmp/downloads")
    assert isinstance(result, DownloadResult)
    assert result.success

    # Test close
    await client.close()
    assert client.closed


def test_async_client_abc_cannot_instantiate() -> None:
    """Test that AsyncMarketplaceClient ABC cannot be instantiated directly."""
    with pytest.raises(TypeError):
        AsyncMarketplaceClient()  # type: ignore[abstract]
