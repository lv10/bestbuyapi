import json
import unittest
#import xml.etree.ElementTree as ET

from api.constants import BASE_URL
from api.categories import BestBuyCategoryAPI


class TestCategoryAPI(unittest.TestCase):

    def setUp(self):
        self.key = "YourSecretKey"
        self.bestbuy = BestBuyCategoryAPI(self.key)
        self._api_name = "categories"

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

    def test_search_category_by_id(self):
        cat_id = "abcat0011000"
        query = "id={0}".format(cat_id)
        response = self.bestbuy.search(query=query, show="id", format="json")
        json_response = json.loads(response)

        assert json_response['categories'][0]['id'] == cat_id
