import json

from bestbuyapi import BASE_URL, BestBuyAPI


def test_search_by_description(bbapi):
    description_type = 1
    description = "iphone*"
    response_format = "json"
    response = bbapi.products.search_by_description(
        description_type=description_type,
        description=description,
        format=response_format,
    )
    product_name = response["products"][0]["name"]
    assert "iphone" in product_name.lower(), "Description search failing"


def test_search_by_sku(bbapi):
    sku_nbr = 5706617
    response = bbapi.products.search_by_sku(sku=sku_nbr, format="json")
    assert sku_nbr == response["products"][0]["sku"], "Product SKU by search fails"


def test_search(bbapi):
    query = "sku in(5706617,6084400,2088495)"
    result = bbapi.products.search(query=query, format="json")
    assert result["total"] >= 2, "general search is failing to complete"
