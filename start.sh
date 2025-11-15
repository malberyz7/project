#!/usr/bin/env bash
# Startup script for AI Chatbot RAG application

set -e

echo "🚀 Starting AI Chatbot RAG Application..."
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
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    if [ -f ".env" ]; then
        echo "🔑 Loading API key from .env file..."
        export $(cat .env | grep -v '^#' | xargs)
    else
        echo "⚠️  WARNING: OPENAI_API_KEY not set!"
        echo "   Please set it in your environment or create a .env file"
        echo "   Example: export OPENAI_API_KEY=your-key-here"
        echo ""
    fi
fi

# Create data directory if it doesn't exist
mkdir -p data

echo ""
echo "✅ Starting backend server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

