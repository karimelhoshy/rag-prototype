import os
from typing import List
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    TextLoader
)


class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def load_document(self, file_path: str) -> List[Document]:
        """Load a single document based on file extension."""
        file_extension = Path(file_path).suffix.lower()

        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension in ['.doc', '.docx']:
                loader = Docx2txtLoader(file_path)
            elif file_extension in ['.xls', '.xlsx']:
                loader = UnstructuredExcelLoader(file_path)
            elif file_extension in ['.ppt', '.pptx']:
                loader = UnstructuredPowerPointLoader(file_path)
            elif file_extension == '.txt':
                loader = TextLoader(file_path)
            else:
                print(f"Unsupported file type: {file_extension}")
                return []

            documents = loader.load()
            return documents
        except Exception as e:
            print(f"Error loading document {file_path}: {e}")
            return []

    def process_documents(self, file_paths: List[str]) -> List[Document]:
        """Load and chunk multiple documents."""
        all_documents = []

        for file_path in file_paths:
            print(f"Processing: {file_path}")
            docs = self.load_document(file_path)

            for doc in docs:
                doc.metadata['source'] = file_path
                doc.metadata['filename'] = os.path.basename(file_path)

            all_documents.extend(docs)

        chunked_documents = self.text_splitter.split_documents(all_documents)
        print(f"Created {len(chunked_documents)} chunks from {len(file_paths)} documents")

        return chunked_documents
