# Changelog

All notable changes to asset-marketplace-client-core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-12-25

### Added
- **Async/await support**: New `AsyncMarketplaceClient`, `AsyncAuthProvider`, and `AsyncProgressCallback` abstract base classes for building high-performance asynchronous marketplace clients
- Comprehensive test suite with 30+ tests covering sync/async functionality, backward compatibility, models, and utilities
- `pytest-asyncio` for async test support

### Changed
- **Code reorganization** (backward compatible): Moved sync implementations into subdirectories (`client/sync.py`, `auth/sync.py`, `models/sync_progress.py`) while maintaining all existing imports
- Renamed `models/progress.py` to `models/sync_progress.py` to distinguish from async version
- Updated README.md with async/await examples and updated key features list

### Fixed
- Import paths updated to use relative imports correctly after reorganization

### Technical
- All tests pass (30/30)
- mypy strict mode compliance maintained
- ruff linting passes with Python 3.7+ compatibility preserved
- Zero runtime dependencies maintained (stdlib only)

### Documentation
- Added async quick start example to README.md
- Updated key features to highlight async/await support
- Created comprehensive test suite serving as usage examples

## [0.1.0] - 2024-12-22

### Added
- Initial release with sync-only abstractions
- `MarketplaceClient` abstract base class
- `AuthProvider` abstract base class
- `EndpointConfig` dataclass for API endpoints
- `BaseAsset` and `BaseCollection` data models
- `ProgressCallback` for download progress reporting
- `DownloadResult` for download operation results
- Exception hierarchy (`MarketplaceError` and subclasses)
- Utility functions: `sanitize_filename`, `validate_url`, `safe_create_directory`, `format_bytes`
- Full type hints and mypy strict mode support
- Zero runtime dependencies (stdlib only)
- Python 3.7+ compatibility
- Context manager protocol support
- Comprehensive documentation

[0.2.0]: https://github.com/brentlopez/asset-marketplace-client-core/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/brentlopez/asset-marketplace-client-core/releases/tag/v0.1.0
