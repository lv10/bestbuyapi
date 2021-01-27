class BestBuyAPIError(Exception):
    """Errors generated before BestBuy servers respond to a call"""

    pass


class BestBuyProductAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a call"""

    pass


class BestBuyCategoryAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a call"""

    pass


class BestBuyBulkAPIError(BestBuyAPIError):
    """Errors generated before BestBuy servers respond to a call"""

    pass


class BestBuyStoresAPIError(BestBuyAPIError):
    """Errors before BestBuy servers respond to a call to the stores API"""

    pass
