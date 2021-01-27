import json

from bestbuyapi import BestBuyAPI


def test_search(bbapi):
    store_id = 281
    response_format = "json"
    response = bbapi.stores.search_by_id(store_id=store_id, format=response_format)
    assert store_id == response["stores"][0]["storeId"], "Store by id not found"
