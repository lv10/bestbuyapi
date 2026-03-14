from typing import Any

from ..api.base import BestBuyCore
from ..constants import CATEGORY_API


class BestBuyCategoryAPI(BestBuyCore):
    def _api_name(self) -> str:
        return CATEGORY_API

    # =================================
    #   Search
    # =================================

    def search(self, query: str, **kwargs: Any) -> Any:
        """
        Performs a customized search on the BestBuy category API. Query
        parameters should be passed to function in as a string.

        :param query: String with query parameter.
        """
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def asearch(self, query: str, **kwargs: Any) -> Any:
        """Async version of search"""
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)

    def search_by_id(self, category_id: str, **kwargs: Any) -> Any:
        """
        Search the category API by id

        :param category_id: string, with the id of the desired category.
        :param kwargs: dictionary, with request parameters
        """
        payload = {"query": f"id={category_id}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_id(self, category_id: str, **kwargs: Any) -> Any:
        """Async version of search_by_id"""
        payload = {"query": f"id={category_id}", "params": kwargs}
        return await self._acall(payload)

    def search_by_name(self, category: str, **kwargs: Any) -> Any:
        """Search the category API by name
        :params:
            :category (str): string, with the name of the desired category.
            :kwargs (dict): dictionary, with request parameters
        """
        payload = {"query": f"name={category}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_name(self, category: str, **kwargs: Any) -> Any:
        """Async version of search_by_name"""
        payload = {"query": f"name={category}", "params": kwargs}
        return await self._acall(payload)
