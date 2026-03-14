import pytest
import httpx


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
def test_search(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    query = "sku in(5706617,6084400,2088495)"
    # Account for potential URL encoding of spaces/parentheses
    mock_bestbuy_api.get(
        url__regex=r".*products\(sku.*in.*5706617.*6084400.*2088495.*"
    ).mock(return_value=httpx.Response(200, json={"total": 3, "products": []}))
    result = bbapi.products.search(query=query, format="json")
    assert result["total"] >= 2, "general search is failing to complete"
