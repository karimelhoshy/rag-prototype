from typing import List, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from langchain.docstore.document import Document
from config import settings


class ChromaVectorDB:
    def __init__(
        self,
        collection_name: str = None,
        persist_directory: str = None,
        embedding_model_name: str = None
    ):
        self.collection_name = collection_name or settings.collection_name
        self.persist_directory = persist_directory or settings.chroma_persist_directory
        self.embedding_model_name = embedding_model_name or settings.embedding_model

        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        self.client = chromadb.Client(ChromaSettings(
            persist_directory=self.persist_directory,
            anonymized_telemetry=False
        ))

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector database."""
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        embeddings = self.embedding_model.encode(texts).tolist()

        ids = [f"doc_{i}" for i in range(len(documents))]

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Added {len(documents)} documents to vector database")

    def query(
        self,
        query_text: str,
        n_results: int = 5
    ) -> dict:
        """Query the vector database."""
        query_embedding = self.embedding_model.encode([query_text]).tolist()

        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results

    def delete_collection(self) -> None:
        """Delete the collection."""
        self.client.delete_collection(self.collection_name)
        print(f"Deleted collection: {self.collection_name}")

    def get_collection_stats(self) -> dict:
        """Get statistics about the collection."""
        return {
            "name": self.collection_name,
            "count": self.collection.count()
        }
