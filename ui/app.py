import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ingestion import IngestionPipeline
from src.rag import RAGQueryEngine
from src.vectordb import ChromaVectorDB
from config import settings


st.set_page_config(
    page_title="RAG Document QA System",
    page_icon="📚",
    layout="wide"
)

st.title("📚 RAG Document Question Answering System")

if 'query_engine' not in st.session_state:
    st.session_state.query_engine = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with st.sidebar:
    st.header("⚙️ Configuration")

    st.subheader("1. Document Ingestion")
    storage_type = st.selectbox(
        "Select Storage Provider",
        ["s3", "gcp", "azure"],
        help="Choose your cloud storage provider"
    )

    prefix = st.text_input(
        "Storage Prefix (optional)",
        "",
        help="Filter files by prefix/folder path"
    )

    if st.button("🔄 Ingest Documents", type="primary"):
        with st.spinner("Ingesting documents..."):
            try:
                pipeline = IngestionPipeline(storage_type=storage_type)
                pipeline.run(prefix=prefix)
                st.success("✅ Documents ingested successfully!")

                st.session_state.query_engine = RAGQueryEngine()
            except Exception as e:
                st.error(f"❌ Error during ingestion: {str(e)}")

    st.divider()

    st.subheader("2. Initialize Query Engine")
    if st.button("🚀 Initialize/Reload Query Engine"):
        try:
            st.session_state.query_engine = RAGQueryEngine()
            st.success("✅ Query engine initialized!")
        except Exception as e:
            st.error(f"❌ Error initializing query engine: {str(e)}")

    st.divider()

    st.subheader("📊 Database Stats")
    try:
        vector_db = ChromaVectorDB()
        stats = vector_db.get_collection_stats()
        st.metric("Documents in DB", stats['count'])
        st.info(f"Collection: {stats['name']}")
    except Exception as e:
        st.warning("Unable to fetch stats")

    st.divider()

    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Ask Questions")

    if st.session_state.query_engine is None:
        st.info("👈 Please initialize the query engine from the sidebar first")
    else:
        query = st.text_input(
            "Enter your question:",
            placeholder="What is this document about?",
            key="query_input"
        )

        if st.button("🔍 Ask", type="primary") and query:
            with st.spinner("Searching and generating answer..."):
                try:
                    result = st.session_state.query_engine.query(query)

                    st.session_state.chat_history.append({
                        'query': query,
                        'result': result
                    })

                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with col2:
    st.subheader("ℹ️ About")
    st.markdown("""
    This RAG system allows you to:
    - Ingest documents from cloud storage
    - Ask questions about your documents
    - Get AI-powered answers with sources

    **Supported Storage:**
    - AWS S3
    - GCP Cloud Storage
    - Azure Blob Storage

    **Supported Documents:**
    - PDF, DOCX, TXT
    - Excel, PowerPoint
    """)

st.divider()

if st.session_state.chat_history:
    st.subheader("📝 Chat History")

    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.expander(f"Q: {chat['query']}", expanded=(i == 0)):
            st.markdown("**Answer:**")
            st.write(chat['result']['answer'])

            st.markdown("**Sources:**")
            for source in chat['result']['sources']:
                st.caption(f"📄 {source['filename']}")

            if st.checkbox(f"Show context", key=f"context_{len(st.session_state.chat_history) - i}"):
                st.markdown("**Retrieved Context:**")
                st.text(chat['result']['context'])
else:
    st.info("No questions asked yet. Start by asking a question above!")

st.divider()
st.caption("Powered by OpenAI, ChromaDB, and Streamlit")
