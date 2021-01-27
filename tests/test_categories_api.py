import json

from bestbuyapi import BASE_URL, BestBuyAPI


api_name = "categories"


def test_build_url(bbapi):

    sample_url = f"{BASE_URL}{api_name}(sku=43900)"
    payload = {"query": "sku=43900", "params": {"format": "json"}}
    url, thePayload = bbapi.category._build_url(payload)
    assert sample_url == url, "Sample url is different built url"
    assert thePayload["format"] == "json", "Response format isn't JSON"
    assert thePayload.get("apiKey") is not None, "Response doesn't have API Key"


def test_search_category_by_id(bbapi):
    cat_id = "cat00000"
    query = f"id={cat_id}"
    resp = bbapi.category.search(query=query, show="id", format="json")
    assert resp["categories"][0]["id"] == cat_id, "Returned category id is different"


def test_search_category_by_name(bbapi):
    cat_name = "Sony"
    query = f"name={cat_name}"
    resp = bbapi.category.search(query=query, format="json")
    assert (
        resp["categories"][0]["name"] == cat_name
    ), "Response category name is different"
