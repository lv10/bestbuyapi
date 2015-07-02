import unittest

from nose.tools import raises

from api.products import BestBuyAPI, BestBuyAPIError


class TestAPIBasics(unittest.TestCase):

    def setUp(self):
        self.key = "aSecretKey"
        self.bestbuy = BestBuyAPI(self.key)

    def tearDown(self):
        pass

    @raises(BestBuyAPIError)
    def test_validate_params(self):

        payload = {
            'query': "some query",
            'params': {'fiz': "bazz", 'wrong': None}
        }

        self.bestbuy._validate_params(payload)
