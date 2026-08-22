from collections.abc import Sequence
from typing import Any

from ..api.base import BestBuyCore
from ..constants import OPEN_BOX_API


class BestBuyOpenBoxAPI(BestBuyCore):
    """Best Buy Buying Options (Open Box) API wrapper.

    Allows querying for ship-from-store eligible open box products, condition ratings,
    and special pricing across SKUs and categories.
    """

    def _api_name(self) -> str:
        return OPEN_BOX_API

    def search_by_sku(self, sku: int | str, **kwargs: Any) -> Any:
        """Query available Open Box offers for a specific product SKU.

        :param sku: Product SKU identifier.
        """
        payload = {"query": f"products/{sku}/openBox", "params": kwargs}
        return self._call(payload)

    async def asearch_by_sku(self, sku: int | str, **kwargs: Any) -> Any:
        """Async version of search_by_sku."""
        payload = {"query": f"products/{sku}/openBox", "params": kwargs}
        return await self._acall(payload)

    def search_by_skus(self, skus: Sequence[int | str], **kwargs: Any) -> Any:
        """Query available Open Box offers for a list of product SKUs.

        :param skus: Sequence of product SKUs.
        """
        skus_str = ",".join(str(s) for s in skus)
        payload = {"query": f"products/openBox(sku in({skus_str}))", "params": kwargs}
        return self._call(payload)

    async def asearch_by_skus(self, skus: Sequence[int | str], **kwargs: Any) -> Any:
        """Async version of search_by_skus."""
        skus_str = ",".join(str(s) for s in skus)
        payload = {"query": f"products/openBox(sku in({skus_str}))", "params": kwargs}
        return await self._acall(payload)

    def search_by_category(self, category_id: str, **kwargs: Any) -> Any:
        """Query available Open Box offers for products in a specific category.

        :param category_id: Category ID string (e.g. 'abcat0400000').
        """
        payload = {
            "query": f"products/openBox(categoryId={category_id})",
            "params": kwargs,
        }
        return self._call(payload)

    async def asearch_by_category(self, category_id: str, **kwargs: Any) -> Any:
        """Async version of search_by_category."""
        payload = {
            "query": f"products/openBox(categoryId={category_id})",
            "params": kwargs,
        }
        return await self._acall(payload)

    def search(self, query: str | None = None, **kwargs: Any) -> Any:
        """Perform a custom query on the Open Box API or retrieve all offers.

        :param query: Optional query filter expression (e.g. 'customerReviews.averageScore>4').
        """
        if not query:
            full_query = "products/openBox"
        elif query.startswith("products/openBox"):
            full_query = query
        elif query.startswith("(") and query.endswith(")"):
            full_query = f"products/openBox{query}"
        else:
            full_query = f"products/openBox({query})"

        payload = {"query": full_query, "params": kwargs}
        return self._call(payload)

    async def asearch(self, query: str | None = None, **kwargs: Any) -> Any:
        """Async version of search."""
        if not query:
            full_query = "products/openBox"
        elif query.startswith("products/openBox"):
            full_query = query
        elif query.startswith("(") and query.endswith(")"):
            full_query = f"products/openBox{query}"
        else:
            full_query = f"products/openBox({query})"

        payload = {"query": full_query, "params": kwargs}
        return await self._acall(payload)
