import httpx
import pytest
import respx
from bestbuyapi import AsyncBestBuyAPI


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_search_by_sku():
    api_key = "dummy_key"
    sku = 12345
    mock_response = {"products": [{"sku": sku, "name": "Dummy Product"}]}

    async with AsyncBestBuyAPI(api_key) as bb:
        with respx.mock:
            respx.get(f"https://api.bestbuy.com/v1/products(sku={sku})").mock(
                return_value=httpx.Response(200, json=mock_response)
            )

            response = await bb.products.asearch_by_sku(sku)
            assert response == mock_response
            assert response["products"][0]["sku"] == sku


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_search_by_description():
    api_key = "dummy_key"
    description = "iphone*"
    mock_response = {"products": [{"name": "iPhone 13"}]}

    async with AsyncBestBuyAPI(api_key) as bb:
        with respx.mock:
            respx.get(f"https://api.bestbuy.com/v1/products(name={description})").mock(
                return_value=httpx.Response(200, json=mock_response)
            )

            response = await bb.products.asearch_by_description(1, description)
            assert response == mock_response
            assert "iphone" in response["products"][0]["name"].lower()
