import pytest
import httpx

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
