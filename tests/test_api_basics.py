import json
import xml.etree.ElementTree as ET

import pytest

from bestbuyapi.utils.exceptions import BestBuyAPIError


def test_validate_params(bbapi):
    with pytest.raises(BestBuyAPIError):
        payload = {"query": "some query", "params": {"fiz": "bazz", "wrong": None}}
        bbapi.category._validate_params(payload)


def test_json_response(bbapi):
    query = "accessories.sku=5985609"
    response = bbapi.products.search(query=query, format="json")
    assert isinstance(response, dict), "Response cannot be converted to JSON"


def test_xml_response(bbapi):

    sku_nbr = 5985609
    query = f"sku={sku_nbr}"

    # leaving the format blank will default to xml
    response = bbapi.products.search(query=query, format="xml")
    xml_tree = ET.fromstring(response)
    response_sku = xml_tree[0].findall("sku")[0].text
    assert int(response_sku) == sku_nbr, "XML Response parsing is failing"
