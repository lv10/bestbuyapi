import requests

from constants import PRODUCT_SEARCH_PARAMS, PRODUCT_DESCRIPTION_TYPES


class BestBuyProductAPIError(Exception):

    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyProductsAPI(object):

    NAME = "name"
    DESCRIPTION = "description"
    SHORT_DESCRIPTION = "shortDescription"
    LONG_DESCRIPTION = "longDescription"

    def __init__(self, api_key):
        """
            :param api_key: best buy developer API key.
        """
        self.api_key = api_key.strip()

    def _call(self, payload):
        """
            Actual call ot the Best Buy API.

            :rType: JSON
        """
        params = self._validate_params(payload)
        url = self._build_url(params)
        request = requests.get(url)

        return request.json()

    def _build_url(self, params):
        """
            Receives a payload (dict) with all the necessary make a call to
            the Best Buy API and returns a string URL to be used to make the
            API call. The API key is added to the request at this point.

            :param paylod: dictionary with request parameters

            :rType: String
        """
        pass

    def _validate_params(self, params):
        """
            Validate parameters, double check that there are no None values
            in the keys.

            :param params: dictionary, with the parameters to be used to make a
                           a request.
        """

        for key, value in params.iteritems():

            if key not in PRODUCT_SEARCH_PARAMS:

                err_msg = "{0} is an invalid Product Search Param".format(key)
                raise BestBuyProductAPIError(err_msg)

            if value is None:
                err_msg = "Key {0} can't have None for a value".format(key)
                raise BestBuyProductAPIError(err_msg)

        return params

    # =================================
    #   Search by description or SKU
    # =================================

    def search_by_description(self, description_type, description, **kwargs):
        """
            Searches the product API using description parameter

            :param description_type: Integer from 1 to 4 to determine the type
                                     of description the call is going to use.
                                     The integers represent:
                                     - 1: name
                                     - 2: description
                                     - 3: shortDescription
                                     - 4: longDescription
            :param description: String with the actual description's content.
        """
        d_type = PRODUCT_DESCRIPTION_TYPES[description_type]
        kwargs[d_type] = description

        return self._call(kwargs)

    def search_by_sku(self, sku, **kwargs):
        """
            Search the product API by SKU

            :param sky: string, with the SKU number of the desired product.
            :param kwargs: dictionary, with request parameters
        """
        kwargs["sku"] = sku

        return self._call(kwargs)
