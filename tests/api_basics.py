import unittest

from nose.tools import raises

from api.constants import BASE_URL
from api.products import BestBuyAPI, BestBuyAPIError


class TestAPIBasics(unittest.TestCase):

    def setUp(self):
        self.key = "aSecretKey"
        self.bestbuy = BestBuyAPI(self.key)

    def tearDown(self):
        pass

    def test_build_url(self):

        sample_url = "{0}products(sku=43900)".format(BASE_URL)

        payload = {
            'query': "sku=43900",
            'params': {'format': "json"}
        }

        url, thePayload = self.bestbuy._build_url(payload)

        assert sample_url == url
        assert (thePayload['format'] == "json"
                and thePayload.get('apiKey') is not None)

    @raises(BestBuyAPIError)
    def test_validate_params(self):

        payload = {
            'query': "some query",
            'params': {'fiz': "bazz", 'wrong': None}
        }

        self.bestbuy._validate_params(payload)
