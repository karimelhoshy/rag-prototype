from abc import ABC, abstractmethod
from typing import List, Optional
from pathlib import Path


class StorageConnector(ABC):
    @abstractmethod
    def list_files(self, prefix: str = "") -> List[str]:
        """List all files in the storage with optional prefix filter."""
        pass

    @abstractmethod
    def download_file(self, file_path: str, local_path: str) -> str:
        """Download a file from storage to local path."""
        pass

    @abstractmethod
    def download_all(self, local_dir: str, prefix: str = "") -> List[str]:
        """Download all files to local directory."""
        pass
