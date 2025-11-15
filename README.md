# AI Chatbot with RAG (Retrieval-Augmented Generation)

A complete AI-powered chatbot that answers questions based on uploaded PDF or text documents using Retrieval-Augmented Generation (RAG) with embeddings and a FAISS vector database.

## 🚀 Features

- **Document Upload**: Upload PDF or text files
- **Text Extraction**: Automatically extracts text from PDFs
- **Vector Database**: Uses FAISS for efficient similarity search
- **RAG Implementation**: Retrieves relevant document chunks and generates answers using GPT
- **Web Interface**: Clean, modern HTML/CSS/JS frontend
- **REST API**: FastAPI backend with proper error handling

## 📁 Project Structure

```
project-1/
├── backend/
│   └── main.py              # FastAPI application
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── styles.css           # Styling
│   └── app.js               # Frontend JavaScript
├── utils/
│   ├── __init__.py
│   ├── pdf_extractor.py     # PDF text extraction
│   ├── text_processor.py    # Text chunking utilities
│   ├── embeddings.py        # OpenAI embedding generation
│   ├── vector_db.py         # FAISS vector database wrapper
│   └── gpt_client.py        # GPT API integration
├── data/                    # Uploaded documents and vector DB
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔧 Prerequisites

1. **Python 3.8+** installed
2. **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/api-keys)

## 📦 Installation

### 1. Clone or navigate to the project directory

```bash
cd project-1
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up OpenAI API Key

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

Or set it as an environment variable:

```bash
export OPENAI_API_KEY=your-api-key-here
```

## 🚀 Running the Application

### Start the Backend Server

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or from the project root:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### Access the Frontend

Open your browser and navigate to:
- **Frontend**: `http://localhost:8000/`
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## 📚 API Endpoints

### `POST /upload`
Upload a PDF or text document for processing.

**Request**: Multipart form data with `file` field

**Response**:
```json
{
  "message": "Document 'example.pdf' uploaded and processed successfully",
  "chunks": 15,
  "total_documents": 15
}
```

### `POST /ask`
Ask a question about uploaded documents.

**Request**:
```json
{
  "question": "What is the main topic of this document?"
}
```

**Response**:
```json
{
  "answer": "Based on the document, the main topic is...",
  "sources": [
    "[Document Excerpt 1]: ...",
    "[Document Excerpt 2]: ..."
  ]
}
```

### `GET /status`
Get the status of the vector database.

**Response**:
```json
{
  "status": "running",
  "documents_in_db": 15,
  "message": "AI Chatbot RAG API is operational"
}
```

### `DELETE /clear`
Clear all documents from the vector database.

## 🎯 Usage Guide

1. **Start the backend server** (see instructions above)

2. **Open the frontend** in your browser at `http://localhost:8000/`

3. **Upload a document**:
   - Click "Choose a PDF or Text file"
   - Select a PDF or .txt file
   - Click "Upload Document"
   - Wait for processing confirmation

4. **Ask questions**:
   - Type your question in the input box
   - Click "Ask" or press Enter
   - View the answer and the document excerpts used

## 🔍 How It Works

1. **Document Upload**: When you upload a file, the system:
   - Extracts text (PDFs are parsed, text files are read)
   - Chunks the text into smaller pieces (1000 chars with 200 char overlap)
   - Generates embeddings for each chunk using OpenAI
   - Stores embeddings and text in FAISS vector database

2. **Question Answering**: When you ask a question:
   - System generates an embedding for your question
   - Searches the vector database for similar document chunks (top 3)
   - Sends the question + relevant chunks to GPT API
   - Returns the generated answer along with source excerpts

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: OpenAI text-embedding-3-small
- **LLM**: OpenAI GPT-3.5-turbo (or GPT-4)
- **PDF Processing**: PyPDF2

## ⚙️ Configuration

You can modify the following in the code:

- **Chunk size**: Change `chunk_size` and `overlap` in `text_processor.py` or `main.py`
- **Embedding model**: Change `model` parameter in `embeddings.py` (default: `text-embedding-3-small`)
- **GPT model**: Change `model` in `gpt_client.py` (default: `gpt-3.5-turbo`)
- **Number of results**: Change `k` parameter in `/ask` endpoint (default: 3)

## 🐛 Troubleshooting

### "OpenAI API key not found"
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Or create a `.env` file with your API key

### "No documents uploaded yet"
- Upload at least one document before asking questions

### Port 8000 already in use
- Change the port: `uvicorn backend.main:app --reload --port 8001`
- Update the `API_BASE_URL` in `frontend/app.js` to match

### PDF extraction errors
- Ensure the PDF is not corrupted or password-protected
- Try converting the PDF to text format if issues persist

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Ensure you're in the correct directory when running commands

## 📝 Notes

- The vector database is stored in `data/faiss_index.pkl` and persists between restarts
- Uploaded files are saved in the `data/` directory
- For production use, consider:
  - Using environment-specific API keys
  - Implementing authentication
  - Adding rate limiting
  - Using a production-grade ASGI server
  - Setting proper CORS origins

## 📄 License

This project is open source and available for educational purposes.

---

**Happy Chatting! 🚀**

