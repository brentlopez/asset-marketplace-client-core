"""Tests for data models."""

from datetime import datetime

import pytest

from asset_marketplace_core import BaseAsset, BaseCollection, DownloadResult


def test_base_asset_creation() -> None:
    """Test BaseAsset can be created."""
    asset = BaseAsset(uid="test-123", title="Test Asset")
    assert asset.uid == "test-123"
    assert asset.title == "Test Asset"
    assert asset.description is None
    assert asset.raw_data == {}


def test_base_asset_with_all_fields() -> None:
    """Test BaseAsset with all optional fields."""
    now = datetime.now()
    asset = BaseAsset(
        uid="test-123",
        title="Test Asset",
        description="A test asset",
        created_at=now,
        updated_at=now,
        raw_data={"extra": "data"},
    )
    assert asset.description == "A test asset"
    assert asset.created_at == now
    assert asset.updated_at == now
    assert asset.raw_data == {"extra": "data"}


def test_base_collection_empty() -> None:
    """Test empty BaseCollection."""
    collection = BaseCollection()
    assert len(collection) == 0
    assert collection.assets == []
    assert collection.total_count is None


def test_base_collection_with_assets() -> None:
    """Test BaseCollection with assets."""
    assets = [
        BaseAsset(uid="1", title="Asset 1"),
        BaseAsset(uid="2", title="Asset 2"),
    ]
    collection = BaseCollection(assets=assets, total_count=2)
    assert len(collection) == 2
    assert collection.total_count == 2


def test_base_collection_filter() -> None:
    """Test BaseCollection filter method."""
    assets = [
        BaseAsset(uid="1", title="Python Asset"),
        BaseAsset(uid="2", title="Java Asset"),
        BaseAsset(uid="3", title="Python Tool"),
    ]
    collection = BaseCollection(assets=assets)

    filtered = collection.filter(lambda a: "Python" in a.title)
    assert len(filtered) == 2
    assert all("Python" in a.title for a in filtered.assets)


def test_base_collection_find_by_uid() -> None:
    """Test BaseCollection find_by_uid method."""
    assets = [
        BaseAsset(uid="1", title="Asset 1"),
        BaseAsset(uid="2", title="Asset 2"),
    ]
    collection = BaseCollection(assets=assets)

    found = collection.find_by_uid("2")
    assert found is not None
    assert found.title == "Asset 2"

    not_found = collection.find_by_uid("999")
    assert not_found is None


def test_download_result_success() -> None:
    """Test successful DownloadResult."""
    result = DownloadResult(
        success=True,
        asset_uid="test-123",
        files=["/tmp/file1.zip", "/tmp/file2.zip"],
        metadata={"size": 1024},
    )
    assert result.success
    assert result.asset_uid == "test-123"
    assert len(result.files) == 2
    assert result.error is None
    assert result.metadata["size"] == 1024


def test_download_result_failure() -> None:
    """Test failed DownloadResult."""
    result = DownloadResult(
        success=False, asset_uid="test-123", error="Network timeout"
    )
    assert not result.success
    assert result.error == "Network timeout"
    assert result.files == []
