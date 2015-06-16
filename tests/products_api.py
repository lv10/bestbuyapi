import json
import unittest
import xml.etree.ElementTree as ET


from api.products import BestBuyProductsAPI


class TestProductsAPI(unittest.TestCase):

    def setUp(self):
        self.key = "7uydv9dy2t95c3k69g7t69qx"
        self.key = "7uydv9dy2t95c3k69g7t69qx"
        self.bb = BestBuyProductsAPI(self.key)

    def tearDown(self):
        pass

    def test_json_response(self):
        query = "sku=9776457"
        response = self.bb.search(query=query, format="json")
        return type(json.loads(response)) is dict

    def test_xml_response(self):
        sku_nbr = 9776457
        query = "sku={0}".format(sku_nbr)

        # leaving the format blank will default to xml
        response = self.bb.search(query=query, format="xml")
        xml_tree = ET.fromstring(response)
        response_sku = xml_tree.getchildren()[0].findall('sku')[0].text
        return int(response_sku) == sku_nbr

    def test_search_by_sku(self):
        sku_nbr = 9776457

        response = self.bb.search_by_sku(sku=sku_nbr, format="json")
        json_response = json.loads(response)

        return sku_nbr == json_response['products'][0]['sku']

    def test_search(self):
        query = "sku in(43900,2088495,7150065)"
        result = self.bb.search(query=query, format="json")

        json_response = json.loads(result)

        return json_response['total'] == 3
