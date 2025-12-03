import os
import shutil
import logging
from typing import List, Optional
from .document_processor import DocumentProcessor
from src.storage import StorageConnector, S3Connector, GCPConnector, AzureConnector
from src.vectordb import ChromaVectorDB

logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(
        self,
        storage_type: str = "s3",
        temp_dir: str = "./temp_downloads"
    ):
        self.storage_type = storage_type.lower()
        self.temp_dir = temp_dir
        self.document_processor = DocumentProcessor()
        self.vector_db = ChromaVectorDB()

        self.storage_connector = self._get_storage_connector()

    def _get_storage_connector(self) -> StorageConnector:
        """Get the appropriate storage connector."""
        if self.storage_type == "s3":
            return S3Connector()
        elif self.storage_type == "gcp":
            return GCPConnector()
        elif self.storage_type == "azure":
            return AzureConnector()
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")

    def run(self, prefix: str = "") -> None:
        """Run the complete ingestion pipeline."""
        try:
            os.makedirs(self.temp_dir, exist_ok=True)

            logger.info(f"Downloading files from {self.storage_type}...")
            downloaded_files = self.storage_connector.download_all(
                self.temp_dir,
                prefix=prefix
            )

            if not downloaded_files:
                logger.warning("No files downloaded. Check your storage configuration.")
                return

            logger.info(f"Downloaded {len(downloaded_files)} files")

            logger.info("Processing documents...")
            chunked_documents = self.document_processor.process_documents(
                downloaded_files
            )

            if not chunked_documents:
                logger.warning("No documents processed.")
                return

            logger.info("Adding documents to vector database...")
            self.vector_db.add_documents(chunked_documents)

            stats = self.vector_db.get_collection_stats()
            logger.info(f"Ingestion complete! Collection '{stats['name']}' now has {stats['count']} documents")

        finally:
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
