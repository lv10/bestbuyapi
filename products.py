import requests
from config import APIKEY


class BestBuyProductAPIError(Exception):

    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyProductsAPI(object):

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
            if value is None:
                err_msg = "Key {0} can't have None for a value".format(key)
                raise BestBuyProductAPIError(err_msg)

        return params

    # =================================
    #   Search by description or SKU
    # =================================

    def search_by_description(self, description_type, **kwargs):
        pass
