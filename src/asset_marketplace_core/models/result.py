"""Result models for marketplace operations."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DownloadResult:
    """Result of a download operation.

    Provides structured information about download success or failure,
    including any files downloaded and associated metadata.

    Attributes:
        success: Whether the download completed successfully
        asset_uid: Unique identifier of the asset that was downloaded
        files: List of file paths that were downloaded
        error: Error message if download failed, None if successful
        metadata: Additional platform-specific metadata (file sizes, checksums, etc.)

    Examples:
        >>> # Successful download
        >>> result = DownloadResult(
        ...     success=True,
        ...     asset_uid="12345",
        ...     files=["/downloads/asset.zip"],
        ...     metadata={"size_bytes": 1048576}
        ... )

        >>> # Failed download
        >>> result = DownloadResult(
        ...     success=False,
        ...     asset_uid="12345",
        ...     files=[],
        ...     error="Network timeout"
        ... )
    """

    success: bool
    asset_uid: str
    files: List[str] = field(default_factory=list)
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
