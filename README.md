# Python Best Buy API Wrapper

![image](https://img.shields.io/badge/version-2.1.0-blue.svg)
[![CI](https://github.com/lv10/bestbuyapi/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/lv10/bestbuyapi/actions/workflows/ci.yml)

This is a small python wrapper implementation for BestBuy API.

# Features

- Query Bulk BestBuy API
- Query Stores BestBuy API
- Query Products BestBuy API
- Query Categories BestBuy API
- Obtain queries result in JSON or XML
- Environment variable support via `python-dotenv`
- Modern development workflow with `uv` and `pre-commit`

# Install

We recommend using `uv` for package management:

```bash
uv add bestbuyapi
```

Or with pip:

```bash
pip install bestbuyapi
```

# Configuration

You can use a `.env` file to store your API key:

```env
BESTBUY_API_KEY=your_api_key_here
```

# Usage

```python
from bestbuyapi import BestBuyAPI

# If not provided, it will look for BESTBUY_API_KEY in environment variables
bb = BestBuyAPI()

a_prod = bb.products.search(query="sku=9776457", format="json")
a_cat = bb.category.search_by_id(category_id="abcat0011001", format="json")
all_categories = bb.bulk.archive("categories", "json")
```

# Development

## Running Tests

Tests are executed via `pytest`. We use `pytest-cov` for coverage reporting.

```bash
uv run pytest --cov=bestbuyapi
```

## CI/CD and Coverage

Our CI pipeline in GitHub Actions runs tests across multiple Python versions. Coverage reports are generated during the test phase and can be shared or uploaded to services like Codecov.

## Pre-commit Hooks

We use `pre-commit` to ensure code quality. It runs `ruff` for linting and formatting.

```bash
uv run pre-commit run --all-files
```

# FAQ

- Is there any difference between /api.bestbuy.com/ and api.remix.bestbuy.com?
  A: There is no difference, they serve the same data - we just consolidated domains. The official url to use is api.bestbuy.com.

Any questions please feel free to email me at: luis@lv10.me
