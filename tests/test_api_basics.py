import xml.etree.ElementTree as ET

import httpx
import pytest
import respx

from bestbuyapi import BestBuyAPI
from bestbuyapi.utils.exceptions import BestBuyValidationError


@pytest.mark.unit
def test_validate_params(bbapi):
    with pytest.raises(BestBuyValidationError):
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


@pytest.mark.unit
def test_corrupted_json_content_type_fallback(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(
                200,
                content=b"Invalid JSON content",
                headers={"Content-Type": "application/json"},
            )
        )
        resp = bbapi.products.search(query="sku=123")
        assert resp == b"Invalid JSON content"


@pytest.mark.unit
def test_query_parentheses_building(bbapi):
    url, _ = bbapi.products._build_url({"query": "(sku=123)", "params": {}})
    assert url == "https://api.bestbuy.com/v1/products(sku=123)"


@pytest.mark.unit
def test_core_direct_context_manager():
    core = BestBuyAPI("dummy_key").products
    with core as c:
        assert c is core


@pytest.mark.asyncio
@pytest.mark.unit
async def test_core_direct_async_context_manager():
    core = BestBuyAPI("dummy_key").products
    async with core as c:
        assert c is core
