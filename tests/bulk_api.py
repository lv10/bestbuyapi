import zipfile
import unittest
from StringIO import StringIO

from bestbuy import BASE_URL
from bestbuy import BestBuyBulkAPI
from config import TEST_API_KEY


class TestBulkAPI(unittest.TestCase):

    def setUp(self):

        self.key = TEST_API_KEY
        self.bestbuy = BestBuyBulkAPI(self.key)

    def test_build_url(self):

        sample_url = "{0}products.xml.zip".format(BASE_URL)

        payload = {
            'query': "products.xml.zip",
            'params': {}
        }

        url, thePayload = self.bestbuy._build_url(payload)

        assert sample_url == url
        assert thePayload.get('apiKey') is not None

    def test_archive(self):

        archive_name = "categories"
        file_format = "xml"

        response = self.bestbuy.archive(archive_name, file_format)
        the_zipfile = zipfile.ZipFile(StringIO(response))

        # This test will fail if there's a bad file in the zip file or if
        # if the zip file comes back empty
        assert the_zipfile.testzip() is None
        assert the_zipfile.namelist() > 0

    def test_archive_subset(self):

        subset_name = "productsSoftware"
        file_format = "json"

        response = self.bestbuy.archive_subset(subset_name, file_format)
        the_zipfile = zipfile.ZipFile(StringIO(response))

        # This test will fail if there's a bad file in the zip file or if
        # if the zip file comes back empty
        assert the_zipfile.testzip() is None
        assert the_zipfile.namelist() > 0
