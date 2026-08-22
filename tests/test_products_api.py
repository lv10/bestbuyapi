import httpx
import pytest

from bestbuyapi.utils.exceptions import BestBuyValidationError


@pytest.mark.unit
def test_search_by_description(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    description_type = 1
    description = "iphone*"
    response_format = "json"
    mock_bestbuy_api.get(url__regex=r".*products\(name=iphone.*").mock(
        return_value=httpx.Response(200, json={"products": [{"name": "iPhone 13"}]})
    )
    response = bbapi.products.search_by_description(
        description_type=description_type,
        description=description,
        format=response_format,
    )
    product_name = response["products"][0]["name"]
    assert "iphone" in product_name.lower(), "Description search failing"


@pytest.mark.unit
def test_search_by_sku(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    sku_nbr = 5706617
    mock_bestbuy_api.get(url__regex=r".*products\(sku=5706617\).*").mock(
        return_value=httpx.Response(200, json={"products": [{"sku": sku_nbr}]})
    )
    response = bbapi.products.search_by_sku(sku=sku_nbr, format="json")
    assert sku_nbr == response["products"][0]["sku"], "Product SKU by search fails"


@pytest.mark.unit
def test_search_by_upc(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    upc = "012345678901"
    mock_bestbuy_api.get(url__regex=r".*products\(upc=012345678901\).*").mock(
        return_value=httpx.Response(200, json={"products": [{"upc": upc}]})
    )
    response = bbapi.products.search_by_upc(upc=upc, format="json")
    assert response["products"][0]["upc"] == upc


@pytest.mark.unit
def test_search_by_review_criteria(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    # Test review_type=1 (customerReviewAverage)
    mock_bestbuy_api.get(url__regex=r".*products\(customerReviewAverage=4\.5\).*").mock(
        return_value=httpx.Response(
            200, json={"products": [{"customerReviewAverage": 4.5}]}
        )
    )
    res1 = bbapi.products.search_by_review_criteria(
        review_type=1, review=4.5, format="json"
    )
    assert res1["products"][0]["customerReviewAverage"] == 4.5

    # Test review_type=2 (customerReviewCount)
    mock_bestbuy_api.get(url__regex=r".*products\(customerReviewCount=100\).*").mock(
        return_value=httpx.Response(
            200, json={"products": [{"customerReviewCount": 100}]}
        )
    )
    res2 = bbapi.products.search_by_review_criteria(
        review_type=2, review=100, format="json"
    )
    assert res2["products"][0]["customerReviewCount"] == 100


@pytest.mark.unit
def test_search_validation_errors(bbapi):
    with pytest.raises(BestBuyValidationError):
        bbapi.products.search_by_description(description_type=99, description="test")

    with pytest.raises(BestBuyValidationError):
        bbapi.products.search_by_review_criteria(review_type=99, review=4.0)


@pytest.mark.unit
def test_search(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    query = "sku in(5706617,6084400,2088495)"
    mock_bestbuy_api.get(
        url__regex=r".*products\(sku.*in.*5706617.*6084400.*2088495.*"
    ).mock(return_value=httpx.Response(200, json={"total": 3, "products": []}))
    result = bbapi.products.search(query=query, format="json")
    assert result["total"] >= 2, "general search is failing to complete"


@pytest.mark.unit
def test_products_all_and_iterators(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*products.*").mock(
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

    all_res = bbapi.products.all(format="json")
    assert len(all_res["products"]) == 1

    # Reset mock for iter_pages
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*products.*").mock(
        side_effect=[
            httpx.Response(
                200,
                json={"products": [{"sku": 1}], "currentPage": 1, "totalPages": 2},
            ),
            httpx.Response(
                200,
                json={"products": [{"sku": 2}], "currentPage": 2, "totalPages": 2},
            ),
        ]
    )
    pages = list(bbapi.products.iter_pages(max_pages=2))
    assert len(pages) == 2

    # Reset mock for iter_cursor
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*products.*").mock(
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
    cursor_results = list(bbapi.products.iter_cursor())
    assert len(cursor_results) == 2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_products_async_methods(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*products.*").mock(
        return_value=httpx.Response(200, json={"products": [{"sku": 123}]})
    )

    assert (await bbapi.products.asearch_by_sku(123, format="json"))["products"][0][
        "sku"
    ] == 123
    assert (await bbapi.products.asearch_by_upc("01234", format="json"))["products"][0][
        "sku"
    ] == 123
    assert (await bbapi.products.asearch_by_review_criteria(1, 4.5, format="json"))[
        "products"
    ][0]["sku"] == 123
    assert (await bbapi.products.aall(format="json"))["products"][0]["sku"] == 123

    with pytest.raises(BestBuyValidationError):
        await bbapi.products.asearch_by_description(99, "test")

    with pytest.raises(BestBuyValidationError):
        await bbapi.products.asearch_by_review_criteria(99, 4.0)

    # Test aiter_cursor
    mock_bestbuy_api.routes.clear()
    mock_bestbuy_api.get(url__regex=r".*products.*").mock(
        side_effect=[
            httpx.Response(
                200, json={"products": [{"sku": 1}], "nextCursorMark": "c2"}
            ),
            httpx.Response(
                200, json={"products": [{"sku": 2}], "nextCursorMark": None}
            ),
        ]
    )
    async_cursors = [p async for p in bbapi.products.aiter_cursor()]
    assert len(async_cursors) == 2
