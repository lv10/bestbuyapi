from typing import Any


class BestBuyAPIError(Exception):
    """Base exception for all Best Buy API errors."""


class BestBuyValidationError(BestBuyAPIError):
    """Errors related to invalid request parameters or arguments before sending."""


class BestBuyHTTPError(BestBuyAPIError):
    """Errors generated when Best Buy servers respond with an error status code."""

    def __init__(
        self,
        status_code: int,
        message: str = "",
        response: Any | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.response = response
        super().__init__(
            f"HTTP {status_code}: {message}" if message else f"HTTP {status_code}"
        )


class BestBuyAuthenticationError(BestBuyHTTPError):
    """Raised when API key is missing, invalid, or unauthorized (HTTP 401/403)."""


class BestBuyNotFoundError(BestBuyHTTPError):
    """Raised when requested resource is not found (HTTP 404)."""


class BestBuyRateLimitError(BestBuyHTTPError):
    """Raised when API call rate limit or quota is exceeded (HTTP 429)."""


class BestBuyServerError(BestBuyHTTPError):
    """Raised when Best Buy servers encounter an internal error (HTTP 5xx)."""


class BestBuyProductAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a products API call."""


class BestBuyCategoryAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a categories API call."""


class BestBuyBulkAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a bulk API call."""


class BestBuyStoresAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a stores API call."""


class BestBuyRecommendationsAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a recommendations API call."""


class BestBuyOpenBoxAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to an open box API call."""
