"""
Free utility module for generating text embeddings using Sentence Transformers (local, no API costs).
"""
from typing import List
import os


# Global model instance to avoid reloading
_model = None
_model_name = "all-MiniLM-L6-v2"  # Free, lightweight, 384-dimensional embeddings


def _get_model():
    """Lazy load the sentence transformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading embedding model: {_model_name} (first time only, this may take a minute)...")
            _model = SentenceTransformer(_model_name)
            print("Model loaded successfully!")
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. Install with: pip install sentence-transformers torch"
            )
    return _model


def get_embedding_dimension() -> int:
    """Get the dimension of embeddings produced by the current model."""
    return 384  # all-MiniLM-L6-v2 produces 384-dimensional embeddings


def generate_embedding(text: str, model: str = None) -> List[float]:
    """
    Generate embedding for a single text string using Sentence Transformers (FREE, local).
    
    Args:
        text: Text to embed
        model: Ignored (kept for compatibility), uses local Sentence Transformer model
        
    Returns:
        List of float values representing the embedding (384 dimensions)
    """
    try:
        model = _get_model()
        embedding = model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    except Exception as e:
        raise ValueError(f"Error generating embedding: {str(e)}")


def generate_embeddings_batch(texts: List[str], model: str = None) -> List[List[float]]:
    """
    Generate embeddings for multiple texts efficiently using Sentence Transformers (FREE, local).
    
    Args:
        texts: List of texts to embed
        model: Ignored (kept for compatibility), uses local Sentence Transformer model
        
    Returns:
        List of embeddings (each is a list of 384 floats)
    """
    try:
        model = _get_model()
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return embeddings.tolist()
    except Exception as e:
        raise ValueError(f"Error generating embeddings: {str(e)}")

