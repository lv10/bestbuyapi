import requests

from constants import API_SEARCH_PARAMS, BASE_URL, BULK_API


class BestBuyAPIError(Exception):

    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyAPI(object):

    def __init__(self, api_key):
        """
            :param api_key: best buy developer API key.
        """
        self.api_key = api_key.strip()

    def _call(self, payload):
        """
            Actual call ot the Best Buy API.

            :rType:
                - JSON
                - Text/String
        """
        valid_payload = self._validate_params(payload)
        url, valid_payload = self._build_url(valid_payload)
        request = requests.get(url, params=valid_payload)

        if request.headers['content-type'] == "text/json":
            return request.json()

        return request.content

    def _api_name(self):
        return None

    def _build_url(self, payload):
        """
            Receives a payload (dict) with the necessary params to make a call
            to the Best Buy API and returns a string URL that includes the
            query and the dict parameters pre-processed for a API call to be
            made.

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

        if self._api_name() == BULK_API:
            url = BASE_URL + "{0}".format(query)
        else:
            url = BASE_URL + "{0}({1})".format(self._api_name(), query)

        return (url, out)

    def _validate_params(self, payload):
        """
            Validate parameters, double check that there are no None values
            in the keys.

            :param payload: dictionary, with the parameters to be used to make
                            a request.
        """

        for key, value in payload['params'].iteritems():

            if key not in API_SEARCH_PARAMS:
                err_msg = ("{0} is an invalid Product"
                           " Search Parameter".format(key))
                raise BestBuyAPIError(err_msg)

            if value is None:
                err_msg = "Key {0} can't have None for a value".format(key)
                raise BestBuyAPIError(err_msg)

        return payload
