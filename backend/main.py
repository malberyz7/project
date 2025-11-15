"""
FastAPI backend for AI Chatbot with RAG capabilities.
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

# Add parent directory to path for imports
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

from utils.pdf_extractor import extract_text_from_pdf
from utils.text_processor import chunk_text
from utils.embeddings import generate_embeddings_batch, generate_embedding
from utils.vector_db import VectorDB
from utils.gpt_client import generate_answer

# Initialize FastAPI app
app = FastAPI(title="AI Chatbot RAG API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize vector database (use absolute path)
vector_db = VectorDB(dimension=1536, index_path=str(BASE_DIR / "data" / "faiss_index.pkl"))

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
    app.mount("/static", StaticFiles(directory="frontend"), name="static")
    
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
    return {"message": "AI Chatbot RAG API is running. Frontend not found."}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a PDF or text document.
    
    - Extracts text from the file
    - Chunks the text
    - Generates embeddings
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
        
        # Generate embeddings for all chunks
        print(f"Generating embeddings for {len(chunks)} chunks...")
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
            "message": f"Document '{file.filename}' uploaded and processed successfully",
            "chunks": len(chunks),
            "total_documents": vector_db.size()
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
    Ask a question and get an answer based on uploaded documents.
    
    - Generates embedding for the question
    - Searches vector database for relevant chunks
    - Uses GPT API to generate answer from context
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
        
        # Generate embedding for the question
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
        
        # Generate answer using GPT
        answer = generate_answer(question, context_chunks)
        
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
        "documents_in_db": vector_db.size(),
        "message": "AI Chatbot RAG API is operational"
    }


@app.delete("/clear")
def clear_database():
    """Clear all documents from the vector database."""
    vector_db.clear()
    return {"message": "Vector database cleared successfully"}

