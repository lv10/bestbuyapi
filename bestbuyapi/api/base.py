import json
import sys
from collections.abc import AsyncIterator, Callable, Iterator
from typing import Any

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import httpx

from ..constants import (
    ALL_VALID_PARAMS,
    BASE_URL,
    BETA_BASE_URL,
    BULK_API,
    OPEN_BOX_API,
    RECOMMENDATIONS_API,
)
from ..utils.exceptions import (
    BestBuyAuthenticationError,
    BestBuyHTTPError,
    BestBuyNotFoundError,
    BestBuyRateLimitError,
    BestBuyServerError,
    BestBuyValidationError,
)

# Default connection limits for high-performance connection pooling
DEFAULT_LIMITS = httpx.Limits(
    max_keepalive_connections=20, max_connections=50, keepalive_expiry=30.0
)
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0)


class BestBuyCore:
    def __init__(
        self,
        api_key: str,
        client: httpx.Client | None = None,
        aclient: httpx.AsyncClient | None = None,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        limits: httpx.Limits = DEFAULT_LIMITS,
    ):
        """API's base class with high-performance connection pooling.

        :params:
            :api_key (str): Best Buy developer API key.
            :client (httpx.Client): optional persistent sync client.
            :aclient (httpx.AsyncClient): optional persistent async client.
            :timeout: request timeout (seconds or httpx.Timeout).
            :limits: connection pool limits.
        """
        self.api_key = api_key.strip()
        self.client = client
        self.aclient = aclient
        self._timeout = timeout
        self._limits = limits

        self._internal_client: httpx.Client | None = None
        self._internal_aclient: httpx.AsyncClient | None = None

    def get_client(self) -> httpx.Client:
        """Returns the active persistent sync client, lazily initializing if needed."""
        if self.client is not None:
            return self.client
        if self._internal_client is None or self._internal_client.is_closed:
            self._internal_client = httpx.Client(
                timeout=self._timeout,
                limits=self._limits,
                headers={"Accept-Encoding": "gzip, deflate"},
            )
        return self._internal_client

    def get_aclient(self) -> httpx.AsyncClient:
        """Returns the active persistent async client, lazily initializing if needed."""
        if self.aclient is not None:
            return self.aclient
        if self._internal_aclient is None or self._internal_aclient.is_closed:
            self._internal_aclient = httpx.AsyncClient(
                timeout=self._timeout,
                limits=self._limits,
                headers={"Accept-Encoding": "gzip, deflate"},
            )
        return self._internal_aclient

    def close(self) -> None:
        """Close the underlying sync HTTP client and connection pool."""
        if self._internal_client and not self._internal_client.is_closed:
            self._internal_client.close()
            self._internal_client = None

    async def aclose(self) -> None:
        """Close the underlying async HTTP client and connection pool."""
        if self._internal_aclient and not self._internal_aclient.is_closed:
            await self._internal_aclient.aclose()
            self._internal_aclient = None

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()

    def _call(self, payload: dict[str, Any]) -> Any:
        """Execute synchronous call to the Best Buy API using connection pool."""
        valid_payload = self._validate_params(payload)
        url, params = self._build_url(valid_payload)
        client = self.get_client()
        response = client.get(url, params=params)
        return self._handle_response(response)

    async def _acall(self, payload: dict[str, Any]) -> Any:
        """Execute asynchronous call to the Best Buy API using connection pool."""
        valid_payload = self._validate_params(payload)
        url, params = self._build_url(valid_payload)
        aclient = self.get_aclient()
        response = await aclient.get(url, params=params)
        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> Any:
        """Parse response and raise granular exceptions on error status codes."""
        if response.status_code >= 400:
            error_message = self._extract_error_message(response)
            if response.status_code in (401, 403):
                raise BestBuyAuthenticationError(
                    response.status_code, message=error_message, response=response
                )
            if response.status_code == 404:
                raise BestBuyNotFoundError(
                    response.status_code, message=error_message, response=response
                )
            if response.status_code == 429:
                raise BestBuyRateLimitError(
                    response.status_code, message=error_message, response=response
                )
            if response.status_code >= 500:
                raise BestBuyServerError(
                    response.status_code, message=error_message, response=response
                )
            raise BestBuyHTTPError(
                response.status_code, message=error_message, response=response
            )

        content_type = response.headers.get("Content-Type", "")
        if "json" in content_type:
            try:
                return response.json()
            except (json.JSONDecodeError, ValueError):
                return response.content
        return response.content

    def _extract_error_message(self, response: httpx.Response) -> str:
        try:
            data = response.json()
            if isinstance(data, dict):
                if "error" in data:
                    err = data["error"]
                    if isinstance(err, dict):
                        return err.get("message") or str(err)
                    return str(err)
                if "message" in data:
                    return str(data["message"])
                if "errors" in data:
                    return str(data["errors"])
        except (json.JSONDecodeError, ValueError):
            return response.text[:200] if response.text else ""
        return response.text[:200] if response.text else ""

    def _api_name(self) -> str | None:
        return None

    def _build_url(self, payload: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        query = payload.get("query", "")
        out = {
            key: (
                ",".join(map(str, value))
                if isinstance(value, (list, tuple, set))
                else value
            )
            for key, value in payload.get("params", {}).items()
        }

        out["apiKey"] = self.api_key
        api = self._api_name()

        if api == BULK_API or api == RECOMMENDATIONS_API:
            url = f"{BASE_URL}{query}"
        elif api == OPEN_BOX_API:
            url = f"{BETA_BASE_URL}{query}"
        else:
            if not query:
                url = f"{BASE_URL}{api}"
            elif query.startswith("(") and query.endswith(")"):
                url = f"{BASE_URL}{api}{query}"
            else:
                url = f"{BASE_URL}{api}({query})"

        return (url, out)

    def _validate_params(self, payload: dict[str, Any]) -> dict[str, Any]:
        for key, value in payload.get("params", {}).items():
            if key not in ALL_VALID_PARAMS:
                err_msg = f"{key} is an invalid Search Parameter"
                raise BestBuyValidationError(err_msg)

            if value is None:
                err_msg = f"Key {key} can't have None for a value"
                raise BestBuyValidationError(err_msg)

        return payload

    def _iter_pages(
        self,
        call_fn: Callable[..., Any],
        query: str = "",
        page_size: int = 10,
        max_pages: int | None = None,
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        """Synchronously iterate over pages of results."""
        page = 1
        while True:
            res = call_fn(query=query, page=page, pageSize=page_size, **kwargs)
            if not isinstance(res, dict):
                yield res
                break
            yield res

            total_pages = res.get("totalPages", 1)
            current_page = res.get("currentPage", page)
            if current_page >= total_pages:
                break
            if max_pages is not None and page >= max_pages:
                break
            page += 1

    async def _aiter_pages(
        self,
        acall_fn: Callable[..., Any],
        query: str = "",
        page_size: int = 10,
        max_pages: int | None = None,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Asynchronously iterate over pages of results."""
        page = 1
        while True:
            res = await acall_fn(query=query, page=page, pageSize=page_size, **kwargs)
            if not isinstance(res, dict):
                yield res
                break
            yield res

            total_pages = res.get("totalPages", 1)
            current_page = res.get("currentPage", page)
            if current_page >= total_pages:
                break
            if max_pages is not None and page >= max_pages:
                break
            page += 1

    def _iter_cursor(
        self,
        call_fn: Callable[..., Any],
        query: str = "",
        page_size: int = 100,
        **kwargs: Any,
    ) -> Iterator[dict[str, Any]]:
        """Synchronously iterate through results using cursor marks."""
        cursor: str = "*"
        while cursor:
            res = call_fn(query=query, cursorMark=cursor, pageSize=page_size, **kwargs)
            if not isinstance(res, dict):
                yield res
                break
            yield res

            next_cursor = res.get("nextCursorMark")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor

    async def _aiter_cursor(
        self,
        acall_fn: Callable[..., Any],
        query: str = "",
        page_size: int = 100,
        **kwargs: Any,
    ) -> AsyncIterator[dict[str, Any]]:
        """Asynchronously iterate through results using cursor marks."""
        cursor: str = "*"
        while cursor:
            res = await acall_fn(
                query=query, cursorMark=cursor, pageSize=page_size, **kwargs
            )
            if not isinstance(res, dict):
                yield res
                break
            yield res

            next_cursor = res.get("nextCursorMark")
            if not next_cursor or next_cursor == cursor:
                break
            cursor = next_cursor
