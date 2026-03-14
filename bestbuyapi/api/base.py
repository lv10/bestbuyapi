from typing import Any, Dict, Optional, Tuple

import httpx

from ..constants import ALL_VALID_PARAMS, BASE_URL, BULK_API
from ..utils.exceptions import BestBuyAPIError


class BestBuyCore:
    def __init__(
        self,
        api_key: str,
        client: Optional[httpx.Client] = None,
        aclient: Optional[httpx.AsyncClient] = None,
    ):
        """API's base class
        :params:
        :api_key (str): best buy developer API key.
        :client (httpx.Client): optional persistent sync client.
        :aclient (httpx.AsyncClient): optional persistent async client.
        """
        self.api_key = api_key.strip()
        self.client = client
        self.aclient = aclient

    def _call(self, payload: Dict[str, Any]) -> Any:
        """
        Actual call to the Best Buy API.
        """
        valid_payload = self._validate_params(payload)
        url, params = self._build_url(valid_payload)

        if self.client:
            response = self.client.get(url, params=params)
            return self._handle_response(response)

        with httpx.Client() as client:
            response = client.get(url, params=params)
            return self._handle_response(response)

    async def _acall(self, payload: Dict[str, Any]) -> Any:
        """
        Async call to the Best Buy API.
        """
        valid_payload = self._validate_params(payload)
        url, params = self._build_url(valid_payload)

        if self.aclient:
            response = await self.aclient.get(url, params=params)
            return self._handle_response(response)

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> Any:
        if "json" in response.headers.get("Content-Type", ""):
            return response.json()
        return response.content

    def _api_name(self) -> Optional[str]:
        return None

    def _build_url(self, payload: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        query = payload["query"]
        out = {
            key: (",".join(value) if isinstance(value, list) else value)
            for key, value in payload["params"].items()
        }

        out["apiKey"] = self.api_key
        if self._api_name() == BULK_API:
            url = f"{BASE_URL}{query}"
        else:
            url = f"{BASE_URL}{self._api_name()}({query})"

        return (url, out)

    def _validate_params(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in payload["params"].items():
            if key not in ALL_VALID_PARAMS:
                err_msg = f"{key} is an invalid Search Parameter"
                raise BestBuyAPIError(err_msg)

            if value is None:
                err_msg = f"Key {key} can't have None for a value"
                raise BestBuyAPIError(err_msg)

        return payload
