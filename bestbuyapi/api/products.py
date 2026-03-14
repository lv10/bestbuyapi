from typing import Any, Union

from ..api.base import BestBuyCore
from ..constants import PRODUCT_API, PRODUCT_DESCRIPTION_TYPES


class BestBuyProductsAPI(BestBuyCore):
    def _api_name(self) -> str:
        return PRODUCT_API

    # =================================
    #   Search by description or SKU
    # =================================

    def search_by_description(
        self, description_type: int, description: str, **kwargs: Any
    ) -> Any:
        """Searches the product API using description parameter
        :params:
            :description_type (int): Integer from 1 to 4 to determine the type
                of description the call is going to use.
                The integers represent:
                    - 1: name
                    - 2: description
                    - 3: shortDescription
                    - 4: longDescription
            :description (str): description's content.
        """
        d_type = PRODUCT_DESCRIPTION_TYPES[description_type]
        payload = {"query": f"{d_type}={description}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_description(
        self, description_type: int, description: str, **kwargs: Any
    ) -> Any:
        """Async version of search_by_description"""
        d_type = PRODUCT_DESCRIPTION_TYPES[description_type]
        payload = {"query": f"{d_type}={description}", "params": kwargs}
        return await self._acall(payload)

    def search_by_sku(self, sku: Union[int, str], **kwargs: Any) -> Any:
        """Search the product API by SKU
        :params:
            :sku (str): SKU number of the desired product.
            :kwargs (dict): request parameters
        """
        payload = {"query": f"sku={sku}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_sku(self, sku: Union[int, str], **kwargs: Any) -> Any:
        """Async version of search_by_sku"""
        payload = {"query": f"sku={sku}", "params": kwargs}
        return await self._acall(payload)

    def search_by_review_criteria(
        self, review_type: int, review: float, **kwargs: Any
    ) -> Any:
        """
        Searches the product API using the Review criteria.

        :param review_type: Integer, with customer review type the API
                            call will use.
                            The integer represent:
                            - 1: "customerReviewAverage"
                            - 2: "customerReviewCount"
        :param review: Float, with the actual value of the review to be
                       criteria to be search for.
        """
        if review_type == 2:
            review = int(review)
        # Using walrus operator if it was useful here, but it's not really.
        # Let's use it for demonstration in a place where it makes sense.
        payload = {"query": f"{review_type}={review}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_review_criteria(
        self, review_type: int, review: float, **kwargs: Any
    ) -> Any:
        """Async version of search_by_review_criteria"""
        if review_type == 2:
            review = int(review)
        payload = {"query": f"{review_type}={review}", "params": kwargs}
        return await self._acall(payload)

    # =================================
    #         Custom Search
    # =================================

    def search(self, query: str, **kwargs: Any) -> Any:
        """Performs a customized search on the BestBuy product API. Query
        parameters should be passed to function in a dictionary.

        :params:
            :query (str): String with query parameter.
        """
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def asearch(self, query: str, **kwargs: Any) -> Any:
        """Async version of search"""
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)
