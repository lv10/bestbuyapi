import os
import json
import unittest

from nose.tools import ok_

from bestbuy import BestBuyStoresAPI


class TestStoresAPI(unittest.TestCase):
    def setUp(self):
        self.key = os.getenv("BESTBUY_API_KEY")
        self._api_name = "stores"
        self.bestbuy = BestBuyStoresAPI(self.key)

    def test_search(self):
        store_id = 281
        response_format = "json"
        response = self.bestbuy.search_by_id(store_id=store_id, format=response_format)
        json_response = json.loads(response)
        ok_(store_id == json_response["stores"][0]["storeId"], "Store by id not found")
