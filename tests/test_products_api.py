import os
import json
import unittest

from nose.tools import ok_

from bestbuy import BASE_URL, BestBuyAPI


class TestProductsAPI(unittest.TestCase):
    def setUp(self):

        self.key = os.getenv("BESTBUY_API_KEY")
        self._api_name = "products"
        self.bbapi = BestBuyAPI(self.key)

    def test_search_by_description(self):
        description_type = 1
        description = "iphone*"
        response_format = "json"
        response = self.bbapi.products.search_by_description(
            description_type=description_type,
            description=description,
            format=response_format,
        )
        product_name = response["products"][0]["name"]
        ok_("iphone" in product_name.lower(), "Description search failing")

    def test_search_by_sku(self):
        sku_nbr = 5706617
        response = self.bbapi.products.search_by_sku(sku=sku_nbr, format="json")
        ok_(sku_nbr == response["products"][0]["sku"], "Product SKU by search fails")

    def test_search(self):
        query = "sku in(5706617,6084400,2088495)"
        result = self.bbapi.products.search(query=query, format="json")
        ok_(result["total"] >= 2, "general search is failing to complete")
