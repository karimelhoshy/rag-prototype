# RAG Prototype - Document Question Answering System

A Retrieval-Augmented Generation (RAG) system that ingests documents from cloud storage (AWS S3, GCP, Azure Blob), creates embeddings, stores them in a vector database, and provides a Streamlit UI for querying documents.

## Features

- **Multi-Cloud Support**: Ingest documents from AWS S3, GCP Cloud Storage, or Azure Blob Storage
- **Document Processing**: Support for PDF, DOCX, TXT, Excel, and PowerPoint files
- **Vector Database**: Uses ChromaDB for efficient similarity search
- **Embeddings**: Leverages sentence-transformers for document embeddings
- **LLM Integration**: Uses OpenAI GPT models for question answering
- **Interactive UI**: Streamlit-based web interface for easy querying
- **CLI Tools**: Command-line scripts for ingestion and querying

## Project Structure

```
rag-prototype/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── src/
│   ├── storage/
│   │   ├── base.py          # Storage connector interface
│   │   ├── s3_connector.py  # AWS S3 connector
│   │   ├── gcp_connector.py # GCP Storage connector
│   │   └── azure_connector.py # Azure Blob connector
│   ├── ingestion/
│   │   ├── document_processor.py  # Document loading and chunking
│   │   └── ingestion_pipeline.py  # End-to-end ingestion pipeline
│   ├── vectordb/
│   │   └── chroma_db.py     # ChromaDB integration
│   └── rag/
│       └── query_engine.py  # RAG query engine
├── ui/
│   └── app.py               # Streamlit UI
├── ingest.py                # CLI ingestion script
├── query.py                 # CLI query script
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-prototype
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Choose ONE cloud storage provider and configure:

# Option 1: AWS S3
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket-name

# Option 2: GCP Cloud Storage
GCP_PROJECT_ID=your-project-id
GCP_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Option 3: Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
AZURE_CONTAINER_NAME=your-container-name
```

### 5. Upload Documents to Cloud Storage

Upload your documents (PDF, DOCX, TXT, etc.) to your chosen cloud storage:

- **AWS S3**: Upload to your S3 bucket
- **GCP**: Upload to your Cloud Storage bucket
- **Azure**: Upload to your Blob container

## Usage

### Method 1: Streamlit UI (Recommended)

Start the Streamlit application:

```bash
streamlit run ui/app.py
```

This will open a web interface where you can:
1. Select your storage provider (S3, GCP, or Azure)
2. Optionally specify a prefix to filter files
3. Click "Ingest Documents" to process and index your documents
4. Initialize the query engine
5. Ask questions about your documents

### Method 2: Command Line Interface

#### Ingest Documents

```bash
# Ingest from AWS S3
python ingest.py --storage s3

# Ingest from GCP with prefix filter
python ingest.py --storage gcp --prefix "documents/reports/"

# Ingest from Azure
python ingest.py --storage azure
```

#### Query Documents

```bash
python query.py "What are the key findings in the report?"

# Retrieve more documents for context
python query.py "Summarize the main topics" --top-k 10
```

## How It Works

1. **Document Ingestion**:
   - Downloads documents from cloud storage
   - Loads and parses documents based on file type
   - Splits documents into chunks (default: 1000 chars with 200 char overlap)
   - Generates embeddings using sentence-transformers
   - Stores embeddings in ChromaDB

2. **Query Process**:
   - User submits a question
   - Question is embedded using the same model
   - ChromaDB retrieves the most similar document chunks
   - Retrieved chunks are used as context for the LLM
   - OpenAI GPT generates an answer based on the context
   - Answer and sources are returned to the user

## Configuration Options

All settings can be configured via environment variables or by editing [config/settings.py](config/settings.py):

- `EMBEDDING_MODEL`: Sentence transformer model (default: "all-MiniLM-L6-v2")
- `LLM_MODEL`: OpenAI model (default: "gpt-3.5-turbo")
- `LLM_TEMPERATURE`: Response creativity (default: 0.7)
- `CHROMA_PERSIST_DIRECTORY`: Vector DB storage location (default: "./chroma_db")
- `COLLECTION_NAME`: ChromaDB collection name (default: "documents")

## Supported File Types

- PDF (.pdf)
- Word Documents (.doc, .docx)
- Text Files (.txt)
- Excel Spreadsheets (.xls, .xlsx)
- PowerPoint Presentations (.ppt, .pptx)

## Requirements

- Python 3.8+
- OpenAI API key
- Access to at least one cloud storage provider (AWS/GCP/Azure)

## Troubleshooting

### No documents ingested

- Verify your cloud storage credentials in `.env`
- Check that files exist in your bucket/container
- Ensure you have proper permissions to read from storage

### Embedding errors

- The first run will download the sentence-transformers model (can take a few minutes)
- Ensure you have sufficient disk space

### OpenAI API errors

- Verify your `OPENAI_API_KEY` is valid
- Check your OpenAI account has available credits
- Ensure you're using a supported model

### GCP Authentication

For GCP, you need a service account JSON file:
1. Create a service account in GCP Console
2. Download the JSON key file
3. Set `GOOGLE_APPLICATION_CREDENTIALS` to the file path

## Cost Considerations

- **OpenAI API**: Charges based on tokens used (embeddings + completions)
- **Cloud Storage**: Minimal costs for storage and data transfer
- **Local Storage**: ChromaDB stores embeddings locally (can grow large with many documents)

## Future Enhancements

- [ ] Support for more document types (HTML, Markdown, CSV)
- [ ] Multiple vector database backends (Pinecone, Weaviate)
- [ ] Support for local LLMs (Ollama, llama.cpp)
- [ ] Conversation memory for multi-turn dialogues
- [ ] Document update and deletion capabilities
- [ ] Authentication and user management
- [ ] Batch processing for large document sets

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
