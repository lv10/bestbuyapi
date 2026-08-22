import httpx
import pytest
import respx

from bestbuyapi.utils.exceptions import (
    BestBuyAuthenticationError,
    BestBuyHTTPError,
    BestBuyNotFoundError,
    BestBuyRateLimitError,
    BestBuyServerError,
    BestBuyValidationError,
)


@pytest.mark.unit
def test_invalid_param_error(bbapi):
    with pytest.raises(BestBuyValidationError) as exc:
        bbapi.products.search("sku=123", invalid_param_name="value")
    assert "invalid Search Parameter" in str(exc.value)


@pytest.mark.unit
def test_none_param_value_error(bbapi):
    with pytest.raises(BestBuyValidationError) as exc:
        bbapi.products.search("sku=123", format=None)
    assert "can't have None" in str(exc.value)


@pytest.mark.unit
def test_http_401_authentication_error(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(
                401, json={"error": {"message": "Invalid API key."}}
            )
        )
        with pytest.raises(BestBuyAuthenticationError) as exc:
            bbapi.products.search("sku=123")
        assert exc.value.status_code == 401
        assert "Invalid API key" in exc.value.message


@pytest.mark.unit
def test_http_404_not_found_error(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(404, json={"message": "Resource not found"})
        )
        with pytest.raises(BestBuyNotFoundError) as exc:
            bbapi.products.search("sku=123")
        assert exc.value.status_code == 404


@pytest.mark.unit
def test_http_429_rate_limit_error(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(429, json={"message": "Call limit reached."})
        )
        with pytest.raises(BestBuyRateLimitError) as exc:
            bbapi.products.search("sku=123")
        assert exc.value.status_code == 429


@pytest.mark.unit
def test_http_500_server_error(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )
        with pytest.raises(BestBuyServerError) as exc:
            bbapi.products.search("sku=123")
        assert exc.value.status_code == 500


@pytest.mark.unit
def test_http_400_generic_error(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(400, json={"error": "Bad request syntax"})
        )
        with pytest.raises(BestBuyHTTPError) as exc:
            bbapi.products.search("sku=123")
        assert exc.value.status_code == 400


@pytest.mark.unit
def test_http_error_with_errors_array(bbapi):
    with respx.mock:
        respx.get(url__regex=r".*products.*").mock(
            return_value=httpx.Response(400, json={"errors": ["Field error 1"]})
        )
        with pytest.raises(BestBuyHTTPError) as exc:
            bbapi.products.search("sku=123")
        assert "Field error 1" in exc.value.message
