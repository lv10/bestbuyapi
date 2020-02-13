Python Best Buy API Wrapper
===========================

.. image:: https://img.shields.io/badge/version-1.0.0-blue.svg
.. image:: https://travis-ci.com/lv10/bestbuyapi.svg?branch=master
    :target: https://travis-ci.com/lv10/bestbuyapi


This is a small python wrapper implementation for BestBuy API. This implementation
does not cover all the APIs from BestBuy yet. As of now, it only supports the
calls to the Products, Categories, bulk and Cover APIs. Locations and Reviews API are in the
making.

The wrapper doesn't assume any design requirements on the user end. Queries to
the API endpoints are done similar to what you would put in the browser with the
convenience of having python prepare for you the query, url, and interpret the
response.

NOTICE: This project is only supported by python 3.6, 3.7, 3.8. If you need support for
an older version of python3, please reach out to me.

Features
--------

- Query Bulk BestBuy API
- Query Stores BestBuy API (by id, currently)
- Query Products BestBuy API
- Query Categories BestBuy API
- Obtain queries result in JSON or XML

For details on how to use the Best Buy API go to:
https://developer.bestbuy.com/documentation

Install
-------

.. code-block:: python

    $ pip install BestBuyAPI


How to use Product, Category, Store and Bulk APIs
--------------------------------

.. code-block:: python

    >>> from bestbuy import BestBuy
    >>> bb = BestBuy("YourSecretAPIKey")
    >>>
    >>> a_prod = bb.products.search(query="sku=9776457", format="json")
    >>> a_cat = bb.category.search_by_id(category_id="abcat0011001", format="json")
    >>> all_categories = bb.bulk.archive("categories", "json")


FAQ
-------

- Is there any difference between /api.bestbuy.com/ and api.remix.bestbuy.com?

  A:// This is the response from BestBuy Dev department: "There is no difference, they serve the same data - we just consolidated domains. The official url to use is api.bestbuy.com though."


Any questions please feel free to email me at: luis@lv10.me
