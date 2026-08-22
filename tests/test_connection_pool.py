import httpx
import pytest

from bestbuyapi import AsyncBestBuyAPI, BestBuyAPI
from bestbuyapi.utils.exceptions import BestBuyAuthenticationError


@pytest.mark.unit
def test_env_var_fallback(monkeypatch):
    monkeypatch.setenv("BESTBUY_API_KEY", "env_test_key")
    bb = BestBuyAPI()
    assert bb.api_key == "env_test_key"


@pytest.mark.unit
def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("BESTBUY_API_KEY", raising=False)
    with pytest.raises(BestBuyAuthenticationError):
        BestBuyAPI()


@pytest.mark.unit
def test_sync_client_reuse_and_close():
    bb = BestBuyAPI("test_key")
    client1 = bb.get_client()
    client2 = bb.products.get_client()
    assert client1 is client2
    assert not client1.is_closed

    bb.close()
    assert client1.is_closed


@pytest.mark.unit
def test_sync_context_manager():
    with BestBuyAPI("test_key") as bb:
        client = bb.get_client()
        assert not client.is_closed
    assert client.is_closed


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_client_reuse_and_close():
    bb = BestBuyAPI("test_key")
    aclient1 = bb.get_aclient()
    aclient2 = bb.products.get_aclient()
    assert aclient1 is aclient2
    assert not aclient1.is_closed

    await bb.aclose()
    assert aclient1.is_closed


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_bestbuy_api_context_manager():
    async with AsyncBestBuyAPI("test_key") as bb:
        assert bb.aclient is not None
        assert bb.products.aclient is bb.aclient
        assert bb.stores.aclient is bb.aclient
        assert bb.recommendations.aclient is bb.aclient
        assert bb.open_box.aclient is bb.aclient
        assert not bb.aclient.is_closed

    assert bb.aclient is None
    assert bb.products.aclient is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_bestbuy_api_with_preset_aclient():
    custom_aclient = httpx.AsyncClient()
    async with AsyncBestBuyAPI("test_key", aclient=custom_aclient) as bb:
        assert bb.get_aclient() is custom_aclient
    await custom_aclient.aclose()
