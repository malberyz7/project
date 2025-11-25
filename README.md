# 🤖 AI Chatbot with RAG - Document Q&A System

A powerful AI-powered chatbot that answers questions about your uploaded documents using Retrieval-Augmented Generation (RAG). Upload PDFs, ask questions, and get intelligent answers! 

**Includes both FREE and paid versions** - the free version uses local models with zero API costs, while the paid version uses OpenAI for premium quality.

---

## ✨ What Does This Project Do?

Imagine having a smart assistant that has read all your documents and can answer any question about them instantly. That's exactly what this project does!

**Simply put:**
- 📄 Upload your PDF documents
- 💬 Ask questions in natural language
- 🤖 Get accurate answers based on your documents
- 🆓 **100% free** - no OpenAI costs, no API fees!

---

## 🌟 Why Is This Useful?

### For Students
- Upload textbooks, lecture notes, or research papers
- Ask questions and get instant answers
- Perfect for studying and exam preparation

### For Professionals
- Process company documents, reports, or manuals
- Quick access to information without reading everything
- Great for onboarding and knowledge management

### For Everyone
- No subscription fees or API costs
- Your data stays private (runs locally)
- Works offline after setup
- Unlimited usage!

---

## 🚀 Key Features

### 🎯 Core Capabilities
- **Document Upload**: Upload PDF files
- **Smart Q&A**: Ask questions in natural language
- **RAG Technology**: Uses Retrieval-Augmented Generation for accurate answers
- **Source Tracking**: See which document excerpts were used for each answer

### 💰 100% Free
- **Local Embeddings**: Uses Sentence Transformers (no API calls)
- **Local LLM**: Uses Ollama for free, local language models
- **No Limits**: No rate limits or usage quotas
- **Privacy First**: Your documents never leave your machine

### 🎨 User-Friendly Interface
- Clean, modern web interface
- Drag-and-drop file upload
- Real-time chat experience
- Uploaded files management with delete option

### 🛠️ Developer-Friendly
- FastAPI backend with automatic API docs
- Modular, well-commented code
- Easy to extend and customize
- Complete error handling

---

## 🔧 How It Works

### The Magic Behind the Scenes

1. **Upload & Process**
   - You upload a PDF 
   - The system extracts all text from your document
   - Text is split into smaller, manageable chunks
   - Each chunk is converted into a mathematical representation (embedding)

2. **Storage**
   - Embeddings are stored in a FAISS vector database
   - This allows for super-fast similarity searches
   - Your original text chunks are kept for reference

3. **Question Answering**
   - When you ask a question, it's also converted to an embedding
   - The system searches for the most relevant document chunks
   - Those chunks are sent to an AI language model (LLM)
   - The LLM generates an answer based on the context
   - You get the answer plus the source excerpts!

### Technology Stack

- **Backend**: FastAPI (modern, fast Python web framework)
- **Frontend**: Clean HTML/CSS/JavaScript (no complex frameworks needed)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: Sentence Transformers (local, free)
- **LLM**: Ollama (local) or Hugging Face API (free tier)
- **PDF Processing**: PyPDF2

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- (Optional) Ollama for best performance - [Install Guide](INSTALL_OLLAMA.md)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/malberyz7/project.git
   cd project
   ```
   
   Or if you already have it:
   ```bash
   cd project-1  # or whatever you named the folder
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_free.txt
   ```

4. **Install Ollama** (optional but recommended)
   ```bash
   # macOS
   brew install ollama
   
   # Or download from https://ollama.ai/
   ```

5. **Download a language model** (if using Ollama)
   ```bash
   ollama pull llama3.2
   ```

6. **Start the server**
   ```bash
   ./start_free.sh
   ```
   
   Or manually:
   ```bash
   source venv/bin/activate
   cd backend
   uvicorn main_free:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Open your browser**
   - Navigate to: `http://localhost:8000/`
   - Start uploading and asking questions! 🎉

---

## 🎯 Usage

### Step 1: Upload Documents
1. Click on the upload area (shows "Upload PDF")
2. Select a PDF or text file from your computer
3. Wait for processing (usually just a few seconds)
4. See confirmation that your document is ready
5. Uploaded files appear in the "Uploaded Files" section below

### Step 2: Ask Questions
1. Type your question in the input box
2. Press Enter or click "Ask"
3. Get instant answers based on your documents!

### Step 3: Manage Files
- View all uploaded files in the "Uploaded Files" section
- Delete any file with the 🗑️ button
- Upload multiple files and ask questions across all of them

---

## 🎨 Screenshots

**Upload Interface**: Drag and drop your PDF files easily  
**Chat Interface**: Ask questions and get intelligent answers  
**File Management**: View and manage all your uploaded documents

---

## 🔍 API Endpoints

The backend provides a RESTful API. **Note:** Some endpoints are only available in the free version:

### Common Endpoints (Both Versions)
- `POST /upload` - Upload and process a document
- `POST /ask` - Ask a question about uploaded documents
- `GET /status` - Check server and database status
- `DELETE /clear` - Clear all documents (for testing)

### Free Version Only (`main_free.py`)
- `GET /files` - List all uploaded files with details
- `DELETE /files/{filename}` - Delete a specific file and its chunks

