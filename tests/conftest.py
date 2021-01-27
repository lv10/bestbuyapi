import os

import pytest

from bestbuyapi import BestBuyAPI


@pytest.fixture(scope="session")
def bbapi():
    api_key = os.getenv("BESTBUY_API_KEY")
    assert api_key is not None, "API Key not laoded"
    yield BestBuyAPI(api_key)
