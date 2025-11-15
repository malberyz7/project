"""
Utility module for managing FAISS vector database.
"""
import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple
from pathlib import Path


class VectorDB:
    """
    A simple wrapper around FAISS for storing and searching document embeddings.
    """
    
    def __init__(self, dimension: int = 1536, index_path: str = "data/faiss_index.pkl"):
        """
        Initialize the vector database.
        
        Args:
            dimension: Dimension of embeddings (1536 for text-embedding-3-small)
            index_path: Path to save/load the FAISS index
        """
        self.dimension = dimension
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity
        self.texts = []  # Store original text chunks
        self.metadata = []  # Store metadata (filename, chunk_index, etc.)
        
        # Load existing index if it exists
        self.load()
    
    def add_documents(self, embeddings: List[List[float]], texts: List[str], 
                     metadata: List[dict] = None):
        """
        Add document embeddings to the vector database.
        
        Args:
            embeddings: List of embedding vectors
            texts: List of corresponding text chunks
            metadata: Optional list of metadata dictionaries
        """
        if not embeddings or not texts:
            return
        
        if len(embeddings) != len(texts):
            raise ValueError("Number of embeddings must match number of texts")
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store texts and metadata
        self.texts.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            # Create default metadata
            self.metadata.extend([{}] * len(texts))
        
        # Save after adding
        self.save()
    
    def search(self, query_embedding: List[float], k: int = 3) -> List[Tuple[str, float, dict]]:
        """
        Search for similar documents in the vector database.
        
        Args:
            query_embedding: The query embedding vector
            k: Number of results to return
            
        Returns:
            List of tuples: (text, distance, metadata)
        """
        if self.index.ntotal == 0:
            return []
        
        # Convert query to numpy array
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search in FAISS
        distances, indices = self.index.search(query_array, min(k, self.index.ntotal))
        
        # Return results with text and metadata
        results = []
        for i, idx in enumerate(indices[0]):
            if idx >= 0:  # Valid index
                distance = float(distances[0][i])
                text = self.texts[idx]
                metadata = self.metadata[idx] if idx < len(self.metadata) else {}
                results.append((text, distance, metadata))
        
        return results
    
    def save(self):
        """Save the FAISS index and associated data to disk."""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        # Save index
        faiss.write_index(self.index, self.index_path.replace('.pkl', '.index'))
        
        # Save texts and metadata
        data = {
            'texts': self.texts,
            'metadata': self.metadata,
            'dimension': self.dimension
        }
        with open(self.index_path, 'wb') as f:
            pickle.dump(data, f)
    
    def load(self):
        """Load the FAISS index and associated data from disk."""
        index_file = self.index_path.replace('.pkl', '.index')
        
        if os.path.exists(index_file) and os.path.exists(self.index_path):
            try:
                # Load index
                self.index = faiss.read_index(index_file)
                
                # Load texts and metadata
                with open(self.index_path, 'rb') as f:
                    data = pickle.load(f)
                    self.texts = data.get('texts', [])
                    self.metadata = data.get('metadata', [])
                    self.dimension = data.get('dimension', self.dimension)
            except Exception as e:
                print(f"Warning: Could not load existing index: {e}")
                # Reset to empty index
                self.index = faiss.IndexFlatL2(self.dimension)
                self.texts = []
                self.metadata = []
    
    def clear(self):
        """Clear all documents from the database."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []
        # Remove saved files
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        index_file = self.index_path.replace('.pkl', '.index')
        if os.path.exists(index_file):
            os.remove(index_file)
    
    def size(self) -> int:
        """Get the number of documents in the database."""
        return self.index.ntotal

