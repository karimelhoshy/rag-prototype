import logging
from typing import List, Dict, Optional
from openai import OpenAI
from src.vectordb import ChromaVectorDB
from config import settings

logger = logging.getLogger(__name__)


class RAGQueryEngine:
    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        top_k: int = 5
    ):
        self.model = model or settings.llm_model
        self.temperature = temperature or settings.llm_temperature
        self.top_k = top_k

        self.client = OpenAI(api_key=settings.openai_api_key)
        self.vector_db = ChromaVectorDB()

    def _build_context(self, query_results: dict) -> str:
        """Build context from retrieved documents."""
        documents = query_results['documents'][0]
        metadatas = query_results['metadatas'][0]

        context_parts = []
        for i, (doc, metadata) in enumerate(zip(documents, metadatas), 1):
            source = metadata.get('filename', 'Unknown')
            context_parts.append(f"[Document {i} - {source}]\n{doc}\n")

        return "\n".join(context_parts)

    def _build_prompt(self, query: str, context: str) -> str:
        """Build the prompt for the LLM."""
        prompt = f"""You are a helpful assistant that answers questions based on the provided context.

Context:
{context}

Question: {query}

Instructions:
- Answer the question using only the information from the context above
- If the context doesn't contain enough information to answer the question, say so
- Be concise and accurate
- Cite the document number when referencing information

Answer:"""
        return prompt

    def query(self, query_text: str) -> Dict[str, any]:
        """Query the RAG system."""
        logger.info(f"Searching for relevant documents...")
        query_results = self.vector_db.query(query_text, n_results=self.top_k)

        if not query_results['documents'][0]:
            logger.warning("No relevant documents found in the database")
            return {
                "answer": "No relevant documents found in the database.",
                "sources": [],
                "query": query_text
            }

        context = self._build_context(query_results)

        prompt = self._build_prompt(query_text, context)

        logger.info(f"Generating answer...")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature
        )

        answer = response.choices[0].message.content

        sources = []
        for metadata in query_results['metadatas'][0]:
            source_info = {
                'filename': metadata.get('filename', 'Unknown'),
                'source': metadata.get('source', 'Unknown')
            }
            if source_info not in sources:
                sources.append(source_info)

        return {
            "answer": answer,
            "sources": sources,
            "query": query_text,
            "context": context
        }
