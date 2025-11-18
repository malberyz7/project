"""
Utility module for generating text embeddings using OpenAI API.
"""
import openai
from typing import List, Optional
import os


def initialize_openai(api_key: Optional[str] = None):
    """
    Initialize OpenAI client with API key.
    
    Args:
        api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
            "or pass api_key parameter."
        )
    
    openai.api_key = api_key


def generate_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """
    Generate embedding for a single text string.
    
    Args:
        text: Text to embed
        model: OpenAI embedding model to use
        
    Returns:
        List of float values representing the embedding
    """
    try:
        from openai import OpenAI
        from openai import APIError
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize client without proxies parameter
        client = OpenAI(api_key=api_key)
        
        response = client.embeddings.create(
            model=model,
            input=text
        )
        return response.data[0].embedding
    except APIError as e:
        if e.status_code == 429:
            if "insufficient_quota" in str(e) or "quota" in str(e).lower():
                raise ValueError(
                    "OpenAI API quota exceeded. Please check your OpenAI account billing and quota. "
                    "Visit https://platform.openai.com/account/billing to add credits or upgrade your plan."
                )
            else:
                raise ValueError(
                    f"OpenAI API rate limit exceeded. Please try again in a few moments. "
                    f"Error: {str(e)}"
                )
        else:
            raise ValueError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error generating embedding: {str(e)}")


def generate_embeddings_batch(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently.
    
    Args:
        texts: List of texts to embed
        model: OpenAI embedding model to use
        
    Returns:
        List of embeddings (each is a list of floats)
    """
    try:
        from openai import OpenAI
        from openai import APIError
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize client without proxies parameter
        client = OpenAI(api_key=api_key)
        
        # OpenAI API supports batch processing
        response = client.embeddings.create(
            model=model,
            input=texts
        )
        return [item.embedding for item in response.data]
    except APIError as e:
        if e.status_code == 429:
            if "insufficient_quota" in str(e) or "quota" in str(e).lower():
                raise ValueError(
                    "OpenAI API quota exceeded. Please check your OpenAI account billing and quota. "
                    "Visit https://platform.openai.com/account/billing to add credits or upgrade your plan."
                )
            else:
                raise ValueError(
                    f"OpenAI API rate limit exceeded. Please try again in a few moments. "
                    f"Error: {str(e)}"
                )
        else:
            raise ValueError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error generating embeddings: {str(e)}")

