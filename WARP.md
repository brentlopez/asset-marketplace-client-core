# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **platform-agnostic Python library** providing base abstractions for asset marketplace API clients. It defines interfaces and base classes that are extended by platform-specific implementations (e.g., Fab.com, Unity Asset Store, Unreal Marketplace clients).

**Critical Design Principle:** This library has **zero runtime dependencies** (stdlib only). Do not add any runtime dependencies. Dev dependencies are acceptable.

## Development Commands

### Setup
```bash
pip install -e ".[dev]"
```

### Type Checking
```bash
mypy src/
```
This project uses **mypy strict mode**. All code must have complete type annotations.

### Linting & Formatting
```bash
# Format code
black src/

# Lint code
ruff check src/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=asset_marketplace_core --cov-report=term-missing

# Note: Tests directory doesn't exist yet - create tests/ when adding tests
```

## Architecture

### Core Abstractions

The library provides three main abstract base classes that platform-specific clients must implement:

1. **`MarketplaceClient` (src/asset_marketplace_core/client.py)**
   - Abstract base for platform-specific API clients
   - Required methods: `get_collection()`, `get_asset()`, `download_asset()`, `close()`
   - Supports context manager protocol for resource cleanup

2. **`AuthProvider` (src/asset_marketplace_core/auth.py)**
   - Abstract base for authentication mechanisms
   - Required methods: `get_session()`, `get_endpoints()`
   - Optional methods: `refresh()`, `close()`
   - Returns type `Any` for session to avoid HTTP library dependencies

3. **`EndpointConfig` (src/asset_marketplace_core/auth.py)**
   - Base dataclass for API endpoint configuration
   - Contains `base_url` field
   - Platform implementations extend this with their specific endpoints

### Data Models (src/asset_marketplace_core/models/)

- **`BaseAsset`** - Core asset representation with uid, title, description, timestamps, and raw_data dict
- **`BaseCollection`** - Container for assets with filtering and search capabilities
- **`ProgressCallback`** - Abstract base for download progress reporting
- **`DownloadResult`** - Standard result structure for download operations

### Exception Hierarchy (src/asset_marketplace_core/exceptions.py)

All exceptions inherit from `MarketplaceError`:
- `MarketplaceAuthenticationError` - Auth failures
- `MarketplaceAPIError` - API errors
- `MarketplaceNotFoundError` - Resource not found
- `MarketplaceNetworkError` - Network issues
- `MarketplaceValidationError` - Input validation failures

### Utilities (src/asset_marketplace_core/utils.py)

Provides cross-platform file and URL utilities:
- `sanitize_filename()` - Safe filename sanitization
- `validate_url()` - URL validation
- `safe_create_directory()` - Safe directory creation
- `format_bytes()` - Human-readable byte formatting

## Design Patterns

### Extension Pattern
This library uses the **Abstract Base Class (ABC) pattern**. Platform implementations:
1. Extend base classes (e.g., `class FabClient(MarketplaceClient)`)
2. Implement all abstract methods
3. Add platform-specific fields and methods to models by extending `BaseAsset` and `BaseCollection`
4. Store original API responses in the `raw_data` dict on `BaseAsset` for extensibility

### Type Safety
- All code must pass `mypy` in strict mode
- Use proper type hints on all functions and methods
- Avoid `Any` types except for `AuthProvider.get_session()` (intentionally generic to avoid HTTP library dependencies)

### Zero Dependencies Philosophy
- **Never add runtime dependencies** - this is a core design principle
- Platform implementations choose their own HTTP libraries and dependencies
- Dev dependencies (pytest, mypy, black, ruff) are acceptable in `[project.optional-dependencies]`

## Key Implementation Notes

### When Adding New Abstract Methods
- Add to the appropriate ABC (MarketplaceClient, AuthProvider, etc.)
- Update docstrings with clear parameter and return type documentation
- Document all expected exceptions
- Update `__all__` in `src/asset_marketplace_core/__init__.py`

### When Adding New Data Models
- Use `@dataclass` decorator
- Inherit from appropriate base class when applicable
- Add `raw_data: Dict[str, Any] = field(default_factory=dict)` for API response storage
- Include type hints for all fields
- Add helper methods for common operations

### When Adding Utilities
- Keep utilities platform-agnostic and stdlib-only
- Add comprehensive docstrings
- Export in `__all__` list in `__init__.py`

## Python Version Support

- Minimum: Python 3.7+
- Target versions in pyproject.toml: 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- Use features compatible with Python 3.7 (avoid walrus operator, pattern matching, etc.)

## Related Projects

- **asset-marketplace-client-system** (https://github.com/brentlopez/asset-marketplace-client-system) - System architecture and design documentation
- Platform-specific implementations extend this core library (e.g., fab-api-client, unity-asset-store-client)

## Important Documentation

- `docs/platform_client_guide.md` - Complete guide for building platform-specific clients
- `docs/async_api_plan.md` - Future async/await support roadmap
- README.md - Public API documentation with examples
