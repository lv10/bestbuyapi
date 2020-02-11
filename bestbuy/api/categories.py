from bestbuy.api.base import BestBuyCore
from bestbuy.constants import CATEGORY_API
from bestbuy.utils.exceptions import BestBuyCategoryAPIError


class BestBuyCategoryAPI(BestBuyCore):
    def _api_name(self):
        return CATEGORY_API

    # =================================
    #   Search by description or SKU
    # =================================

    def search(self, query, **kwargs):
        """
            Performs a customized search on the BestBuy category API. Query
            parameters should be passed to function in as a string.

            :param query: String with query parameter. For examples of query
                          check BestBuy documenation at https://goo.gl/ZH5mnP
        """
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    def search_by_id(self, category_id, **kwargs):
        """
            Search the category API by id

            :param id: string, with the id of the desired category.
            :param kwargs: dictionary, with request parameters
        """

        payload = {"query": f"id={category_id}", "params": kwargs}

        return self._call(payload)

    def search_by_name(self, category, **kwargs):
        """Search the category API by name
        :params:
            :name (str): string, with the name of the desired category.
            :kwargs (dict): dictionary, with request parameters
        """
        payload = {"query": "name={0}".format(category), "params": kwargs}
        return self._call(payload)
