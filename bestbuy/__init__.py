from bestbuy.constants import BASE_URL
from bestbuy.api.stores import BestBuyStoresAPI
from bestbuy.api.bulk import BestBuyBulkAPI
from bestbuy.api.products import BestBuyProductsAPI
from bestbuy.api.categories import BestBuyCategoryAPI
from bestbuy.utils.exceptions import (
    BestBuyBulkAPIError,
    BestBuyBulkAPIError,
    BestBuyProductAPIError,
    BestBuyCategoryAPIError,
)


__version__ = "1.0.0"


class BestBuyAPI:

  def __init__(self, api_key):
        """API's base class
        :params:
            :api_key (str): best buy developer API key.
        """
        self.api_key = api_key.strip()
        self.bulk = BestBuyBulkAPI(self.api_key)
        self.products = BestBuyProductsAPI(self.api_key)
        self.category = BestBuyCategoryAPI(self.api_key)
        self.stores = BestBuyStoresAPI(self.api_key)
