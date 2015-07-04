Python Best Buy API Wrapper
===========================

.. image:: https://img.shields.io/badge/pypi-2.7-green.svg
    :target: https://pypi.python.org/pypi/BestBuyAPI

.. image:: https://img.shields.io/badge/version-0.4-blue.svg


This is a small python wrapper implementation for BestBuy API. The Wrapper is not
does not cover all the API's from BestBuy yet. As of now, it only supports the
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

- Query the Products BestBuy API
- Query the Categories BestBuy API
- Obtain queries result in JSON or XML

For details on how to use the Best Buy API go to:
https://developer.bestbuy.com/documentation

How to
-------

.. code-block:: python

    >>> import bestbuy
    >>> from bestbuy import BestBuyProductsAPI
    >>> bb = BestBuyProductsAPI("YourSecretAPIKey")
    >>>
    >>> bb.search(query="sku=9776457", format="json", show=id)

Any questions please feel free to email me at: luis@lv10.me
