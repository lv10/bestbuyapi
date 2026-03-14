import xml.etree.ElementTree as ET

import pytest

from bestbuyapi.utils.exceptions import BestBuyAPIError


@pytest.mark.unit
def test_validate_params(bbapi):
    with pytest.raises(BestBuyAPIError):
        payload = {"query": "some query", "params": {"fiz": "bazz", "wrong": None}}
        bbapi.category._validate_params(payload)


@pytest.mark.unit
def test_json_response(bbapi, mock_bestbuy_api):
    query = "accessories.sku=5985609"
    response = bbapi.products.search(query=query, format="json")
    assert isinstance(response, dict), "Response cannot be converted to JSON"


@pytest.mark.unit
def test_xml_response(bbapi, mock_bestbuy_api):
    sku_nbr = 5985609
    query = f"sku={sku_nbr}"

    # leaving the format blank will default to xml
    response = bbapi.products.search(query=query, format="xml")
    xml_tree = ET.fromstring(response)
    response_sku = xml_tree[0].findall("sku")[0].text
    assert int(response_sku) == sku_nbr, "XML Response parsing is failing"
