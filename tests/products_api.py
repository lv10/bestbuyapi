import json
import unittest

from api.constants import BASE_URL
from api.products import BestBuyProductsAPI


class TestProductsAPI(unittest.TestCase):

    def setUp(self):
        self.key = "YourSecretKey"
        self.bestbuy = BestBuyProductsAPI(self.key)
        self._api_name = "products"

    def test_build_url(self):

        sample_url = "{0}{1}(sku=43900)".format(BASE_URL, self._api_name)

        payload = {
            'query': "sku=43900",
            'params': {'format': "json"}
        }

        url, thePayload = self.bestbuy._build_url(payload)

        assert sample_url == url
        assert (thePayload['format'] == "json"
                and thePayload.get('apiKey') is not None)

    def test_search_by_description(self):

        description_type = 1
        description = "iphone*"
        response_format = "json"

        response = self.bestbuy.search_by_description(
            description_type=description_type,
            description=description,
            format=response_format)

        json_response = json.loads(response)
        product_name = json_response['products'][0]['name']

        assert "iphone" in product_name.lower()

    def test_search_by_sku(self):

        sku_nbr = 9776457

        response = self.bestbuy.search_by_sku(sku=sku_nbr, format="json")
        json_response = json.loads(response)

        return sku_nbr == json_response['products'][0]['sku']

    def test_search(self):

        query = "sku in(43900,2088495,7150065)"
        result = self.bestbuy.search(query=query, format="json")

        json_response = json.loads(result)

        assert json_response['total'] == 3
