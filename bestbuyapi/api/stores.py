from typing import Any, Union

from ..api.base import BestBuyCore
from ..constants import STORES_API


class BestBuyStoresAPI(BestBuyCore):
    def _api_name(self) -> str:
        return STORES_API

    # =================================
    #   Search by store by name or id
    # =================================

    def search_by_id(self, store_id: Union[int, str], **kwargs: Any) -> Any:
        """Searches the stores api given an id"""
        payload = {"query": f"storeId={store_id}", "params": kwargs}
        return self._call(payload)

    async def asearch_by_id(self, store_id: Union[int, str], **kwargs: Any) -> Any:
        """Async version of search_by_id"""
        payload = {"query": f"storeId={store_id}", "params": kwargs}
        return await self._acall(payload)
