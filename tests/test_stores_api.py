import os
import json
import unittest

from nose.tools import ok_

from bestbuy import BestBuyAPI


class TestStoresAPI(unittest.TestCase):
    def setUp(self):
        self.key = os.getenv("BESTBUY_API_KEY")
        self._api_name = "stores"
        self.bbapi = BestBuyAPI(self.key)

    def test_search(self):
        store_id = 281
        response_format = "json"
        response = self.bbapi.stores.search_by_id(store_id=store_id, format=response_format)
        ok_(store_id == response["stores"][0]["storeId"], "Store by id not found")
