from main import BestBuyAPI, BestBuyAPIError
from constants import STORES_API


class BestBuyStoresAPIError(BestBuyAPIError):
    """Errors before BestBuy servers respond to a call to the stores API"""

    pass


class BestBuyStoresAPI(BestBuyAPI):
    def _api_name(self):
        return STORES_API

    # =================================
    #   Search by store by name or id
    # =================================

    def search_store(self, **kwargs):
        """Searches the stores api given an id or name"""
        payload = {"params": kwargs, "query": ""}
        return self._call(payload)
