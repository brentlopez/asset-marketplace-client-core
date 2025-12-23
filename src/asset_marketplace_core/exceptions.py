"""Exception hierarchy for asset marketplace operations."""


class MarketplaceError(Exception):
    """Base exception for all marketplace-related errors.
    
    Platform-specific client libraries should inherit from this base
    to create their own exception hierarchies.
    """
    pass


class MarketplaceAuthenticationError(MarketplaceError):
    """Raised when authentication fails or credentials are invalid.
    
    Examples:
        - Invalid or expired authentication tokens
        - Missing required credentials
        - Authentication service unavailable
    """
    pass


class MarketplaceAPIError(MarketplaceError):
    """Raised when the API returns an error response.
    
    Examples:
        - 4xx client errors (bad request, not authorized, etc.)
        - 5xx server errors
        - Unexpected API response format
    """
    pass


class MarketplaceNotFoundError(MarketplaceError):
    """Raised when a requested resource is not found.
    
    Examples:
        - Asset UID does not exist
        - Collection not found
        - Endpoint returns 404
    """
    pass


class MarketplaceNetworkError(MarketplaceError):
    """Raised when a network-level error occurs.
    
    Examples:
        - Connection timeout
        - DNS resolution failure
        - Network unreachable
    """
    pass


class MarketplaceValidationError(MarketplaceError):
    """Raised when input validation fails.
    
    Examples:
        - Invalid asset UID format
        - Invalid file path
        - Missing required parameters
    """
    pass
