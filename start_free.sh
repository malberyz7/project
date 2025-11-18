#!/usr/bin/env bash
# Startup script for AI Chatbot RAG application - FREE VERSION (no OpenAI costs)

set -e

echo "🚀 Starting AI Chatbot RAG Application (FREE VERSION - no OpenAI costs)..."
echo ""
echo "This version uses:"
echo "  - Sentence Transformers (local embeddings - FREE)"
echo "  - Ollama or Hugging Face (FREE LLM)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed_free" ]; then
    echo "📥 Installing FREE dependencies (this may take a few minutes for torch and sentence-transformers)..."
    pip install -r requirements_free.txt
    touch venv/.installed_free
fi

# Create data directory if it doesn't exist
mkdir -p data

echo ""
echo "✅ Starting backend server (FREE VERSION)..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
echo "Note: First time using embeddings will download the model (~90MB)"
echo "      This only happens once."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
cd backend
uvicorn main_free:app --reload --host 0.0.0.0 --port 8000