**Interactive API Docs**: Visit `http://localhost:8000/docs` when the server is running!

---

## 🆚 Free vs Paid Version

We provide two versions:

### 🆓 Free Version (Recommended)
- **Location**: `backend/main_free.py`
- **Embeddings**: Sentence Transformers (local)
- **LLM**: Ollama (local) or Hugging Face (free)
- **Cost**: $0
- **Privacy**: High (local processing)
- **Setup**: Requires model download (~90MB for embeddings, ~2GB for Ollama)
- **Features**: Includes file management endpoints (`GET /files`, `DELETE /files/{filename}`)

### 💳 Paid Version (Optional)
- **Location**: `backend/main.py`
- **Embeddings**: OpenAI API (requires `OPENAI_API_KEY`)
- **LLM**: OpenAI GPT (requires `OPENAI_API_KEY`)
- **Cost**: ~$0.01-0.10 per document
- **Privacy**: Medium (cloud processing)
- **Setup**: Just needs API key in `.env` file
- **Features**: Basic endpoints only (no file management endpoints)

**The free version is fully functional and recommended for most users!**

---

## 📁 Project Structure

```
project-1/
├── backend/
│   ├── main.py              # Paid version (OpenAI)
│   └── main_free.py         # Free version (local models) ⭐ Recommended
├── frontend/
│   ├── index.html           # Main web interface
│   ├── styles.css           # Beautiful styling
│   └── app.js               # Frontend logic
├── utils/
│   ├── __init__.py          # Package initialization
│   ├── pdf_extractor.py     # PDF text extraction
│   ├── text_processor.py    # Text chunking utilities
│   ├── embeddings_free.py   # Free embeddings (Sentence Transformers) ⭐
│   ├── embeddings.py        # Paid embeddings (OpenAI)
│   ├── vector_db.py         # FAISS database wrapper with delete support
│   ├── gpt_client_free.py   # Free LLM client (Ollama/HF) ⭐
│   └── gpt_client.py        # Paid LLM client (OpenAI)
├── data/                    # Uploaded files and vector database storage
│   └── .gitkeep             # Keeps directory in git
├── requirements.txt         # Dependencies (paid version)
├── requirements_free.txt    # Dependencies (free version) ⭐ Use this!
├── start.sh                 # Startup script (paid version)
├── start_free.sh            # Startup script (free version) ⭐ Use this!
├── INSTALL_OLLAMA.md        # Guide for installing Ollama
├── README_FREE.md           # Additional free version documentation
└── README.md                # This file!

⭐ = Free version components (recommended)
```

---

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill
# Then restart the server
```

### Ollama Not Found
- Install Ollama: `brew install ollama` (macOS) or visit https://ollama.ai/
- The app will automatically use Hugging Face API as fallback

### Model Download Issues
- First-time embedding model download (~90MB) happens automatically
- For Ollama, run: `ollama pull llama3.2`
- Make sure you have internet connection for initial setup

### Slow Performance
- Close other applications to free up RAM
- Use smaller Ollama models (e.g., `phi3` instead of `llama3.2`)
- Processing large PDFs may take a minute or two

### Import Errors
- Make sure virtual environment is activated
- Run: `pip install -r requirements_free.txt`
- Restart the server after installing dependencies

---

## 🚀 Performance Tips

- **First Upload**: May take 30-60 seconds (model download + processing)
- **Subsequent Uploads**: Usually 5-15 seconds
- **Answer Generation**: 2-10 seconds depending on question complexity
- **Memory Usage**: ~2-4GB RAM (with Ollama model loaded)

---

## 🛡️ Privacy & Security

- ✅ All processing happens locally (with Ollama)
- ✅ Your documents are stored only on your machine
- ✅ No data is sent to external services (when using Ollama)
- ✅ Free Hugging Face fallback is also free and respects privacy
- ✅ No tracking or analytics

---

## 🎓 Learning Resources

### Understanding RAG
- **RAG** = Retrieval-Augmented Generation
- Retrieves relevant information from documents
- Uses that information to generate accurate answers
- Combines the best of search and AI!

### Key Concepts
- **Embeddings**: Mathematical representations of text
- **Vector Search**: Finding similar text using math
- **Chunking**: Breaking documents into smaller pieces
- **Context**: Providing relevant info to AI models

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is open source and available for educational and commercial use.

---

## 🙏 Acknowledgments

- **FastAPI** - Amazing Python web framework
- **FAISS** - Facebook AI Similarity Search
- **Sentence Transformers** - Free, local embeddings
- **Ollama** - Local LLM platform
- **Hugging Face** - Free AI models and APIs

---

## 💡 Future Enhancements

Possible improvements (feel free to contribute!):
- Support for more file formats (Word, Excel, etc.)
- Chat history persistence
- User authentication
- Multi-language support
- Better mobile responsiveness
- Advanced search filters

---

## 📞 Support

Having issues? Check the troubleshooting section above, or:
- Review the API docs at `/docs` when server is running
- Check server logs for error messages
- Make sure all dependencies are installed correctly
- Discord : malberyy
---

**Ready to get started?** Run `./start_free.sh` and open `http://localhost:8000/` in your browser! 🚀

**Happy Document Chatting!** 📚💬🤖

---

