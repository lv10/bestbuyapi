Python Best Buy API Wrapper
===========================

.. image:: https://img.shields.io/badge/pypi-2.7-green.svg
    :target: https://pypi.python.org/pypi/BestBuyAPI

.. image:: https://img.shields.io/badge/version-0.5-blue.svg


This is a small python wrapper implementation for BestBuy API. This implementation
does not cover all the APIs from BestBuy yet. As of now, it only supports the
calls to the Products API and Categories API. Locations and Reviews API are in the
making.

The wrapper doesn't assume any design requirements on the user end. Queries to
the API endpoints are done similar to what you would put in the browser with the
convenience of having python prepare for you the query, url, and interpret the
response.

NOTICE: This is a python library in the making. New features and bug fixes will
be included. Feel free to add change anything you consider could be better or
could extend the functionality of the library.

Features
--------

- Query Bulk BestBuy API
- Query Products BestBuy API
- Query Categories BestBuy API
- Obtain queries result in JSON or XML

For details on how to use the Best Buy API go to:
https://developer.bestbuy.com/documentation

Install
-------

.. code-block:: python

    $ pip install BestBuyAPI


How to Product and Category APIs
--------------------------------

.. code-block:: python

    >>> from bestbuy import BestBuyProductsAPI, BestBuyCategoryAPI
    >>> bb_prod = BestBuyProductsAPI("YourSecretAPIKey")
    >>> bb_cat = BestBuyCategoryAPI("YourSecretAPIKey")
    >>>
    >>> bb_prod.search(query="sku=9776457", format="json")
    >>> bb_cat.search_by_id(category_id="abcat0011001", format="json")


How to Bulk API
---------------

.. code-block:: python

    >>> from bestbuy import BestBuyBulkAPI
    >>> import zipfile, StringIO
    >>> #import zipfile, io --> For python 3+
    >>>
    >>> bb_bulk = BestBuyBulkAPI("YourSecretAPIKey")
    >>>
    >>> response = bb_bulk.archive("categories", "json")
    >>> zip_file = zipfile.ZipFile(StringIO.StringIO(response))
    >>> # zip_file = zipfile.ZipFile(io.BytesIO(response)) --> For python 3+
    >>> zip_file.extractall()


FAQ
-------

- Is there any difference between /api.bestbuy.com/ and api.remix.bestbuy.com?

  A:// This is the response from BestBuy Dev department: "There is no difference, they serve the same data - we just consolidated domains. The official url to use is api.bestbuy.com though."


Any questions please feel free to email me at: luis@lv10.me
