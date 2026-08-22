import zipfile
from io import BytesIO

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


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_bulk_and_subsets():
    api_key = "dummy_key"
    bio = BytesIO()
    with zipfile.ZipFile(bio, "w") as z:
        z.writestr("test.json", b'{"key": "value"}')

    async with AsyncBestBuyAPI(api_key) as bb:
        with respx.mock:
            respx.get(url__regex=r".*categories\.json\.zip.*").mock(
                return_value=httpx.Response(200, content=bio.getvalue())
            )
            respx.get(url__regex=r".*subsets/productsSoftware\.json\.zip.*").mock(
                return_value=httpx.Response(200, content=bio.getvalue())
            )

            res1 = await bb.bulk.aarchive("categories", "json")
            assert "test.json" in res1

            res2 = await bb.bulk.aarchive_subset("productsSoftware", "json")
            assert "test.json" in res2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_iterators():
    api_key = "dummy_key"
    async with AsyncBestBuyAPI(api_key) as bb:
        with respx.mock:
            respx.get(url__regex=r".*products.*").mock(
                side_effect=[
                    httpx.Response(
                        200,
                        json={
                            "products": [{"sku": 1}],
                            "currentPage": 1,
                            "totalPages": 2,
                            "nextCursorMark": "c2",
                        },
                    ),
                    httpx.Response(
                        200,
                        json={
                            "products": [{"sku": 2}],
                            "currentPage": 2,
                            "totalPages": 2,
                            "nextCursorMark": None,
                        },
                    ),
                ]
            )

            pages = []
            async for page in bb.products.aiter_pages(max_pages=2):
                pages.append(page)
            assert len(pages) == 2

            # Test aiter_cursor
            respx.get(url__regex=r".*products.*").mock(
                side_effect=[
                    httpx.Response(
                        200,
                        json={"products": [{"sku": 1}], "nextCursorMark": "c2"},
                    ),
                    httpx.Response(
                        200,
                        json={"products": [{"sku": 2}], "nextCursorMark": None},
                    ),
                ]
            )
            cursor_results = []
            async for page in bb.products.aiter_cursor():
                cursor_results.append(page)
            assert len(cursor_results) == 2
