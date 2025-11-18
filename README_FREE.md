# AI Chatbot with RAG - FREE VERSION 🆓

**No OpenAI API costs! Uses free, local models.**

This is a completely FREE version that uses:
- **Sentence Transformers** (local embeddings - no API calls)
- **Ollama** (local LLM) or **Hugging Face Inference API** (free tier)

## 🎯 Why FREE Version?

- **No API costs** - everything runs locally or uses free APIs
- **No API keys needed** - completely free to use
- **Privacy** - data stays on your machine (with Ollama)
- **Unlimited usage** - no quotas or rate limits

## 🚀 Quick Start (FREE Version)

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Ollama for best performance - see [INSTALL_OLLAMA.md](INSTALL_OLLAMA.md)

### 1. Clone the Repository

```bash
git clone https://github.com/malberyz7/project.git
cd project
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements_free.txt
```

**Note:** This will download:
- PyTorch (~2GB)
- Sentence Transformers model (`all-MiniLM-L6-v2`, ~90MB, downloaded automatically on first use)

### 4. Optional: Install Ollama (for local LLM)

For the best experience and privacy, install Ollama for local LLM:

**macOS (Recommended):**
```bash
brew install ollama
ollama pull llama3.2
```

**macOS/Linux (Alternative):**
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

**Windows:** Download from https://ollama.ai/

See [INSTALL_OLLAMA.md](INSTALL_OLLAMA.md) for detailed installation instructions.

If Ollama is not installed, the app will automatically use Hugging Face Inference API (free tier).

### 5. Start the Server

```bash
./start_free.sh
```

Or manually:
```bash
source venv/bin/activate
cd backend
uvicorn main_free:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open Your Browser

Go to: `http://localhost:8000/`

**Also available:**
- API Documentation: `http://localhost:8000/docs`
- Status Check: `http://localhost:8000/status`

## 📊 Differences from Paid Version

| Feature | FREE Version | Paid Version |
|---------|--------------|--------------|
| Embeddings | Sentence Transformers (local) | OpenAI API |
| LLM | Ollama local or Hugging Face | OpenAI GPT |
| Cost | $0 | ~$0.01-0.10 per document |
| Speed | Fast (local) | Fast (cloud) |
| Quality | Very Good | Excellent |
| Privacy | High (local) | Medium (cloud) |
| Setup | Requires model download | Just API key |

## 🔧 Configuration

### Using Ollama (Recommended for Privacy)

1. Install Ollama: https://ollama.ai/
2. Download a model: `ollama pull llama3.2`
3. The app will automatically use Ollama if available

### Using Hugging Face (No Installation Needed)

If Ollama is not available, the app automatically uses Hugging Face Inference API:
- No installation required
- Works immediately
- Free tier (may have rate limits)

## 🎯 Features

### Core Capabilities
- ✅ **Document Upload**: Upload PDF or text files easily
- ✅ **Smart Q&A**: Ask questions in natural language
- ✅ **RAG Technology**: Uses Retrieval-Augmented Generation for accurate answers
- ✅ **Source Tracking**: See which document excerpts were used for each answer
- ✅ **File Management**: List and delete uploaded files
- ✅ **Local Processing**: Everything runs locally (with Ollama) or uses free APIs

### API Endpoints

The backend provides a RESTful API:

- `POST /upload` - Upload and process a document
- `POST /ask` - Ask a question about uploaded documents
- `GET /files` - List all uploaded files
- `DELETE /files/{filename}` - Delete a specific file
- `GET /status` - Check server and database status
- `DELETE /clear` - Clear all documents (for testing)

**Interactive API Docs**: Visit `http://localhost:8000/docs` when the server is running!

## 📝 Notes

- **First run:** The embedding model (`all-MiniLM-L6-v2`, ~90MB) will be downloaded automatically
- **Memory:** Ollama models need 4-8GB RAM (depending on model size)
  - `llama3.2`: ~2-3GB RAM
  - `phi3`: ~2-3GB RAM
  - Larger models like `mistral`: 8GB+ RAM
- **Internet:** Required only for first download and Hugging Face API
- **Performance:** Local models are fast but may be slightly slower than cloud APIs
- **Embedding Model:** Uses `all-MiniLM-L6-v2` (384-dimensional embeddings, free and lightweight)

## 🆚 Which Version Should I Use?

### Use FREE Version if:
- ✅ You want zero costs
- ✅ You want privacy (local processing)
- ✅ You have good hardware (4GB+ RAM)
- ✅ You don't mind slightly longer setup

### Use Paid Version if:
- ✅ You want best quality
- ✅ You have OpenAI credits
- ✅ You want cloud-based (no local setup)
- ✅ You need production-grade quality

## 🐛 Troubleshooting

### "Sentence Transformers model not found"
The model downloads automatically on first use. Make sure you have internet connection.

### "Ollama connection failed"
Install Ollama: https://ollama.ai/ or the app will use Hugging Face instead.

### Slow performance
- Make sure Ollama is running locally (`ollama list` should work)
- Close other applications to free up RAM
- Use smaller Ollama models (`llama3.2` or `phi3` instead of larger models)
- First-time processing is slower (embedding model download)

### Hugging Face API errors
- Some models may be loading. Wait a few seconds and try again.
- If you get authentication errors (401), install Ollama for local use instead.
- The app will automatically fall back to Ollama if available.

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill
# Then restart the server
```

### File Deletion Not Working
- Make sure you're using the correct filename (case-sensitive)
- Check that the file exists using `GET /files` endpoint
- Verify the server is running and has write permissions in the `data/` directory

---

**Enjoy your FREE AI Chatbot! 🎉**

