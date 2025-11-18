"""
Free utility module for generating answers using Ollama or Hugging Face Inference API (no OpenAI costs).
"""
import os
from typing import List, Optional
import requests


def generate_answer(question: str, context_chunks: List[str], 
                   model: str = "llama3.2",  # Default Ollama model
                   use_ollama: bool = True) -> str:
    """
    Generate an answer to a question using a FREE LLM (Ollama local or Hugging Face API).
    
    Args:
        question: The user's question
        context_chunks: List of relevant document chunks retrieved from vector DB
        model: Model name (default: "llama3.2" for Ollama, or HuggingFace model)
        use_ollama: If True, use Ollama (local). If False, use Hugging Face Inference API
        
    Returns:
        Generated answer as a string
    """
    # Combine context chunks
    context = "\n\n".join([f"[Document Excerpt {i+1}]:\n{chunk}" 
                           for i, chunk in enumerate(context_chunks)])
    
    # Create the prompt
    prompt = f"""You are a helpful AI assistant that answers questions based on the provided document context.
Use only the information from the context to answer questions. If the context doesn't contain 
enough information to answer the question, say so clearly. Be concise and accurate.

Context from documents:
{context}

Question: {question}

Please provide an answer based on the context above."""
    
    # Try Ollama first if requested, or if Hugging Face will likely fail
    if use_ollama:
        try:
            return _generate_with_ollama(prompt, model)
        except Exception as e:
            print(f"Ollama error: {e}")
            print("Falling back to Hugging Face...")
            # Try Hugging Face with a free model
            try:
                return _generate_with_huggingface(prompt, model="HuggingFaceH4/zephyr-7b-beta")
            except:
                raise ValueError(
                    "Neither Ollama nor Hugging Face API is available. "
                    "Please install Ollama (https://ollama.ai/) and run 'ollama pull llama3.2' "
                    "for free local LLM access."
                )
    else:
        # Try Hugging Face with a free public model
        try:
            return _generate_with_huggingface(prompt, model="HuggingFaceH4/zephyr-7b-beta")
        except Exception as e:
            # If Hugging Face fails, try Ollama as fallback
            print("Hugging Face failed, trying Ollama...")
            try:
                return _generate_with_ollama(prompt, model="llama3.2")
            except:
                raise ValueError(
                    f"Hugging Face API error: {str(e)}. "
                    "Please install Ollama (https://ollama.ai/) and run 'ollama pull llama3.2' "
                    "for free local LLM access."
                )


def _generate_with_ollama(prompt: str, model: str = "llama3.2") -> str:
    """
    Generate answer using Ollama (local, free).
    
    Requires: Ollama installed and running locally
    Install: https://ollama.ai/
    Run: ollama pull llama3.2
    """
    try:
        import ollama
        
        response = ollama.generate(
            model=model,
            prompt=prompt,
            options={
                "temperature": 0.7,
                "num_predict": 500
            }
        )
        
        # Handle different response formats
        if isinstance(response, dict):
            if "response" in response:
                return response["response"].strip()
            elif "text" in response:
                return response["text"].strip()
        
        return str(response).strip()
    
    except ImportError:
        raise Exception(
            "Ollama Python library not installed. Install with: pip install ollama\n"
            "Also make sure Ollama is installed and running: https://ollama.ai/\n"
            "Run 'ollama pull llama3.2' to download a model."
        )
    except Exception as e:
        # Try fallback to Hugging Face if Ollama fails
        raise Exception(f"Ollama error: {e}")


def _generate_with_huggingface(prompt: str, model: str = "mistralai/Mistral-7B-Instruct-v0.2") -> str:
    """
    Generate answer using Hugging Face Inference API (free tier, no key required for some models).
    Uses the new router API endpoint.
    """
    try:
        # Use the new router endpoint
        api_url = f"https://router.huggingface.co/models/{model}"
        
        response = requests.post(
            api_url,
            headers={"Content-Type": "application/json"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            # Handle different response formats from router API
            if isinstance(result, list) and len(result) > 0:
                result = result[0]
            
            if isinstance(result, dict):
                if "generated_text" in result:
                    return result["generated_text"].strip()
                elif "text" in result:
                    return result["text"].strip()
                elif "response" in result:
                    return result["response"].strip()
                # Try to extract text from any nested structure
                for key in ["text", "output", "content", "message"]:
                    if key in result:
                        return str(result[key]).strip()
            
            # If we get a string directly, return it
            if isinstance(result, str):
                return result.strip()
            
            # Last resort: return string representation
            return str(result).strip()
        elif response.status_code == 503:
            # Model is loading, wait a bit
            import time
            time.sleep(5)
            return "The model is loading, please try again in a few seconds. Please wait and try again."
        elif response.status_code == 401:
            # Unauthorized - API key or auth required
            raise ValueError(
                "Hugging Face API authentication failed (401). "
                "Some models require authentication. Please install Ollama for local use, "
                "or check if this model requires an API key."
            )
        elif response.status_code == 429:
            return "Rate limit exceeded. Please try again in a few moments."
        else:
            # Try to parse error message, avoid showing raw HTML
            error_msg = f"Error {response.status_code}"
            try:
                error_json = response.json()
                if "error" in error_json:
                    error_msg = error_json["error"]
            except:
                # If response is HTML, don't show it - provide a clean error
                if "text/html" in response.headers.get("content-type", "").lower():
                    error_msg = f"API returned HTML error page (status {response.status_code}). "
                    if response.status_code == 401:
                        error_msg += "Authentication required. Try installing Ollama for local use."
                    else:
                        error_msg += "The model may be unavailable or require authentication."
                else:
                    # Try to extract readable text from response
                    text = response.text[:200]  # Limit length
                    if not text.startswith("<"):  # Not HTML
                        error_msg = text
            raise ValueError(f"Hugging Face API error: {error_msg}")
    
    except Exception as e:
        raise ValueError(f"Error generating answer with Hugging Face: {str(e)}")


def generate_answer_simple(question: str, context_chunks: List[str]) -> str:
    """
    Simple answer generation that tries Ollama first, then Hugging Face.
    """
    try:
        return _generate_with_ollama(
            _create_prompt(question, context_chunks),
            model="llama3.2"
        )
    except:
        try:
            return _generate_with_huggingface(
                _create_prompt(question, context_chunks)
            )
        except Exception as e:
            raise ValueError(f"Error generating answer: {str(e)}")


def _create_prompt(question: str, context_chunks: List[str]) -> str:
    """Helper to create prompt."""
    context = "\n\n".join([f"[Document Excerpt {i+1}]:\n{chunk}" 
                           for i, chunk in enumerate(context_chunks)])
    return f"""You are a helpful AI assistant that answers questions based on the provided document context.
Use only the information from the context to answer questions. If the context doesn't contain 
enough information to answer the question, say so clearly. Be concise and accurate.

Context from documents:
{context}

Question: {question}

Please provide an answer based on the context above."""

