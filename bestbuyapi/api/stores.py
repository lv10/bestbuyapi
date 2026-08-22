from collections.abc import AsyncIterator, Iterator
from typing import Any

from ..api.base import BestBuyCore
from ..constants import STORES_API


class BestBuyStoresAPI(BestBuyCore):
    """Best Buy Stores API wrapper.

    Provides store lookup by ID, postal code, city, region/state,
    geographic radius (area), and custom queries.
    """

    def _api_name(self) -> str:
        return STORES_API

    # =================================
    #   Search by Store attributes
    # =================================

    def search_by_id(self, store_id: int | str, **kwargs: Any) -> Any:
        """Searches the stores API given a store number.

        :param store_id: Best Buy store identifier (e.g. 281).
        """
        payload = {"query": f"storeId={store_id}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_id(self, store_id: int | str, **kwargs: Any) -> Any:
        """Async version of search_by_id."""
        payload = {"query": f"storeId={store_id}", "params": kwargs}
        return await self._acall(payload)

    def search_by_postal_code(self, postal_code: int | str, **kwargs: Any) -> Any:
        """Searches the stores API given a 5-digit ZIP or postal code.

        :param postal_code: Postal/ZIP code string or integer (e.g. 55423).
        """
        payload = {"query": f"postalCode={postal_code}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_postal_code(
        self, postal_code: int | str, **kwargs: Any
    ) -> Any:
        """Async version of search_by_postal_code."""
        payload = {"query": f"postalCode={postal_code}", "params": kwargs}
        return await self._acall(payload)

    def search_by_city(self, city: str, **kwargs: Any) -> Any:
        """Searches the stores API for stores located in a city.

        :param city: City name (e.g. 'San Juan', 'New York').
        """
        payload = {"query": f"city={city}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_city(self, city: str, **kwargs: Any) -> Any:
        """Async version of search_by_city."""
        payload = {"query": f"city={city}", "params": kwargs}
        return await self._acall(payload)

    def search_by_region(self, region: str, **kwargs: Any) -> Any:
        """Searches the stores API for stores located in a state or territory.

        :param region: Two-letter state/territory abbreviation (e.g. 'MN', 'UT', 'PR').
        """
        payload = {"query": f"region={region}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_region(self, region: str, **kwargs: Any) -> Any:
        """Async version of search_by_region."""
        payload = {"query": f"region={region}", "params": kwargs}
        return await self._acall(payload)

    def search_by_area(
        self, lat: float, lng: float, distance_miles: float, **kwargs: Any
    ) -> Any:
        """Searches the stores API for stores within a geographic radius in miles.

        :param lat: Latitude coordinate (e.g. 44.88476).
        :param lng: Longitude coordinate (e.g. -93.30058).
        :param distance_miles: Distance radius in miles (e.g. 10).
        """
        payload = {
            "query": f"area({lat},{lng},{distance_miles})",
            "params": kwargs,
        }
        return self._call(payload)

    async def asearch_by_area(
        self, lat: float, lng: float, distance_miles: float, **kwargs: Any
    ) -> Any:
        """Async version of search_by_area."""
        payload = {
            "query": f"area({lat},{lng},{distance_miles})",
            "params": kwargs,
        }
        return await self._acall(payload)

    # =================================
    #         Custom Search & All
    # =================================

    def search(self, query: str = "", **kwargs: Any) -> Any:
        """Performs a customized search on the Best Buy stores API.

        :param query: String with search expression.
        """
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def asearch(self, query: str = "", **kwargs: Any) -> Any:
        """Async version of search."""
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)

    def all(self, **kwargs: Any) -> Any:
        """Retrieve all stores (with optional pagination parameters)."""
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
        """Synchronously iterate page-by-page through stores search results."""
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
        """Asynchronously iterate page-by-page through stores search results."""
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
        """Synchronously stream through store results using cursor marks."""
        return self._iter_cursor(
            self.search, query=query, page_size=page_size, **kwargs
        )

    def aiter_cursor(
        self,
        query: str = "",
        page_size: int = 100,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        """Asynchronously stream through store results using cursor marks."""
        return self._aiter_cursor(
            self.asearch, query=query, page_size=page_size, **kwargs
        )
