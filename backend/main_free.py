"""
FastAPI backend for AI Chatbot with RAG capabilities - FREE VERSION (no OpenAI costs).
Uses Sentence Transformers for embeddings and Ollama/HuggingFace for LLM.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file (optional for free version)
BASE_DIR = Path(__file__).parent.parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

# Add parent directory to path for imports
sys.path.append(str(BASE_DIR))

from utils.pdf_extractor import extract_text_from_pdf
from utils.text_processor import chunk_text
from utils.embeddings_free import generate_embeddings_batch, generate_embedding, get_embedding_dimension
from utils.vector_db import VectorDB
from utils.gpt_client_free import generate_answer

# Initialize FastAPI app
app = FastAPI(title="AI Chatbot RAG API - FREE VERSION")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector database with FREE embedding dimension (384 instead of 1536)
EMBEDDING_DIM = get_embedding_dimension()  # 384 for all-MiniLM-L6-v2
vector_db = VectorDB(dimension=EMBEDDING_DIM, index_path=str(BASE_DIR / "data" / "faiss_index_free.pkl"))

# Ensure data directory exists
os.makedirs(BASE_DIR / "data", exist_ok=True)


class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str


class QuestionResponse(BaseModel):
    """Response model for answers."""
    answer: str
    sources: List[str]  # Document excerpts used for the answer


# Serve frontend static files (CSS, JS, etc.)
frontend_path = BASE_DIR / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")
    
    # Serve CSS and JS files
    @app.get("/styles.css")
    async def get_styles():
        css_path = BASE_DIR / "frontend" / "styles.css"
        if css_path.exists():
            return FileResponse(css_path, media_type="text/css")
        raise HTTPException(status_code=404, detail="CSS file not found")
    
    @app.get("/app.js")
    async def get_app_js():
        js_path = BASE_DIR / "frontend" / "app.js"
        if js_path.exists():
            return FileResponse(js_path, media_type="application/javascript")
        raise HTTPException(status_code=404, detail="JS file not found")

@app.get("/")
def root():
    """Root endpoint - serve frontend."""
    index_path = BASE_DIR / "frontend" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "AI Chatbot RAG API (FREE VERSION) is running. Frontend not found."}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF or text document (FREE VERSION - uses Sentence Transformers).
    
    - Extracts text from the file
    - Chunks the text
    - Generates embeddings locally (no API costs)
    - Stores in vector database
    """
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.txt', '.text'}
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported types: {allowed_extensions}"
            )
        
        # Read file content
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Extract text based on file type
        if file_ext == '.pdf':
            text = extract_text_from_pdf(content)
        else:  # .txt or .text
            text = content.decode('utf-8')
            if not text.strip():
                raise HTTPException(status_code=400, detail="Text file is empty")
        
        # Process text: chunk it
        chunks = chunk_text(text, chunk_size=1000, overlap=200)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No text could be extracted from the file")
        
        # Generate embeddings for all chunks (FREE, local, no API costs)
        print(f"Generating embeddings for {len(chunks)} chunks using FREE local model...")
        embeddings = generate_embeddings_batch(chunks)
        
        # Prepare metadata for each chunk
        metadata_list = [
            {
                "filename": file.filename,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]
        
        # Add to vector database
        vector_db.add_documents(embeddings, chunks, metadata_list)
        
        # Save the uploaded file (optional, for reference)
        file_path = BASE_DIR / "data" / file.filename
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "message": f"Document '{file.filename}' uploaded and processed successfully (FREE version - no API costs)",
            "chunks": len(chunks),
            "total_documents": vector_db.size(),
            "embedding_model": "all-MiniLM-L6-v2 (local, free)"
        }
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question and get an answer based on uploaded documents (FREE VERSION).
    
    - Generates embedding for the question (local, free)
    - Searches vector database for relevant chunks
    - Uses FREE LLM (Ollama local or Hugging Face) to generate answer from context
    """
    try:
        question = request.question.strip()
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Check if vector database has documents
        if vector_db.size() == 0:
            raise HTTPException(
                status_code=400,
                detail="No documents uploaded yet. Please upload a document first."
            )
        
        # Generate embedding for the question (FREE, local)
        question_embedding = generate_embedding(question)
        
        # Search for relevant document chunks
        search_results = vector_db.search(question_embedding, k=3)
        
        if not search_results:
            raise HTTPException(
                status_code=404,
                detail="No relevant documents found for this question"
            )
        
        # Extract text chunks from search results
        context_chunks = [result[0] for result in search_results]
        
        # Generate answer using FREE LLM (Ollama local or Hugging Face)
        # Try Ollama first, fallback to Hugging Face automatically
        try:
            answer = generate_answer(question, context_chunks, use_ollama=True)
        except Exception as e:
            # If both Ollama and Hugging Face fail, provide helpful error
            error_msg = str(e)
            if "401" in error_msg or "authentication" in error_msg.lower():
                raise HTTPException(
                    status_code=503,
                    detail=(
                        "LLM service unavailable. Please install Ollama for free local use:\n"
                        "1. Install from https://ollama.ai/\n"
                        "2. Run: ollama pull llama3.2\n"
                        "3. Restart the server"
                    )
                )
            raise
        
        return QuestionResponse(
            answer=answer,
            sources=context_chunks
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


@app.get("/status")
def get_status():
    """Get status of the vector database."""
    return {
        "status": "running",
        "version": "FREE (no OpenAI costs)",
        "documents_in_db": vector_db.size(),
        "embedding_model": "all-MiniLM-L6-v2 (local, Sentence Transformers)",
        "llm": "Ollama (local) or Hugging Face (free API)",
        "embedding_dimension": EMBEDDING_DIM,
        "message": "AI Chatbot RAG API - FREE VERSION is operational (no API costs)"
    }


@app.get("/files")
def list_files():
    """
    Get a list of all uploaded files with their information.
    
    Returns:
        List of files with metadata (filename, chunks count)
    """
    try:
        file_info = vector_db.get_file_info()
        return {
            "files": file_info,
            "total_files": len(file_info),
            "total_chunks": vector_db.size()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")


@app.delete("/files/{filename:path}")
def delete_file(filename: str):
    """
    Delete a specific file from the vector database and filesystem.
    
    Args:
        filename: The filename to delete
        
    Returns:
        Confirmation message with deletion details
    """
    try:
        # Check if file exists in database
        file_info = vector_db.get_file_info()
        file_exists = any(f["filename"] == filename for f in file_info)
        
        if not file_exists:
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found in database")
        
        # Delete from vector database
        chunks_deleted = vector_db.delete_documents_by_filename(filename)
        
        # Delete physical file from filesystem
        file_path = BASE_DIR / "data" / filename
        file_deleted = False
        if file_path.exists():
            try:
                os.remove(file_path)
                file_deleted = True
            except Exception as e:
                print(f"Warning: Could not delete file {filename}: {e}")
        
        return {
            "message": f"File '{filename}' deleted successfully",
            "filename": filename,
            "chunks_deleted": chunks_deleted,
            "file_deleted_from_disk": file_deleted,
            "remaining_chunks": vector_db.size()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


@app.delete("/clear")
def clear_database():
    """Clear all documents from the vector database."""
    try:
        # Get list of files before clearing
        file_info = vector_db.get_file_info()
        filenames = [f["filename"] for f in file_info]
        
        # Clear vector database
        vector_db.clear()
        
        # Delete all files from filesystem
        deleted_files = []
        for filename in filenames:
            file_path = BASE_DIR / "data" / filename
            if file_path.exists():
                try:
                    os.remove(file_path)
                    deleted_files.append(filename)
                except Exception as e:
                    print(f"Warning: Could not delete file {filename}: {e}")
        
        return {
            "message": "Vector database cleared successfully",
            "files_deleted": len(deleted_files),
            "chunks_cleared": 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing database: {str(e)}")

