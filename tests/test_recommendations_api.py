import httpx
import pytest
import respx


@pytest.mark.unit
def test_also_bought(bbapi):
    sku = 8880044
    mock_resp = {
        "metadata": {"context": {}, "resultSet": {"count": 1}},
        "results": [{"sku": "9124743", "customerReviews": {"averageScore": 4.9}}],
    }

    with respx.mock:
        respx.get(f"https://api.bestbuy.com/v1/products/{sku}/alsoBought").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        res = bbapi.recommendations.also_bought(sku)
        assert res == mock_resp
        assert res["results"][0]["sku"] == "9124743"


@pytest.mark.unit
def test_also_viewed(bbapi):
    sku = 8880044
    mock_resp = {
        "metadata": {"resultSet": {"count": 1}},
        "results": [{"sku": "1234567"}],
    }

    with respx.mock:
        respx.get(f"https://api.bestbuy.com/v1/products/{sku}/alsoViewed").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        res = bbapi.recommendations.also_viewed(sku)
        assert res["results"][0]["sku"] == "1234567"


@pytest.mark.unit
def test_trending(bbapi):
    mock_resp = {"results": [{"sku": "6323759"}]}

    with respx.mock:
        # Without category
        respx.get("https://api.bestbuy.com/v1/products/trendingViewed").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        res1 = bbapi.recommendations.trending()
        assert res1["results"][0]["sku"] == "6323759"

        # With category
        cat_id = "abcat0400000"
        respx.get(
            f"https://api.bestbuy.com/v1/products/trendingViewed(categoryId={cat_id})"
        ).mock(return_value=httpx.Response(200, json=mock_resp))
        res2 = bbapi.recommendations.trending(category_id=cat_id)
        assert res2["results"][0]["sku"] == "6323759"


@pytest.mark.unit
def test_most_viewed(bbapi):
    mock_resp = {"results": [{"sku": "5852832"}]}

    with respx.mock:
        # Without category
        respx.get("https://api.bestbuy.com/v1/products/mostViewed").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        res1 = bbapi.recommendations.most_viewed()
        assert res1["results"][0]["sku"] == "5852832"

        # With category
        cat_id = "abcat0107000"
        respx.get(
            f"https://api.bestbuy.com/v1/products/mostViewed(categoryId={cat_id})"
        ).mock(return_value=httpx.Response(200, json=mock_resp))
        res2 = bbapi.recommendations.most_viewed(category_id=cat_id)
        assert res2["results"][0]["sku"] == "5852832"


@pytest.mark.unit
def test_viewed_ultimately_bought(bbapi):
    sku = 8880044
    mock_resp = {"results": [{"sku": "3921114"}]}

    with respx.mock:
        respx.get(
            f"https://api.bestbuy.com/v1/products/{sku}/viewedUltimatelyBought"
        ).mock(return_value=httpx.Response(200, json=mock_resp))
        res = bbapi.recommendations.viewed_ultimately_bought(sku)
        assert res["results"][0]["sku"] == "3921114"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_recommendations(bbapi):
    sku = 8880044
    mock_resp = {"results": [{"sku": "9124743"}]}

    with respx.mock:
        respx.get(f"https://api.bestbuy.com/v1/products/{sku}/alsoBought").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        respx.get(f"https://api.bestbuy.com/v1/products/{sku}/alsoViewed").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        respx.get("https://api.bestbuy.com/v1/products/trendingViewed").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        respx.get("https://api.bestbuy.com/v1/products/mostViewed").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        respx.get(
            f"https://api.bestbuy.com/v1/products/{sku}/viewedUltimatelyBought"
        ).mock(return_value=httpx.Response(200, json=mock_resp))

        assert (await bbapi.recommendations.aalso_bought(sku))["results"][0][
            "sku"
        ] == "9124743"
        assert (await bbapi.recommendations.aalso_viewed(sku))["results"][0][
            "sku"
        ] == "9124743"
        assert (await bbapi.recommendations.atrending())["results"][0][
            "sku"
        ] == "9124743"
        assert (await bbapi.recommendations.amost_viewed())["results"][0][
            "sku"
        ] == "9124743"
        assert (await bbapi.recommendations.aviewed_ultimately_bought(sku))["results"][
            0
        ]["sku"] == "9124743"
