import pytest
import zipfile
from io import BytesIO

import httpx

from bestbuyapi import BASE_URL


@pytest.mark.unit
def test_build_url(bbapi):
    sample_url = f"{BASE_URL}products.xml.zip"
    payload = {"query": "products.xml.zip", "params": {}}
    url, thePayload = bbapi.bulk._build_url(payload)
    assert sample_url == url, "URL construction has issues"
    assert thePayload.get("apiKey") is not None, "API Key is None"


@pytest.mark.unit
def test_archive(bbapi, mock_bestbuy_api):
    mock_bestbuy_api.routes.clear()
    archive_name = "categories"
    file_format = "xml"

    # Mock zip response for archive
    bio = BytesIO()
    with zipfile.ZipFile(bio, "w") as z:
        z.writestr("test.xml", b"<test>data</test>")

    # URL is https://api.bestbuy.com/v1/categories.xml.zip
    mock_bestbuy_api.get(url__regex=r".*categories\.xml\.zip.*").mock(
        return_value=httpx.Response(200, content=bio.getvalue())
    )

    response = bbapi.bulk.archive(archive_name, file_format)
    assert len(response) >= 1, "Response is empty"
    for _, data in response.items():
        assert isinstance(data, bytes), "XML data response is not bytes"


@pytest.mark.unit
def test_archive_subset(bbapi, mock_bestbuy_api):
    """The only available subset is productsActive, all other subsets are empty.
    This tests makes sure that subsets are still supported.
    """
    mock_bestbuy_api.routes.clear()
    subset_name = "productsSoftware"
    file_format = "json"

    # Mock zip response for archive_subset
    bio = BytesIO()
    with zipfile.ZipFile(bio, "w") as z:
        z.writestr("test.json", b'{"key": "value"}')

    mock_bestbuy_api.get(url__regex=r".*subsets/productsSoftware\.json\.zip.*").mock(
        return_value=httpx.Response(200, content=bio.getvalue())
    )

    _ = bbapi.bulk.archive_subset(subset_name, file_format)
