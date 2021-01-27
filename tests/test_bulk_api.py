import zipfile
from io import StringIO

from bestbuyapi import BASE_URL, BestBuyAPI


def test_build_url(bbapi):
    sample_url = f"{BASE_URL}products.xml.zip"
    payload = {"query": "products.xml.zip", "params": {}}
    url, thePayload = bbapi.bulk._build_url(payload)
    assert sample_url == url, "URL construction has issues"
    assert thePayload.get("apiKey") is not None, "API Key is None"


def test_archive(bbapi):
    archive_name = "categories"
    file_format = "xml"
    response = bbapi.bulk.archive(archive_name, file_format)
    assert len(response) >= 1, "Response is empty"
    for _, data in response.items():
        assert isinstance(data, bytes), "XML data response is not bytes"


def test_archive_subset(bbapi):
    """The only available subset is productsActive, all other subsets are empty.
    This tests makes sure that subsets are still supported.
    """
    subset_name = "productsSoftware"
    file_format = "json"
    _ = bbapi.bulk.archive_subset(subset_name, file_format)
