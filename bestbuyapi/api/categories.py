from collections.abc import AsyncIterator, Iterator
from typing import Any

from ..api.base import BestBuyCore
from ..constants import CATEGORY_API


class BestBuyCategoryAPI(BestBuyCore):
    """Best Buy Categories API wrapper.

    Provides category search by ID, name, custom query, and pagination iterators.
    """

    def _api_name(self) -> str:
        return CATEGORY_API

    # =================================
    #   Search
    # =================================

    def search(self, query: str = "", **kwargs: Any) -> Any:
        """Performs a customized search on the Best Buy category API.

        :param query: String with search expression.
        """
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def asearch(self, query: str = "", **kwargs: Any) -> Any:
        """Async version of search."""
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)

    def search_by_id(self, category_id: str, **kwargs: Any) -> Any:
        """Search the category API by category ID.

        :param category_id: String with ID of the desired category (e.g. 'cat00000').
        :param kwargs: Request parameters.
        """
        payload = {"query": f"id={category_id}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_id(self, category_id: str, **kwargs: Any) -> Any:
        """Async version of search_by_id."""
        payload = {"query": f"id={category_id}", "params": kwargs}
        return await self._acall(payload)

    def search_by_name(self, category: str, **kwargs: Any) -> Any:
        """Search the category API by category name.

        :param category: String with the name of the desired category.
        :param kwargs: Request parameters.
        """
        payload = {"query": f"name={category}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_name(self, category: str, **kwargs: Any) -> Any:
        """Async version of search_by_name."""
        payload = {"query": f"name={category}", "params": kwargs}
        return await self._acall(payload)

    def all(self, **kwargs: Any) -> Any:
        """Retrieve all categories (with optional pagination parameters)."""
        return self.search(query="", **kwargs)

    async def aall(self, **kwargs: Any) -> Any:
        """Async version of all."""
        return await self.asearch(query="", **kwargs)

    # =================================
    #         Streaming & Pagination
    # =================================

    def iter_pages(
        self,
        query: str = "",
        page_size: int = 10,
        max_pages: int | None = None,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Synchronously iterate page-by-page through category search results."""
        return self._iter_pages(
            self.search, query=query, page_size=page_size, max_pages=max_pages, **kwargs
        )

    def aiter_pages(
        self,
        query: str = "",
        page_size: int = 10,
        max_pages: int | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        """Asynchronously iterate page-by-page through category search results."""
        return self._aiter_pages(
            self.asearch,
            query=query,
            page_size=page_size,
            max_pages=max_pages,
            **kwargs,
        )

    def iter_cursor(
        self,
        query: str = "",
        page_size: int = 100,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Synchronously stream through category results using cursor marks."""
        return self._iter_cursor(
            self.search, query=query, page_size=page_size, **kwargs
        )

    def aiter_cursor(
        self,
        query: str = "",
        page_size: int = 100,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        """Asynchronously stream through category results using cursor marks."""
        return self._aiter_cursor(
            self.asearch, query=query, page_size=page_size, **kwargs
        )
