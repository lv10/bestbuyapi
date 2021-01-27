from .constants import BASE_URL
from .api.stores import BestBuyStoresAPI
from .api.bulk import BestBuyBulkAPI
from .api.products import BestBuyProductsAPI
from .api.categories import BestBuyCategoryAPI


__version__ = "2.0.0"


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
