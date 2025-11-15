"""
Utility module for interacting with OpenAI GPT API for generating answers.
"""
from openai import OpenAI
import os
from typing import List, Optional


def generate_answer(question: str, context_chunks: List[str], 
                   api_key: Optional[str] = None,
                   model: str = "gpt-3.5-turbo") -> str:
    """
    Generate an answer to a question using GPT API with RAG context.
    
    Args:
        question: The user's question
        context_chunks: List of relevant document chunks retrieved from vector DB
        api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
        model: GPT model to use
        
    Returns:
        Generated answer as a string
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )
    
    client = OpenAI(api_key=api_key)
    
    # Combine context chunks
    context = "\n\n".join([f"[Document Excerpt {i+1}]:\n{chunk}" 
                           for i, chunk in enumerate(context_chunks)])
    
    # Create the prompt
    system_prompt = """You are a helpful AI assistant that answers questions based on the provided document context.
    Use only the information from the context to answer questions. If the context doesn't contain 
    enough information to answer the question, say so clearly. Be concise and accurate."""
    
    user_prompt = f"""Context from documents:
{context}

Question: {question}

Please provide an answer based on the context above."""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise ValueError(f"Error generating answer with GPT: {str(e)}")

