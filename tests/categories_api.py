import json
import unittest
import xml.etree.ElementTree as ET

from nose.tools import raises

from api.constants import BASE_URL
from api.products import BestBuyProductsAPI, BestBuyProductAPIError


class TestProductsAPI(unittest.TestCase):

    def setUp(self):

        self.key = "YourSecretKey"
        self.bb = BestBuyProductsAPI(self.key)

    def tearDown(self):
        pass

