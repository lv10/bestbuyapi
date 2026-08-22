import httpx
import pytest
import respx


@pytest.mark.unit
def test_openbox_single_sku(bbapi):
    sku = 8610161
    mock_resp = {
        "results": [
            {
                "customerReviews": {"averageScore": "4.5"},
                "names": {"title": "Test Product"},
                "offers": [{"condition": "excellent", "prices": {"current": 149.99}}],
            }
        ]
    }

    with respx.mock:
        respx.get(f"https://api.bestbuy.com/beta/products/{sku}/openBox").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )
        res = bbapi.open_box.search_by_sku(sku)
        assert res == mock_resp
        assert res["results"][0]["offers"][0]["condition"] == "excellent"


@pytest.mark.unit
def test_openbox_multiple_skus(bbapi):
    skus = [5729048, 7528703, 8610161]
    mock_resp = {"results": [{"sku": 5729048}, {"sku": 7528703}]}

    with respx.mock:
        respx.get(url__regex=r"https://api\.bestbuy\.com/beta/products/openBox.*").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )

        res = bbapi.open_box.search_by_skus(skus)
        assert len(res["results"]) == 2


@pytest.mark.unit
def test_openbox_by_category(bbapi):
    cat_id = "abcat0400000"
    mock_resp = {"results": [{"sku": 5729048}]}

    with respx.mock:
        respx.get(
            url__regex=r"https://api\.bestbuy\.com/beta/products/openBox\(categoryId=abcat0400000\).*"
        ).mock(return_value=httpx.Response(200, json=mock_resp))

        res = bbapi.open_box.search_by_category(cat_id)
        assert res["results"][0]["sku"] == 5729048


@pytest.mark.unit
def test_openbox_custom_search_and_alias(bbapi):
    mock_resp = {"results": []}

    with respx.mock:
        respx.get(url__regex=r"https://api\.bestbuy\.com/beta/products/openBox.*").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )

        # Test search with query
        res1 = bbapi.open_box.search("customerReviews.averageScore>4")
        assert "results" in res1

        # Test search with full prefix
        res_full = bbapi.open_box.search("products/openBox(sku=123)")
        assert "results" in res_full

        # Test search with parentheses
        res_paren = bbapi.open_box.search("(sku=123)")
        assert "results" in res_paren

        # Test search without query (all)
        res2 = bbapi.open_box.search()
        assert "results" in res2

        # Test buying_options alias
        assert bbapi.buying_options is bbapi.open_box
        res3 = bbapi.buying_options.search()
        assert "results" in res3


@pytest.mark.asyncio
@pytest.mark.unit
async def test_async_openbox(bbapi):
    sku = 8610161
    mock_resp = {"results": [{"sku": sku}]}

    with respx.mock:
        respx.get(url__regex=r"https://api\.bestbuy\.com/beta/products/.*").mock(
            return_value=httpx.Response(200, json=mock_resp)
        )

        res_sku = await bbapi.open_box.asearch_by_sku(sku)
        assert res_sku["results"][0]["sku"] == sku

        res_skus = await bbapi.open_box.asearch_by_skus([sku])
        assert res_skus["results"][0]["sku"] == sku

        res_cat = await bbapi.open_box.asearch_by_category("abcat0400000")
        assert res_cat["results"][0]["sku"] == sku

        res_search = await bbapi.open_box.asearch()
        assert res_search["results"][0]["sku"] == sku

        res_search_full = await bbapi.open_box.asearch("products/openBox(sku=123)")
        assert res_search_full["results"][0]["sku"] == sku

        res_search_paren = await bbapi.open_box.asearch("(sku=123)")
        assert res_search_paren["results"][0]["sku"] == sku
