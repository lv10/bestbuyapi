import os
import json
import unittest

from nose.tools import ok_

from bestbuy import BASE_URL, BestBuyCategoryAPI


class TestCategoryAPI(unittest.TestCase):
    def setUp(self):

        self.key = os.getenv("BESTBUY_API_KEY")
        self._api_name = "categories"
        self.bestbuy = BestBuyCategoryAPI(self.key)

    def test_build_url(self):

        sample_url = f"{BASE_URL}{self._api_name}(sku=43900)"
        payload = {"query": "sku=43900", "params": {"format": "json"}}
        url, thePayload = self.bestbuy._build_url(payload)
        ok_(sample_url == url, "Sample url is different built url")
        ok_(
            thePayload["format"] == "json" and thePayload.get("apiKey") is not None,
            "format and/or APIKey are not correctly converted",
        )

    def test_search_category_by_id(self):
        cat_id = "cat00000"
        query = f"id={cat_id}"
        response = self.bestbuy.search(query=query, show="id", format="json")
        json_response = json.loads(response)
        ok_(
            json_response["categories"][0]["id"] == cat_id,
            "Returned category id is different",
        )

    def test_search_category_by_name(self):
        cat_name = "Sony"
        query = f"name={cat_name}"
        response = self.bestbuy.search(query=query, format="json")
        json_response = json.loads(response)
        ok_(
            json_response["categories"][0]["name"] == cat_name,
            "Category name returned is different",
        )
