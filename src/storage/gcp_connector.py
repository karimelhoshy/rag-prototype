import os
import logging
from typing import List
from google.cloud import storage
from google.api_core.exceptions import GoogleAPIError
from .base import StorageConnector
from config import settings

logger = logging.getLogger(__name__)


class GCPConnector(StorageConnector):
    def __init__(self, bucket_name: str = None):
        self.bucket_name = bucket_name or settings.gcp_bucket_name

        if settings.google_application_credentials:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.google_application_credentials

        self.client = storage.Client(project=settings.gcp_project_id)
        self.bucket = self.client.bucket(self.bucket_name)

    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in GCP bucket."""
        try:
            blobs = self.bucket.list_blobs(prefix=prefix)
            return [blob.name for blob in blobs]
        except GoogleAPIError as e:
            logger.error(f"Error listing GCP files: {e}", exc_info=True, extra={"bucket": self.bucket_name})
            return []

    def download_file(self, file_path: str, local_path: str) -> str:
        """Download a single file from GCP."""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            blob = self.bucket.blob(file_path)
            blob.download_to_filename(local_path)
            return local_path
        except GoogleAPIError as e:
            logger.error(f"Error downloading file {file_path}: {e}", exc_info=True)
            return None

    def download_all(self, local_dir: str, prefix: str = "") -> List[str]:
        """Download all files from GCP bucket."""
        files = self.list_files(prefix)
        downloaded = []

        for file_path in files:
            local_path = os.path.join(local_dir, file_path)
            if self.download_file(file_path, local_path):
                downloaded.append(local_path)

        return downloaded
