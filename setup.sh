#!/bin/bash

echo "🚀 Setting up RAG Prototype..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys and credentials"
fi

# Create directories
mkdir -p chroma_db
mkdir -p temp_downloads

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your credentials"
echo "2. Upload documents to your cloud storage"
echo "3. Run: streamlit run ui/app.py"
echo ""
echo "Or use CLI:"
echo "  python ingest.py --storage s3"
echo "  python query.py 'Your question here'"
