import os
import sys

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import httpx
from dotenv import load_dotenv

from .api.bulk import BestBuyBulkAPI
from .api.categories import BestBuyCategoryAPI
from .api.openbox import BestBuyOpenBoxAPI
from .api.products import BestBuyProductsAPI
from .api.recommendations import BestBuyRecommendationsAPI
from .api.stores import BestBuyStoresAPI
from .constants import (
    API_VERSION as API_VERSION,
)
from .constants import (
    BASE_URL as BASE_URL,
)
from .constants import (
    BETA_BASE_URL as BETA_BASE_URL,
)
from .utils.exceptions import (
    BestBuyAPIError as BestBuyAPIError,
)
from .utils.exceptions import (
    BestBuyAuthenticationError as BestBuyAuthenticationError,
)
from .utils.exceptions import (
    BestBuyBulkAPIError as BestBuyBulkAPIError,
)
from .utils.exceptions import (
    BestBuyCategoryAPIError as BestBuyCategoryAPIError,
)
from .utils.exceptions import (
    BestBuyHTTPError as BestBuyHTTPError,
)
from .utils.exceptions import (
    BestBuyNotFoundError as BestBuyNotFoundError,
)
from .utils.exceptions import (
    BestBuyOpenBoxAPIError as BestBuyOpenBoxAPIError,
)
from .utils.exceptions import (
    BestBuyProductAPIError as BestBuyProductAPIError,
)
from .utils.exceptions import (
    BestBuyRateLimitError as BestBuyRateLimitError,
)
from .utils.exceptions import (
    BestBuyRecommendationsAPIError as BestBuyRecommendationsAPIError,
)
from .utils.exceptions import (
    BestBuyServerError as BestBuyServerError,
)
from .utils.exceptions import (
    BestBuyStoresAPIError as BestBuyStoresAPIError,
)
from .utils.exceptions import (
    BestBuyValidationError as BestBuyValidationError,
)

__version__ = "2.2.0"

load_dotenv()


class BestBuyAPI:
    """Best Buy Developer REST API Client.

    Supports both synchronous and asynchronous operations with connection pooling,
    context management, and full coverage of Best Buy API endpoints.
    """

    def __init__(
        self,
        api_key: str | None = None,
        client: httpx.Client | None = None,
        aclient: httpx.AsyncClient | None = None,
        timeout: float | httpx.Timeout = 30.0,
    ):
        """Initialize the Best Buy API Client.

        :params:
            :api_key (str, optional): Best Buy developer API key. If not provided,
                it is read from the `BESTBUY_API_KEY` environment variable.
            :client (httpx.Client, optional): Persistent sync client.
            :aclient (httpx.AsyncClient, optional): Persistent async client.
            :timeout (float or httpx.Timeout, optional): Request timeout (default 30.0s).
        """
        resolved_key = api_key or os.getenv("BESTBUY_API_KEY")
        if not resolved_key:
            raise BestBuyAuthenticationError(
                401,
                "API key is required. Pass api_key or set the BESTBUY_API_KEY environment variable.",
            )

        self.api_key = resolved_key.strip()
        self.client = client
        self.aclient = aclient
        self.timeout = timeout

        # Sub-APIs
        self.products = BestBuyProductsAPI(
            self.api_key, client=self.client, aclient=self.aclient, timeout=self.timeout
        )
        self.category = BestBuyCategoryAPI(
            self.api_key, client=self.client, aclient=self.aclient, timeout=self.timeout
        )
        self.categories = self.category  # Ergonomic alias

        self.stores = BestBuyStoresAPI(
            self.api_key, client=self.client, aclient=self.aclient, timeout=self.timeout
        )
        self.bulk = BestBuyBulkAPI(
            self.api_key, client=self.client, aclient=self.aclient, timeout=self.timeout
        )
        self.recommendations = BestBuyRecommendationsAPI(
            self.api_key, client=self.client, aclient=self.aclient, timeout=self.timeout
        )
        self.open_box = BestBuyOpenBoxAPI(
            self.api_key, client=self.client, aclient=self.aclient, timeout=self.timeout
        )
        self.buying_options = self.open_box  # Ergonomic alias

        self._all_submodules = [
            self.products,
            self.category,
            self.stores,
            self.bulk,
            self.recommendations,
            self.open_box,
        ]

    def get_client(self) -> httpx.Client:
        """Returns the active persistent sync client."""
        return self.products.get_client()

    def get_aclient(self) -> httpx.AsyncClient:
        """Returns the active persistent async client."""
        return self.products.get_aclient()

    def close(self) -> None:
        """Close all persistent sync HTTP clients."""
        for sub in self._all_submodules:
            sub.close()

    async def aclose(self) -> None:
        """Close all persistent async HTTP clients."""
        for sub in self._all_submodules:
            await sub.aclose()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()


class AsyncBestBuyAPI(BestBuyAPI):
    """Convenience class for async-first usage.

    Can be used as an async context manager to automatically manage shared async clients.
    """

    async def __aenter__(self) -> Self:
        if not self.aclient:
            self.aclient = httpx.AsyncClient(timeout=self.timeout)
            for sub in self._all_submodules:
                sub.aclient = self.aclient
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.aclient:
            await self.aclient.aclose()
            self.aclient = None
            for sub in self._all_submodules:
                sub.aclient = None
        await self.aclose()


__all__ = [
    "API_VERSION",
    "BASE_URL",
    "BETA_BASE_URL",
    "AsyncBestBuyAPI",
    "BestBuyAPI",
    "BestBuyAPIError",
    "BestBuyAuthenticationError",
    "BestBuyBulkAPI",
    "BestBuyBulkAPIError",
    "BestBuyCategoryAPI",
    "BestBuyCategoryAPIError",
    "BestBuyHTTPError",
    "BestBuyNotFoundError",
    "BestBuyOpenBoxAPI",
    "BestBuyOpenBoxAPIError",
    "BestBuyProductAPIError",
    "BestBuyProductsAPI",
    "BestBuyRateLimitError",
    "BestBuyRecommendationsAPI",
    "BestBuyRecommendationsAPIError",
    "BestBuyServerError",
    "BestBuyStoresAPI",
    "BestBuyStoresAPIError",
    "BestBuyValidationError",
]
