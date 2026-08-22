from collections.abc import AsyncIterator, Iterator
from typing import Any

from ..api.base import BestBuyCore
from ..constants import (
    PRODUCT_API,
    PRODUCT_DESCRIPTION_TYPES,
    PRODUCT_SEARCH_CRITERIA_TYPES,
)
from ..utils.exceptions import BestBuyValidationError


class BestBuyProductsAPI(BestBuyCore):
    def _api_name(self) -> str:
        return PRODUCT_API

    # =================================
    #   Search by description or SKU
    # =================================

    def search_by_description(
        self, description_type: int, description: str, **kwargs: Any
    ) -> Any:
        """Searches the product API using description parameter.

        :params:
            :description_type (int): Integer from 1 to 4 to determine the type
                of description the call is going to use:
                    - 1: name
                    - 2: description
                    - 3: shortDescription
                    - 4: longDescription
            :description (str): description query content.
        """
        if description_type not in PRODUCT_DESCRIPTION_TYPES:
            raise BestBuyValidationError(
                f"Invalid description_type: {description_type}. Must be 1 (name), 2 (description), 3 (shortDescription), or 4 (longDescription)."
            )
        d_type = PRODUCT_DESCRIPTION_TYPES[description_type]
        payload = {"query": f"{d_type}={description}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_description(
        self, description_type: int, description: str, **kwargs: Any
    ) -> Any:
        """Async version of search_by_description."""
        if description_type not in PRODUCT_DESCRIPTION_TYPES:
            raise BestBuyValidationError(
                f"Invalid description_type: {description_type}. Must be 1 (name), 2 (description), 3 (shortDescription), or 4 (longDescription)."
            )
        d_type = PRODUCT_DESCRIPTION_TYPES[description_type]
        payload = {"query": f"{d_type}={description}", "params": kwargs}
        return await self._acall(payload)

    def search_by_sku(self, sku: int | str, **kwargs: Any) -> Any:
        """Search the product API by SKU.

        :params:
            :sku: SKU number of the desired product.
            :kwargs: request parameters.
        """
        payload = {"query": f"sku={sku}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_sku(self, sku: int | str, **kwargs: Any) -> Any:
        """Async version of search_by_sku."""
        payload = {"query": f"sku={sku}", "params": kwargs}
        return await self._acall(payload)

    def search_by_upc(self, upc: int | str, **kwargs: Any) -> Any:
        """Search the product API by UPC barcode.

        :params:
            :upc: UPC identifier.
            :kwargs: request parameters.
        """
        payload = {"query": f"upc={upc}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_upc(self, upc: int | str, **kwargs: Any) -> Any:
        """Async version of search_by_upc."""
        payload = {"query": f"upc={upc}", "params": kwargs}
        return await self._acall(payload)

    def search_by_review_criteria(
        self, review_type: int, review: float, **kwargs: Any
    ) -> Any:
        """Searches the product API using customer review criteria.

        :param review_type: Integer determining criteria type:
                            - 1: customerReviewAverage
                            - 2: customerReviewCount
        :param review: Float or Int review threshold value.
        """
        if review_type not in PRODUCT_SEARCH_CRITERIA_TYPES:
            raise BestBuyValidationError(
                f"Invalid review_type: {review_type}. Must be 1 (customerReviewAverage) or 2 (customerReviewCount)."
            )
        criteria_name = PRODUCT_SEARCH_CRITERIA_TYPES[review_type]
        if review_type == 2:
            review = int(review)
        payload = {"query": f"{criteria_name}={review}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_review_criteria(
        self, review_type: int, review: float, **kwargs: Any
    ) -> Any:
        """Async version of search_by_review_criteria."""
        if review_type not in PRODUCT_SEARCH_CRITERIA_TYPES:
            raise BestBuyValidationError(
                f"Invalid review_type: {review_type}. Must be 1 (customerReviewAverage) or 2 (customerReviewCount)."
            )
        criteria_name = PRODUCT_SEARCH_CRITERIA_TYPES[review_type]
        if review_type == 2:
            review = int(review)
        payload = {"query": f"{criteria_name}={review}", "params": kwargs}
        return await self._acall(payload)

    # =================================
    #         Custom Search
    # =================================

    def search(self, query: str = "", **kwargs: Any) -> Any:
        """Performs a customized search on the Best Buy product API.

        :params:
            :query (str): String with search expression.
            :kwargs: search query parameters.
        """
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def asearch(self, query: str = "", **kwargs: Any) -> Any:
        """Async version of search."""
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)

    def all(self, **kwargs: Any) -> Any:
        """Retrieve all products matching query parameters (with pagination)."""
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
        """Synchronously iterate page-by-page through products search results."""
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
        """Asynchronously iterate page-by-page through products search results."""
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
        """Synchronously stream through results using cursorMark bookmarks."""
        return self._iter_cursor(
            self.search, query=query, page_size=page_size, **kwargs
        )

    def aiter_cursor(
        self,
        query: str = "",
        page_size: int = 100,
        **kwargs: Any,
    ) -> AsyncIterator[Any]:
        """Asynchronously stream through results using cursorMark bookmarks."""
        return self._aiter_cursor(
            self.asearch, query=query, page_size=page_size, **kwargs
        )
