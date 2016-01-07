from main import BestBuyAPI, BestBuyAPIError
from constants import PRODUCT_DESCRIPTION_TYPES, PRODUCT_API


class BestBuyProductAPIError(BestBuyAPIError):

    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyProductsAPI(BestBuyAPI):

    def _api_name(self):
        return PRODUCT_API

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

        payload = {
            'query': "{0}={1}".format(d_type, description),
            'params': kwargs
        }

        return self._call(payload)

    def search_by_sku(self, sku, **kwargs):
        """
            Search the product API by SKU

           :param sky: string, with the SKU number of the desired product.
           :param kwargs: dictionary, with request parameters
        """
        payload = {
            'query': "sku={0}".format(sku),
            'params': kwargs
        }

        return self._call(payload)

    def search_by_review_criteria(self, review_type, review, **kwargs):
        """
            Searches the product API using the Review criteria.

            :param review_type: Integer, with customer review type the API
                                call will use.
                                The integer represent:
                                - 1: "customerReviewAverage"
                                - 2: "customerReviewCount"
            :param review: Float, with the actual value of the review to be
                           criteria to be search for.
                           - customerReviewAverage: should be a number  between
                             0.0 and 5.0
                           - customerReviewCount: should be a number  which is
                             greater than 0.

        """

        if review_type == 2:
            review = int(review)

        payload = {
            'query': "{0}={1}".format(review_type, review),
            'params': kwargs
        }

        return self._call(payload)

    # =================================
    #         Custome Search
    # =================================

    def search(self, query, **kwargs):
        """
            Performs a customized search on the BestBuy product API. Query
            parameters should be passed to function in a dictionary.

            :param query: String with query parameter. For examples of query
                          check BestBuy documenation at https://goo.gl/jWboE2

        """

        payload = {
            'query': query,
            'params': kwargs
        }

        return self._call(payload)
