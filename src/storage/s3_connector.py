import os
from typing import List
import boto3
from botocore.exceptions import ClientError
from .base import StorageConnector
from config import settings


class S3Connector(StorageConnector):
    def __init__(self, bucket_name: str = None):
        self.bucket_name = bucket_name or settings.aws_s3_bucket
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )

    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in S3 bucket."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )

            if 'Contents' not in response:
                return []

            return [obj['Key'] for obj in response['Contents']]
        except ClientError as e:
            print(f"Error listing S3 files: {e}")
            return []

    def download_file(self, file_path: str, local_path: str) -> str:
        """Download a single file from S3."""
        try:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            self.s3_client.download_file(self.bucket_name, file_path, local_path)
            return local_path
        except ClientError as e:
            print(f"Error downloading file {file_path}: {e}")
            return None

    def download_all(self, local_dir: str, prefix: str = "") -> List[str]:
        """Download all files from S3 bucket."""
        files = self.list_files(prefix)
        downloaded = []

        for file_path in files:
            local_path = os.path.join(local_dir, file_path)
            if self.download_file(file_path, local_path):
                downloaded.append(local_path)

        return downloaded
