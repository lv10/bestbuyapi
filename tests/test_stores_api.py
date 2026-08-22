import httpx
import pytest


@pytest.mark.unit
def test_search_by_id(bbapi, mock_bestbuy_api):
    store_id = 281
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores\(storeId=281\).*").mock(
        return_value=httpx.Response(200, json={"stores": [{"storeId": store_id}]})
    )
    response = bbapi.stores.search_by_id(store_id=store_id, format="json")
    assert store_id == response["stores"][0]["storeId"]


@pytest.mark.unit
def test_search_by_postal_code(bbapi, mock_bestbuy_api):
    postal_code = 55423
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores\(postalCode=55423\).*").mock(
        return_value=httpx.Response(200, json={"stores": [{"postalCode": "55423"}]})
    )
    response = bbapi.stores.search_by_postal_code(
        postal_code=postal_code, format="json"
    )
    assert response["stores"][0]["postalCode"] == "55423"


@pytest.mark.unit
def test_search_by_city(bbapi, mock_bestbuy_api):
    city = "Richfield"
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores\(city=Richfield\).*").mock(
        return_value=httpx.Response(200, json={"stores": [{"city": city}]})
    )
    response = bbapi.stores.search_by_city(city=city, format="json")
    assert response["stores"][0]["city"] == city


@pytest.mark.unit
def test_search_by_region(bbapi, mock_bestbuy_api):
    region = "UT"
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores\(region=UT\).*").mock(
        return_value=httpx.Response(200, json={"stores": [{"region": region}]})
    )
    response = bbapi.stores.search_by_region(region=region, format="json")
    assert response["stores"][0]["region"] == region


@pytest.mark.unit
def test_search_by_area(bbapi, mock_bestbuy_api):
    lat = 44.88476
    lng = -93.30058
    distance = 10
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(
        url__regex=r".*stores\(area\(44\.88476,-93\.30058,10\)\).*"
    ).mock(return_value=httpx.Response(200, json={"stores": [{"storeId": 281}]}))
    response = bbapi.stores.search_by_area(
        lat=lat, lng=lng, distance_miles=distance, format="json"
    )
    assert response["stores"][0]["storeId"] == 281


@pytest.mark.unit
def test_all_and_search(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores.*").mock(
        return_value=httpx.Response(
            200, json={"stores": [{"storeId": 281}], "total": 1}
        )
    )
    res1 = bbapi.stores.all(format="json")
    assert len(res1["stores"]) == 1

    res2 = bbapi.stores.search("storeType=Big Box", format="json")
    assert len(res2["stores"]) == 1


@pytest.mark.unit
def test_stores_iterators(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores.*").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "stores": [{"storeId": 1}],
                    "currentPage": 1,
                    "totalPages": 2,
                    "nextCursorMark": "mark2",
                },
            ),
            httpx.Response(
                200,
                json={
                    "stores": [{"storeId": 2}],
                    "currentPage": 2,
                    "totalPages": 2,
                    "nextCursorMark": None,
                },
            ),
        ]
    )
    # Test iter_pages
    pages = list(bbapi.stores.iter_pages(max_pages=2))
    assert len(pages) == 2

    # Reset mock for iter_cursor
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores.*").mock(
        side_effect=[
            httpx.Response(
                200,
                json={"stores": [{"storeId": 1}], "nextCursorMark": "mark2"},
            ),
            httpx.Response(
                200,
                json={"stores": [{"storeId": 2}], "nextCursorMark": None},
            ),
        ]
    )
    cursor_pages = list(bbapi.stores.iter_cursor())
    assert len(cursor_pages) == 2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_stores(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores.*").mock(
        return_value=httpx.Response(200, json={"stores": [{"storeId": 281}]})
    )
    assert (await bbapi.stores.asearch_by_id(281, format="json"))["stores"][0][
        "storeId"
    ] == 281
    assert (await bbapi.stores.asearch_by_postal_code(55423, format="json"))["stores"][
        0
    ]["storeId"] == 281
    assert (await bbapi.stores.asearch_by_city("Richfield", format="json"))["stores"][
        0
    ]["storeId"] == 281
    assert (await bbapi.stores.asearch_by_region("MN", format="json"))["stores"][0][
        "storeId"
    ] == 281
    assert (await bbapi.stores.asearch_by_area(44.88, -93.30, 10, format="json"))[
        "stores"
    ][0]["storeId"] == 281
    assert (await bbapi.stores.aall(format="json"))["stores"][0]["storeId"] == 281

    # Test aiter_pages and aiter_cursor
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores.*").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "stores": [{"storeId": 1}],
                    "currentPage": 1,
                    "totalPages": 2,
                    "nextCursorMark": "m2",
                },
            ),
            httpx.Response(
                200,
                json={
                    "stores": [{"storeId": 2}],
                    "currentPage": 2,
                    "totalPages": 2,
                    "nextCursorMark": None,
                },
            ),
        ]
    )
    async_pages = [p async for p in bbapi.stores.aiter_pages(max_pages=2)]
    assert len(async_pages) == 2

    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*stores.*").mock(
        side_effect=[
            httpx.Response(
                200, json={"stores": [{"storeId": 1}], "nextCursorMark": "m2"}
            ),
            httpx.Response(
                200, json={"stores": [{"storeId": 2}], "nextCursorMark": None}
            ),
        ]
    )
    async_cursors = [p async for p in bbapi.stores.aiter_cursor()]
    assert len(async_cursors) == 2
