import httpx
import pytest

from bestbuyapi import BASE_URL

api_name = "categories"


@pytest.mark.unit
def test_build_url(bbapi):
    sample_url = f"{BASE_URL}{api_name}(sku=43900)"
    payload = {"query": "sku=43900", "params": {"format": "json"}}
    url, thePayload = bbapi.category._build_url(payload)
    assert sample_url == url, "Sample url is different built url"
    assert thePayload["format"] == "json", "Response format isn't JSON"
    assert thePayload.get("apiKey") is not None, "Response doesn't have API Key"


@pytest.mark.unit
def test_search_category_by_id(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    cat_id = "cat00000"
    mock_bestbuy_api.get(url__regex=r".*categories\(id=cat00000\).*").mock(
        return_value=httpx.Response(200, json={"categories": [{"id": cat_id}]})
    )
    resp = bbapi.category.search_by_id(category_id=cat_id, format="json")
    assert resp["categories"][0]["id"] == cat_id, "Returned category id is different"


@pytest.mark.unit
def test_search_category_by_name(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    cat_name = "Sony"
    mock_bestbuy_api.get(url__regex=r".*categories\(name=Sony\).*").mock(
        return_value=httpx.Response(200, json={"categories": [{"name": cat_name}]})
    )
    resp = bbapi.category.search_by_name(category=cat_name, format="json")
    assert resp["categories"][0]["name"] == cat_name, (
        "Response category name is different"
    )


@pytest.mark.unit
def test_categories_alias_and_all(bbapi, mock_bestbuy_api):
    assert bbapi.categories is bbapi.category
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*categories.*").mock(
        return_value=httpx.Response(200, json={"categories": [{"id": "cat1"}]})
    )
    resp = bbapi.categories.all(format="json")
    assert len(resp["categories"]) == 1


@pytest.mark.unit
def test_categories_iterators(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*categories.*").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "categories": [{"id": "c1"}],
                    "currentPage": 1,
                    "totalPages": 2,
                    "nextCursorMark": "c2",
                },
            ),
            httpx.Response(
                200,
                json={
                    "categories": [{"id": "c2"}],
                    "currentPage": 2,
                    "totalPages": 2,
                    "nextCursorMark": None,
                },
            ),
        ]
    )
    pages = list(bbapi.category.iter_pages(max_pages=2))
    assert len(pages) == 2

    # Reset mock for iter_cursor
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*categories.*").mock(
        side_effect=[
            httpx.Response(
                200, json={"categories": [{"id": "c1"}], "nextCursorMark": "c2"}
            ),
            httpx.Response(
                200, json={"categories": [{"id": "c2"}], "nextCursorMark": None}
            ),
        ]
    )
    cursor_results = list(bbapi.category.iter_cursor())
    assert len(cursor_results) == 2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_categories(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*categories.*").mock(
        return_value=httpx.Response(
            200, json={"categories": [{"id": "cat00000", "name": "TVs"}]}
        )
    )
    assert (await bbapi.category.asearch_by_id("cat00000", format="json"))[
        "categories"
    ][0]["id"] == "cat00000"
    assert (await bbapi.category.asearch_by_name("TVs", format="json"))["categories"][
        0
    ]["name"] == "TVs"
    assert (await bbapi.category.aall(format="json"))["categories"][0][
        "id"
    ] == "cat00000"

    # Test aiter_pages and aiter_cursor
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*categories.*").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "categories": [{"id": "c1"}],
                    "currentPage": 1,
                    "totalPages": 2,
                    "nextCursorMark": "c2",
                },
            ),
            httpx.Response(
                200,
                json={
                    "categories": [{"id": "c2"}],
                    "currentPage": 2,
                    "totalPages": 2,
                    "nextCursorMark": None,
                },
            ),
        ]
    )
    async_pages = [p async for p in bbapi.category.aiter_pages(max_pages=2)]
    assert len(async_pages) == 2

    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*categories.*").mock(
        side_effect=[
            httpx.Response(
                200, json={"categories": [{"id": "c1"}], "nextCursorMark": "c2"}
            ),
            httpx.Response(
                200, json={"categories": [{"id": "c2"}], "nextCursorMark": None}
            ),
        ]
    )
    async_cursors = [p async for p in bbapi.category.aiter_cursor()]
    assert len(async_cursors) == 2
