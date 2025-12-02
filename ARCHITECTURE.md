# RAG Prototype - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Cloud Storage                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐              │
│  │  AWS S3  │    │   GCP    │    │ Azure Blob   │              │
│  └─────┬────┘    └─────┬────┘    └──────┬───────┘              │
└────────┼───────────────┼─────────────────┼──────────────────────┘
         │               │                 │
         └───────────────┴─────────────────┘
                         │
                    [Download]
                         │
                         ▼
         ┌───────────────────────────────┐
         │   Document Processor          │
         │  - PDF, DOCX, TXT, XLSX, PPTX│
         │  - Text Chunking (1000 chars) │
         └───────────┬───────────────────┘
                     │
                [Chunks]
                     │
                     ▼
         ┌───────────────────────────────┐
         │   Embedding Model             │
         │  (sentence-transformers)      │
         │   all-MiniLM-L6-v2            │
         └───────────┬───────────────────┘
                     │
                [Vectors]
                     │
                     ▼
         ┌───────────────────────────────┐
         │   ChromaDB                    │
         │   Vector Database             │
         │   (Local Storage)             │
         └───────────┬───────────────────┘
                     │
                     │
    ┌────────────────┴────────────────┐
    │                                 │
    ▼                                 ▼
┌────────────┐              ┌─────────────────┐
│ Streamlit  │              │   CLI Tools     │
│    UI      │              │  - ingest.py    │
│            │              │  - query.py     │
└─────┬──────┘              └────────┬────────┘
      │                              │
      └──────────────┬───────────────┘
                     │
                [Query]
                     │
                     ▼
         ┌───────────────────────────────┐
         │   RAG Query Engine            │
         │  1. Embed query               │
         │  2. Similarity search         │
         │  3. Retrieve context          │
         │  4. Generate answer           │
         └───────────┬───────────────────┘
                     │
                [Context]
                     │
                     ▼
         ┌───────────────────────────────┐
         │   OpenAI GPT                  │
         │   (gpt-3.5-turbo)             │
         │   Generate Answer             │
         └───────────┬───────────────────┘
                     │
                [Answer]
                     │
                     ▼
              ┌─────────────┐
              │    User     │
              └─────────────┘
```

## Component Details

### 1. Storage Connectors (`src/storage/`)

**Purpose**: Abstract interface for downloading documents from different cloud providers

**Components**:
- `base.py`: Abstract base class defining the interface
- `s3_connector.py`: AWS S3 implementation
- `gcp_connector.py`: GCP Cloud Storage implementation
- `azure_connector.py`: Azure Blob Storage implementation

**Operations**:
- List files in storage
- Download single file
- Download all files with prefix filter

### 2. Document Processor (`src/ingestion/`)

**Purpose**: Load and chunk documents for embedding

**Components**:
- `document_processor.py`: Document loading and text splitting
- `ingestion_pipeline.py`: Orchestrates the full ingestion flow

**Features**:
- Multi-format support (PDF, DOCX, TXT, XLSX, PPTX)
- Configurable chunking (size: 1000, overlap: 200)
- Metadata preservation (source, filename)

### 3. Vector Database (`src/vectordb/`)

**Purpose**: Store and retrieve document embeddings

**Components**:
- `chroma_db.py`: ChromaDB wrapper

**Features**:
- Persistent storage
- Similarity search
- Collection management

### 4. RAG Query Engine (`src/rag/`)

**Purpose**: Retrieve relevant documents and generate answers

**Components**:
- `query_engine.py`: Main RAG logic

**Flow**:
1. Embed user query
2. Retrieve top-k similar chunks from ChromaDB
3. Build context from retrieved chunks
4. Send query + context to LLM
5. Return answer with sources

### 5. User Interfaces

#### Streamlit UI (`ui/app.py`)
- Interactive web interface
- Document ingestion controls
- Chat interface
- Source citation display

#### CLI Tools
- `ingest.py`: Command-line ingestion
- `query.py`: Command-line querying

## Data Flow

### Ingestion Flow

```
Cloud Storage → Download → Parse → Chunk → Embed → Store in ChromaDB
```

### Query Flow

```
User Query → Embed → Similarity Search → Retrieve Context → LLM → Answer
```

## Configuration (`config/settings.py`)

Centralized configuration using Pydantic Settings:
- Cloud credentials
- Model selection
- Database settings
- LLM parameters

Environment variables loaded from `.env` file.

## Key Technologies

- **LangChain**: Document loading and text splitting
- **sentence-transformers**: Lightweight, local embeddings
- **ChromaDB**: Open-source vector database
- **OpenAI**: GPT models for answer generation
- **Streamlit**: Web UI framework
- **boto3**: AWS SDK
- **google-cloud-storage**: GCP SDK
- **azure-storage-blob**: Azure SDK

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **Cloud Credentials**: IAM/Service Account based authentication
3. **Local Storage**: ChromaDB persisted locally
4. **Network**: HTTPS for all cloud API calls

## Scalability Notes

**Current Design**:
- Local ChromaDB (single machine)
- Synchronous processing
- Suitable for: Small to medium document sets (< 10k documents)

**For Production Scale**:
- Replace ChromaDB with managed vector DB (Pinecone, Weaviate)
- Add async processing for large batches
- Implement document deduplication
- Add monitoring and logging
- Consider distributed embedding generation

## Cost Optimization

1. **Embeddings**: Use local sentence-transformers (free)
2. **Vector DB**: ChromaDB is free and local
3. **LLM**: Only pay for OpenAI API calls during queries
4. **Storage**: Minimal - only document downloads are charged

**Estimated Costs** (1000 documents, 100 queries/month):
- OpenAI API: ~$5-10/month
- Cloud Storage: < $1/month
- Infrastructure: $0 (runs locally)
