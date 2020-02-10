from bestbuy.api import BestBuyAPI, BestBuyAPIError
from bestbuy.constants import STORES_API


class BestBuyStoresAPIError(BestBuyAPIError):
    """Errors before BestBuy servers respond to a call to the stores API"""

    pass


class BestBuyStoresAPI(BestBuyAPI):

    def _api_name(self):
        return STORES_API

    # =================================
    #   Search by store by name or id
    # =================================

    def search_by_id(self, store_id, **kwargs):
        """Searches the stores api given an id"""
        payload = {"query": f"storeId={store_id}", "params": kwargs}
        return self._call(payload)
