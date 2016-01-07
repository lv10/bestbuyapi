from constants import BULK_API
from main import BestBuyAPI, BestBuyAPIError


class BestBuyBulkAPIError(BestBuyAPIError):

    """
        Errors generated before BestBuy servers respond to a call
    """
    pass


class BestBuyBulkAPI(BestBuyAPI):

    def _api_name(self):
        return BULK_API

    def archive(self, name, file_format):
        """
            BestBuy generates Bulk files (archives) daily at 9:00 AM CST.

            :param name: string, that identifies the archive type. The archive
                         type supported by BestBuy's API are:
                            - products
                            - stores
                            - reviews
                            - categories
                            - storeAvailability
            :param file_format: string, that indicates the file format in which
                                the archive is to be downloaded.
                                 - {xml or json}: Products, Reviews, Stores,
                                                  and Categories
                                 - {tsv} for Store Availability

            BestBuy bulk docs:
             - https://developer.bestbuy.com/documentation/bulkDownload-api
        """

        payload = {
            'query': "{0}.{1}.zip".format(name, file_format),
            'params': {}
        }

        return self._call(payload)

    def archive_subset(self, subset, file_format):
        """
            Bulk files (archives) are generated every day at 9 AM by BestBuy.

            :param name: string, that identifies the archive type. The archive
                         type supported by BestBuy's API are:
                            - productsActive
                            - productsInactive
                            - productsMusic
                            - productsMovie
                            - productsHardgood
                            - productsBundle
                            - productsGame
                            - productsSoftware
                            - productsBlackTie
                            - productsMarketplace
                            - productsDigital

            :param file_format: string, that indicates the file format in which
                                the archive is to be downloaded.
                                 - xml
                                 - json
            BestBuy product subsets bulk docs:
             - https://developer.bestbuy.com/documentation/bulkDownload-api
        """

        payload = {
            'query': "subsets/{0}.{1}.zip".format(subset, file_format),
            'params': {}
        }

        return self._call(payload)
