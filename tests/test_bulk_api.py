import os
import zipfile
import unittest
from io import StringIO

from nose.tools import ok_

from bestbuy import BASE_URL, BestBuyBulkAPI


class TestBulkAPI(unittest.TestCase):

    def setUp(self):

        self.key = os.getenv("BESTBUY_API_KEY")
        self.bestbuy = BestBuyBulkAPI(self.key)

    def test_build_url(self):
        sample_url = f"{BASE_URL}products.xml.zip"
        payload = {
            'query': "products.xml.zip",
            'params': {}
        }
        url, thePayload = self.bestbuy._build_url(payload)
        ok_(sample_url == url, "URL construction has issues")
        ok_(thePayload.get('apiKey') is not None, "API Key is None")

    def test_archive(self):
        archive_name = "categories"
        file_format = "xml"
        response = self.bestbuy.archive(archive_name, file_format)
        ok_(len(response) >= 1, "Response is empty")
        for _, data in response.items():
            ok_(isinstance(data, bytes), "XML data response is not bytes")

    def test_archive_subset(self):
        subset_name = "productsSoftware"
        file_format = "json"
        response = self.bestbuy.archive_subset(subset_name, file_format)
        ok_(isinstance(response, dict) is True,"Response type is not a dict")
        ok_(len(response) >= 1,"Response is empty")
