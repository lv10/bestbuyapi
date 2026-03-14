import json
import zipfile
from io import BytesIO
from typing import Any, Dict

from ..api.base import BestBuyCore
from ..constants import BULK_API


class BestBuyBulkAPI(BestBuyCore):
    def _api_name(self) -> str:
        return BULK_API

    def archive(self, name: str, file_format: str) -> Dict[str, Any]:
        """BestBuy generates Bulk files (archives) daily at 9:00 AM CST.
        :params:
            :name (str): Archive type.
            :file_format (str): File format in which the archive is to be downloaded.
        """
        payload = {"query": f"{name}.{file_format}.zip", "params": {}}
        response = self._call(payload)
        return self._load_zipped_response(response, file_format)

    async def aarchive(self, name: str, file_format: str) -> Dict[str, Any]:
        """Async version of archive"""
        payload = {"query": f"{name}.{file_format}.zip", "params": {}}
        response = await self._acall(payload)
        return self._load_zipped_response(response, file_format)

    def archive_subset(self, subset: str, file_format: str) -> Dict[str, Any]:
        """Bulk files (archives) are generated every day at 9 AM by BestBuy."""
        payload = {"query": f"subsets/{subset}.{file_format}.zip", "params": {}}
        response = self._call(payload)
        return self._load_zipped_response(response, file_format)

    async def aarchive_subset(self, subset: str, file_format: str) -> Dict[str, Any]:
        """Async version of archive_subset"""
        payload = {"query": f"subsets/{subset}.{file_format}.zip", "params": {}}
        response = await self._acall(payload)
        return self._load_zipped_response(response, file_format)

    def _load_zipped_response(
        self, zipped_response: bytes, file_format: str
    ) -> Dict[str, Any]:
        if not zipfile.is_zipfile(bio := BytesIO(zipped_response)):
            return {}

        with zipfile.ZipFile(bio, "r") as z:
            out = {}
            for filename in z.namelist():
                with z.open(filename) as f:
                    data = f.read()
                    if file_format == "json":
                        out[filename] = json.loads(data)
                    else:
                        out[filename] = data
            return out
