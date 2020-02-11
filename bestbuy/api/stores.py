from bestbuy.api.base import BestBuyCore
from bestbuy.constants import STORES_API
from bestbuy.utils.exceptions import BestBuyStoresAPIError


class BestBuyStoresAPI(BestBuyCore):

    def _api_name(self):
        return STORES_API

    # =================================
    #   Search by store by name or id
    # =================================

    def search_by_id(self, store_id, **kwargs):
        """Searches the stores api given an id"""
        payload = {"query": f"storeId={store_id}", "params": kwargs}
        return self._call(payload)
