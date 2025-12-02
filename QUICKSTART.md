# Quick Start Guide

## 5-Minute Setup

### 1. Initial Setup (One Time)

```bash
# Run the setup script
./setup.sh

# OR manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Your Environment

Edit `.env` and add your credentials:

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-...

# Required: ONE of the following cloud storage providers

# Option A: AWS S3
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=my-documents-bucket

# Option B: GCP
GCP_PROJECT_ID=my-project
GCP_BUCKET_NAME=my-documents-bucket
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# Option C: Azure
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
AZURE_CONTAINER_NAME=documents
```

### 3. Upload Your Documents

Upload documents to your cloud storage:
- PDFs, Word docs, Excel sheets, PowerPoint, or text files
- Any folder structure is supported

### 4. Start Using!

#### Option A: Streamlit UI (Recommended)

```bash
streamlit run ui/app.py
```

Then:
1. Select your storage provider (S3/GCP/Azure)
2. Click "Ingest Documents"
3. Click "Initialize Query Engine"
4. Ask questions!

#### Option B: Command Line

```bash
# Ingest documents
python ingest.py --storage s3

# Ask questions
python query.py "What are the main topics covered?"
```

## Common Use Cases

### Use Case 1: Company Knowledge Base

```bash
# Upload all company docs to S3 bucket: company-docs/
# Organize by department:
#   company-docs/hr/
#   company-docs/engineering/
#   company-docs/sales/

# Ingest all documents
python ingest.py --storage s3

# Query
python query.py "What is the vacation policy?"
```

### Use Case 2: Research Papers

```bash
# Upload PDFs to: research-papers/machine-learning/

# Ingest only ML papers
python ingest.py --storage s3 --prefix "research-papers/machine-learning/"

# Ask research questions
python query.py "What are the key findings about transformers?"
```

### Use Case 3: Project Documentation

```bash
# Upload project docs to GCP bucket

# Use Streamlit UI for interactive exploration
streamlit run ui/app.py

# Ask about architecture, APIs, deployment, etc.
```

## Tips & Tricks

### Tip 1: Better Answers

Ask specific questions:
- ✅ "What are the three main features of Product X?"
- ❌ "Tell me about products"

### Tip 2: Finding Sources

In the Streamlit UI, check the "Show context" option to see exactly what documents were retrieved.

### Tip 3: Filtering Documents

Use the prefix parameter to ingest only specific folders:

```bash
# Only ingest Q1 reports
python ingest.py --storage s3 --prefix "reports/2024/Q1/"
```

### Tip 4: Managing the Database

Reset and start fresh:

```bash
# Delete the vector database
rm -rf chroma_db/

# Re-ingest documents
python ingest.py --storage s3
```

### Tip 5: Retrieving More Context

Query with more documents for better context:

```bash
python query.py "complex question" --top-k 10
```

## Troubleshooting

### Error: "No module named 'src'"

Make sure you're in the project root directory:
```bash
cd /path/to/rag-prototype
```

### Error: "OpenAI API key not found"

Check your `.env` file has:
```
OPENAI_API_KEY=sk-your-key-here
```

### Error: "Access Denied" from cloud storage

Verify:
- Your credentials are correct in `.env`
- Your account has read permissions
- The bucket/container exists

### No documents retrieved

- Check documents were successfully ingested (check ChromaDB count in UI)
- Try a more general question
- Increase `--top-k` parameter

### Slow performance

First run is slow because:
1. Downloads embedding model (~100MB)
2. Processes all documents
3. Generates embeddings

Subsequent queries are fast!

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Customize chunk size in `src/ingestion/document_processor.py`
- Change LLM model in `.env` (try `gpt-4` for better answers)
- Experiment with different embedding models

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error messages carefully
3. Ensure all dependencies are installed
4. Verify your `.env` configuration

Happy querying! 🚀
