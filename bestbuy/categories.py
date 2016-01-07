from constants import CATEGORY_API
from main import BestBuyAPI, BestBuyAPIError


class BestBuyCategoryAPIError(BestBuyAPIError):
    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyCategoryAPI(BestBuyAPI):

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

        payload = {
            'query': query,
            'params': kwargs
        }

        return self._call(payload)

    def search_by_id(self, category_id, **kwargs):
        """
            Search the category API by id

            :param id: string, with the id of the desired category.
            :param kwargs: dictionary, with request parameters
        """

        payload = {
            'query': "id={0}".format(category_id),
            'params': kwargs
        }

        return self._call(payload)

    def search_by_name(self, category, **kwargs):
        """
            Search the category API by name

            :param name: string, with the name of the desired category.
            :param kwargs: dictionary, with request parameters
        """

        payload = {
            'query': "name={0}".format(category),
            'params': kwargs
        }

        return self._call(payload)
