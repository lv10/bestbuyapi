import requests

from constants import *

class BestBuyCategoryAPIError(Exception):
    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyCategoryAPI(object):

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
        valid_payload = self._validate_params(payload)
        url, valid_payload = self._build_url(valid_payload)
        request = requests.get(url, params=valid_payload)

        if request.headers['content-type'] == "text/json":
            return request.json()

        return request.content

    def _build_url(self, payload):
        """
            Receives a payload (dict) with all the necessary make a call to
            the Best Buy API and returns a string URL that includes the query
            and the dict parameters pre-processed for a API call to be made.

            :param paylod: dictionary with request parameters

            :rType: tuple that contains the url that includes the query and
                    the parameters pre-processed for a API call to be made.
        """

        query = payload['query']

        # Pre-process paramenters before submitting payload.

        out = dict()

        for key, value in payload['params'].iteritems():
            if type(value) is list:
                out[key] = ",".join(value)
            else:
                out[key] = value

        # Add key to params
        out['apiKey'] = self.api_key

        if len(query) == 0:
            url = BASE_URL + "categories"
        else:
            url = BASE_URL + "categories({0})".format(query)

        return (url, out)

    def _validate_params(self, payload):
        """
            Validate parameters, double check that there are no None values
            in the keys.

            :param payload: dictionary, with the parameters to be used to make
                            a request.
        """

        for key, value in payload['params'].iteritems():

            if (key not in PRODUCT_SEARCH_PARAMS
                    or key not in API_SEARCH_PARAMS):
                err_msg = ("{0} is an invalid Product"
                           " Search Parameter".format(key))
                raise BestBuyProductAPIError(err_msg)

            if value is None:
                err_msg = "Key {0} can't have None for a value".format(key)
                raise BestBuyProductAPIError(err_msg)

        return payload

    # =================================
    #   Search by description or SKU
    # =================================

    def search(self, query, **kwargs):
        """
            Performs a customized search on the BestBuy category API. Query
            parameters should be passed to function in as a string.

            :param query: String with query parameter. For examples of query
                          check BestBuy documenation at https://goo.gl/ZH5mnP
        """

        payload = {
            'query': query,
            'params': kwargs
        }

        return self._call(payload)

    def search_by_id(self, category_id, **kwargs):
        """
            Search the category API by id

            :param id: string, with the id of the desired category.
            :param kwargs: dictionary, with request parameters
        """

        payload = {
            'query': "id={0}".format(category_id),
            'params': kwargs
        }

        return self._call(payload)

    def search_by_name(self, category, **kwargs):
        """
            Search the category API by name

            :param id: string, with the name of the desired category.
            :param kwargs: dictionary, with request parameters
        """

        payload = {
            'query': "id={0}".format(category),
            'params': kwargs
        }

        return self._call(payload)
