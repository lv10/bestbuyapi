import json
import zipfile
from io import BytesIO

from ..constants import BULK_API
from ..api.base import BestBuyCore
from ..utils.exceptions import BestBuyBulkAPIError


class BestBuyBulkAPI(BestBuyCore):
    def _api_name(self):
        return BULK_API

    def archive(self, name, file_format):
        """BestBuy generates Bulk files (archives) daily at 9:00 AM CST.
        :params:
            :name (str): Archive type. The type supported by BestBuy's API are:
                - products
                - stores
                - reviews
                - categories
                - storeAvailability
            :file_format (str): File format in which the archive is to be downloaded.
                - {xml or json}: Products, Reviews, Stores, and Categories
                - {tsv} for Store Availability
        :returns: Unzipped files from Best Buy's API response
        :rType: dict

        BestBuy bulk docs:
            - https://developer.bestbuy.com/documentation/bulkDownload-api
        """
        payload = {"query": f"{name}.{file_format}.zip", "params": {}}
        response = self._call(payload)
        return self._load_zipped_response(response, file_format)

    def archive_subset(self, subset, file_format):
        """Bulk files (archives) are generated every day at 9 AM by BestBuy.

        :params:
            :name (str): Archive type. The archive type supported are:
                - productsActive
                - productsInactive (Currently empty or deprecated)
                - productsMusic (Currently empty or deprecated)
                - productsMovie (Currently empty or deprecated)
                - productsHardgood (Currently empty or deprecated)
                - productsBundle (Currently empty or deprecated)
                - productsGame (Currently empty or deprecated)
                - productsSoftware (Currently empty or deprecated)
                - productsBlackTie (Currently empty or deprecated)
                - productsMarketplace (Currently empty or deprecated)
                - productsDigital (Currently empty or deprecated)

            :file_format (str): File format in which the archive is to be downloaded.
                - xml
                - json

        BestBuy product subsets bulk docs:
            - https://developer.bestbuy.com/documentation/bulkDownload-api
        """
        payload = {"query": f"subsets/{subset}.{file_format}.zip", "params": {}}
        response = self._call(payload)
        return self._load_zipped_response(response, file_format)

    def _load_zipped_response(self, zipped_response, file_format):
        if zipfile.is_zipfile(BytesIO(zipped_response)):
            with zipfile.ZipFile(BytesIO(zipped_response), "r") as z:
                out = {}
                for filename in z.namelist():
                    with z.open(filename) as f:
                        data = f.read()
                        if file_format == "json":
                            out[filename] = json.loads(data)
                        else:
                            out[filename] = data
                return out
