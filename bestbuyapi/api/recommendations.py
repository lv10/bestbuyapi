from typing import Any

from ..api.base import BestBuyCore
from ..constants import RECOMMENDATIONS_API


class BestBuyRecommendationsAPI(BestBuyCore):
    """Best Buy Recommendations API wrapper.

    Provides trending, most viewed, also viewed, also bought,
    and viewed-ultimately-bought recommendations based on customer behavior.
    """

    def _api_name(self) -> str:
        return RECOMMENDATIONS_API

    def also_bought(self, sku: int | str, **kwargs: Any) -> Any:
        """Get products that customers frequently bought after purchasing the specified product.

        :param sku: Product SKU identifier.
        """
        payload = {"query": f"products/{sku}/alsoBought", "params": kwargs}
        return self._call(payload)

    async def aalso_bought(self, sku: int | str, **kwargs: Any) -> Any:
        """Async version of also_bought."""
        payload = {"query": f"products/{sku}/alsoBought", "params": kwargs}
        return await self._acall(payload)

    def also_viewed(self, sku: int | str, **kwargs: Any) -> Any:
        """Get products that customers frequently viewed after viewing the specified product.

        :param sku: Product SKU identifier.
        """
        payload = {"query": f"products/{sku}/alsoViewed", "params": kwargs}
        return self._call(payload)

    async def aalso_viewed(self, sku: int | str, **kwargs: Any) -> Any:
        """Async version of also_viewed."""
        payload = {"query": f"products/{sku}/alsoViewed", "params": kwargs}
        return await self._acall(payload)

    def trending(self, category_id: str | None = None, **kwargs: Any) -> Any:
        """Get top trending products currently being viewed across Best Buy or in a category.

        :param category_id: Optional Best Buy category ID (e.g. 'abcat0400000').
        """
        query = (
            f"products/trendingViewed(categoryId={category_id})"
            if category_id
            else "products/trendingViewed"
        )
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def atrending(self, category_id: str | None = None, **kwargs: Any) -> Any:
        """Async version of trending."""
        query = (
            f"products/trendingViewed(categoryId={category_id})"
            if category_id
            else "products/trendingViewed"
        )
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)

    def most_viewed(self, category_id: str | None = None, **kwargs: Any) -> Any:
        """Get most viewed / popular products overall or for a specific category.

        :param category_id: Optional Best Buy category ID (e.g. 'abcat0107000').
        """
        query = (
            f"products/mostViewed(categoryId={category_id})"
            if category_id
            else "products/mostViewed"
        )
        payload = {"query": query, "params": kwargs}
        return self._call(payload)

    async def amost_viewed(self, category_id: str | None = None, **kwargs: Any) -> Any:
        """Async version of most_viewed."""
        query = (
            f"products/mostViewed(categoryId={category_id})"
            if category_id
            else "products/mostViewed"
        )
        payload = {"query": query, "params": kwargs}
        return await self._acall(payload)

    def viewed_ultimately_bought(self, sku: int | str, **kwargs: Any) -> Any:
        """Get products customers ultimately purchased after viewing the specified SKU.

        :param sku: Product SKU identifier.
        """
        payload = {"query": f"products/{sku}/viewedUltimatelyBought", "params": kwargs}
        return self._call(payload)

    async def aviewed_ultimately_bought(self, sku: int | str, **kwargs: Any) -> Any:
        """Async version of viewed_ultimately_bought."""
        payload = {"query": f"products/{sku}/viewedUltimatelyBought", "params": kwargs}
        return await self._acall(payload)
