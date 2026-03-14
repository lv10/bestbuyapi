import pytest


@pytest.mark.integration
def test_live_search_by_sku(bbapi):
    # First, find a valid SKU by searching for a common brand
    search_response = bbapi.products.search_by_description(
        description_type=1, description="Apple*", format="json"
    )

    if not search_response.get("products"):
        pytest.fail(
            f"Could not find any Apple products to test with. Response: {search_response}"
        )

    # Take the first product's SKU
    product = search_response["products"][0]
    sku_nbr = product["sku"]

    # Now test search_by_sku with that valid SKU
    response = bbapi.products.search_by_sku(sku=sku_nbr, format="json")

    assert "products" in response, (
        f"Response missing 'products' key. Response: {response}"
    )
    assert len(response["products"]) > 0, (
        f"No products found for SKU {sku_nbr}. Response: {response}"
    )
    assert response["products"][0]["sku"] == sku_nbr


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_asearch_by_sku(bbapi):
    # First, find a valid SKU by searching for a common brand asynchronously
    search_response = await bbapi.products.asearch_by_description(
        description_type=1, description="Nintendo*", format="json"
    )

    if not search_response.get("products"):
        pytest.fail(
            f"Could not find any Nintendo products to test with. Response: {search_response}"
        )

    # Take the first product's SKU
    product = search_response["products"][0]
    sku_nbr = product["sku"]

    # Now test asearch_by_sku with that valid SKU
    response = await bbapi.products.asearch_by_sku(sku=sku_nbr, format="json")

    assert "products" in response, (
        f"Response missing 'products' key. Response: {response}"
    )
    assert len(response["products"]) > 0, (
        f"No products found for SKU {sku_nbr}. Response: {response}"
    )
    assert response["products"][0]["sku"] == sku_nbr
