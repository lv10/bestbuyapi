import pytest
import httpx


@pytest.mark.unit
def test_search(bbapi, mock_bestbuy_api):
    store_id = 281
    response_format = "json"
    mock_bestbuy_api.get(url__regex=r".*stores\(storeId=281\).*").mock(
        return_value=httpx.Response(200, json={"stores": [{"storeId": store_id}]})
    )
    response = bbapi.stores.search_by_id(store_id=store_id, format=response_format)
    assert store_id == response["stores"][0]["storeId"], "Store by id not found"
