"""
Utility module for processing and chunking text documents.
"""
from typing import List


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks for better context retention.
    
    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk (in characters)
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if not text or len(text.strip()) == 0:
        return []
    
    chunks = []
    text = text.strip()
    
    # Start with the first chunk
    start = 0
    while start < len(text):
        # Calculate end position
        end = start + chunk_size
        
        # Try to break at sentence boundaries for better chunking
        if end < len(text):
            # Look for sentence endings near the chunk boundary
            sentence_endings = ['.', '!', '?', '\n']
            for i in range(end, max(start, end - 200), -1):
                if text[i] in sentence_endings:
                    end = i + 1
                    break
        
        # Extract chunk
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position (with overlap)
        start = end - overlap
        
        # Prevent infinite loop
        if start >= end:
            start = end
    
    return chunks if chunks else [text]

