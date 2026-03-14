import os
import pytest
import respx
import httpx
from bestbuyapi import BestBuyAPI


@pytest.fixture(scope="session")
def bbapi(request):
    api_key = os.getenv("BESTBUY_API_KEY")

    # If this is an integration test and no API key is provided, skip it
    if not api_key:
        is_integration = any(
            m.name == "integration" for m in request.node.iter_markers()
        )
        if is_integration:
            pytest.skip("BESTBUY_API_KEY not found, skipping integration test")
        else:
            api_key = "dummy_key"

    return BestBuyAPI(api_key)


@pytest.fixture
def mock_bestbuy_api():
    with respx.mock(assert_all_called=False) as respx_mock:
        # Default mock for products (if not overridden by more specific mocks)
        respx_mock.get(url__regex=r".*products.*").mock(
            side_effect=lambda request: httpx.Response(
                200,
                json={
                    "products": [{"sku": 5985609, "name": "iphone 13"}],
                    "total": 1,
                }
                if "json" in request.url.params.get("format", "json")
                else None,
                content=b"<products><product><sku>5985609</sku></product></products>"
                if "json" not in request.url.params.get("format", "json")
                else None,
                headers={
                    "Content-Type": "application/json"
                    if "json" in request.url.params.get("format", "json")
                    else "application/xml"
                },
            )
        )
        # Default mock for categories
        respx_mock.get(url__regex=r".*categories.*").mock(
            return_value=httpx.Response(
                200,
                json={"categories": [{"id": "abcat0101001", "name": "TVs"}]},
                headers={"Content-Type": "application/json"},
            )
        )
        # Default mock for stores
        respx_mock.get(url__regex=r".*stores.*").mock(
            return_value=httpx.Response(
                200,
                json={"stores": [{"storeId": 281, "name": "Richfield"}]},
                headers={"Content-Type": "application/json"},
            )
        )
        yield respx_mock
