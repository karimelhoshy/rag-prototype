import os
import logging
from typing import List
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
from .base import StorageConnector
from config import settings

logger = logging.getLogger(__name__)


class AzureConnector(StorageConnector):
    def __init__(self, container_name: str = None):
        self.container_name = container_name or settings.azure_container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
        self.container_client = self.blob_service_client.get_container_client(
            self.container_name
        )

    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in Azure container."""
        try:
            blobs = self.container_client.list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blobs]
        except AzureError as e:
            logger.error(f"Error listing Azure files: {e}", exc_info=True, extra={"container": self.container_name})
            return []

    def download_file(self, file_path: str, local_path: str) -> str:
        """Download a single file from Azure."""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            blob_client = self.container_client.get_blob_client(file_path)

            with open(local_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())

            return local_path
        except AzureError as e:
            logger.error(f"Error downloading file {file_path}: {e}", exc_info=True)
            return None

    def download_all(self, local_dir: str, prefix: str = "") -> List[str]:
        """Download all files from Azure container."""
        files = self.list_files(prefix)
        downloaded = []

        for file_path in files:
            local_path = os.path.join(local_dir, file_path)
            if self.download_file(file_path, local_path):
                downloaded.append(local_path)

        return downloaded
