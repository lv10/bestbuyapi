from typing import Optional

import httpx
from dotenv import load_dotenv

from .api.bulk import BestBuyBulkAPI
from .api.categories import BestBuyCategoryAPI
from .api.products import BestBuyProductsAPI
from .api.stores import BestBuyStoresAPI
from .constants import BASE_URL as BASE_URL

__version__ = "2.1.0"

load_dotenv()


class BestBuyAPI:
    def __init__(
        self,
        api_key: str,
        client: Optional[httpx.Client] = None,
        aclient: Optional[httpx.AsyncClient] = None,
    ):
        """API's base class
        :params:
            :api_key (str): best buy developer API key.
            :client (httpx.Client): optional persistent sync client.
            :aclient (httpx.AsyncClient): optional persistent async client.
        """
        self.api_key = api_key.strip()
        self.client = client
        self.aclient = aclient

        self.bulk = BestBuyBulkAPI(
            self.api_key, client=self.client, aclient=self.aclient
        )
        self.products = BestBuyProductsAPI(
            self.api_key, client=self.client, aclient=self.aclient
        )
        self.category = BestBuyCategoryAPI(
            self.api_key, client=self.client, aclient=self.aclient
        )
        self.stores = BestBuyStoresAPI(
            self.api_key, client=self.client, aclient=self.aclient
        )


class AsyncBestBuyAPI(BestBuyAPI):
    """Convenience class for async use.
    It can be used as an async context manager to automatically manage the aclient.
    """

    async def __aenter__(self):
        if not self.aclient:
            self.aclient = httpx.AsyncClient()
            self.products.aclient = self.aclient
            self.category.aclient = self.aclient
            self.stores.aclient = self.aclient
            self.bulk.aclient = self.aclient
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.aclient:
            await self.aclient.aclose()
            self.aclient = None
            self.products.aclient = None
            self.category.aclient = None
            self.stores.aclient = None
            self.bulk.aclient = None
