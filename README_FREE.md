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

### 1. Install Dependencies

```bash
pip install -r requirements_free.txt
```

**Note:** This will download:
- PyTorch (~2GB)
- Sentence Transformers model (~90MB, downloaded automatically on first use)

### 2. Optional: Install Ollama (for local LLM)

For the best experience, install Ollama for local LLM:

**macOS/Linux:**
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

**Windows:** Download from https://ollama.ai/

If Ollama is not installed, the app will automatically use Hugging Face Inference API (free tier).

### 3. Start the Server

```bash
./start_free.sh
```

Or manually:
```bash
source venv/bin/activate
cd backend
uvicorn main_free:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open Your Browser

Go to: `http://localhost:8000/`

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

## 📝 Notes

- **First run:** The embedding model (~90MB) will be downloaded automatically
- **Memory:** Ollama models need 4-8GB RAM (depending on model size)
- **Internet:** Required only for first download and Hugging Face API
- **Performance:** Local models are fast but may be slightly slower than cloud APIs

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
- Make sure Ollama is running locally
- Close other applications to free up RAM
- Use smaller Ollama models (llama3.2 instead of llama3.1)

### Hugging Face API errors
Some models may be loading. Wait a few seconds and try again, or install Ollama for local use.

---

**Enjoy your FREE AI Chatbot! 🎉**

