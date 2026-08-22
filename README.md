# Python Best Buy API Wrapper

![image](https://img.shields.io/pypi/v/bestbuyapi.svg)
[![CI Main](https://github.com/lv10/bestbuyapi/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lv10/bestbuyapi/actions/workflows/ci.yml?query=branch%3Amain)
[![CI Dev](https://github.com/lv10/bestbuyapi/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/lv10/bestbuyapi/actions/workflows/ci.yml?query=branch%3Adev)

A modern, high-performance, asynchronous and synchronous Python SDK for the [Best Buy REST API](https://bestbuyapis.github.io/api-documentation/).

---

## Features

- **Products API**: Search by SKU, UPC, description, customer review criteria, or complex query expressions.
- **Recommendations API**: Access Trending products, Most Viewed, Also Bought, Also Viewed, and Viewed Ultimately Bought.
- **Buying Options (Open Box) API**: Access open-box availability, condition ratings, and special pricing by SKU, list of SKUs, or category.
- **Stores API**: Store lookup by store ID, ZIP/postal code, city, region/state, or geographic radius search (`area(lat,lng,distance)`).
- **Categories API**: Query categories by ID, name, or custom filters.
- **Bulk Data API**: Download and parse daily archives and subsets (JSON/XML).
- **Dual Sync & Async Support**: Unified API with high-performance HTTP connection pooling via `httpx`.
- **CursorMark Pagination**: Stream large result sets seamlessly with `iter_cursor()` / `aiter_cursor()` and `iter_pages()` / `aiter_pages()`.
- **Granular Error Handling**: Specific exceptions for HTTP 401/403, 404, 429 rate limits, and server errors.
- **Type Safety**: Fully typed with PEP 561 `py.typed` support.

---

## Installation

Using `uv` (recommended):

```bash
uv add bestbuyapi
```

Or with `pip`:

```bash
pip install bestbuyapi
```

---

## Configuration

You can supply your API key directly or define `BESTBUY_API_KEY` in your environment or a `.env` file:

```env
BESTBUY_API_KEY=your_api_key_here
```

---

## Quickstart

### Synchronous Usage

```python
from bestbuyapi import BestBuyAPI

# Automatically reads BESTBUY_API_KEY from environment if not provided
with BestBuyAPI() as bb:
    # 1. Search Products
    product = bb.products.search_by_sku(5985609, format="json")
    print(product)

    # 2. Recommendations
    trending = bb.recommendations.trending(category_id="abcat0400000")
    also_bought = bb.recommendations.also_bought(8880044)

    # 3. Open Box / Buying Options
    open_box_deals = bb.open_box.search_by_sku(8610161)

    # 4. Stores by Radius (Latitude, Longitude, Distance in Miles)
    nearby_stores = bb.stores.search_by_area(lat=44.88476, lng=-93.30058, distance_miles=10)

    # 5. Categories
    cat = bb.categories.search_by_id("abcat0101001")

    # 6. Bulk Archives
    all_categories = bb.bulk.archive("categories", "json")
```

### Asynchronous Usage

```python
import asyncio
from bestbuyapi import AsyncBestBuyAPI

async def main():
    async with AsyncBestBuyAPI() as bb:
        # Concurrent API calls
        product_task = bb.products.asearch_by_sku(5985609, format="json")
        trending_task = bb.recommendations.atrending()
        stores_task = bb.stores.asearch_by_postal_code(55423)

        product, trending, stores = await asyncio.gather(
            product_task, trending_task, stores_task
        )
        print(f"Product: {product['products'][0]['name']}")
        print(f"Trending count: {len(trending['results'])}")
        print(f"Stores found: {len(stores['stores'])}")

asyncio.run(main())
```

---

## Deep Pagination & Cursor Streaming

For large query results, use cursor marks to walk the result set efficiently without deep paging overhead:

### Sync Cursor Streaming

```python
with BestBuyAPI() as bb:
    # Streams batches of up to 100 products using cursorMark bookmarks
    for page in bb.products.iter_cursor(query="type=HardGood", page_size=100):
        for item in page.get("products", []):
            print(item["sku"], item.get("name"))
```

### Async Page Streaming

```python
async with AsyncBestBuyAPI() as bb:
    async for page in bb.stores.aiter_pages(query="region=MN", page_size=10, max_pages=3):
        for store in page.get("stores", []):
            print(store["storeId"], store["name"])
```

---

## Error Handling

The library provides granular exception classes:

```python
from bestbuyapi import BestBuyAPI
from bestbuyapi.utils.exceptions import (
    BestBuyAuthenticationError,
    BestBuyNotFoundError,
    BestBuyRateLimitError,
    BestBuyHTTPError,
    BestBuyValidationError,
)

try:
    with BestBuyAPI() as bb:
        bb.products.search_by_sku(12345)
except BestBuyAuthenticationError:
    print("Invalid or missing API key!")
except BestBuyRateLimitError:
    print("API rate limit exceeded. Please back off and retry.")
except BestBuyNotFoundError:
    print("Product not found.")
except BestBuyHTTPError as e:
    print(f"Best Buy HTTP Error ({e.status_code}): {e.message}")
except BestBuyValidationError as e:
    print(f"Invalid parameters: {e}")
```

---

## Development

### Running Tests

```bash
uv run pytest -v --cov=bestbuyapi --cov-report=term-missing
```

### Pre-commit & Linting

```bash
uv run pre-commit run --all-files
uv run ruff check .
uv run ruff format --check .
```

---

## FAQ

- **Is there any difference between `api.bestbuy.com` and `api.remix.bestbuy.com`?**
  No, both serve the same data. `api.bestbuy.com` is the official consolidated endpoint used by this library.

- **Are `bb.category` and `bb.categories` both supported?**
  Yes! `bb.categories` is an ergonomic alias for `bb.category`, and `bb.buying_options` is an alias for `bb.open_box`.

---

Questions or feedback? Feel free to open an issue or reach out at `luis@lv10.me`.
