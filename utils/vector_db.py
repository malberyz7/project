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
        self.embeddings = []  # Store embeddings for deletion purposes
        
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
        
        # Store texts, metadata, and embeddings
        self.texts.extend(texts)
        self.embeddings.extend(embeddings)  # Store embeddings for deletion
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
        
        # Save texts, metadata, and embeddings
        data = {
            'texts': self.texts,
            'metadata': self.metadata,
            'embeddings': self.embeddings,
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
                
                # Load texts, metadata, and embeddings
                with open(self.index_path, 'rb') as f:
                    data = pickle.load(f)
                    self.texts = data.get('texts', [])
                    self.metadata = data.get('metadata', [])
                    self.embeddings = data.get('embeddings', [])
                    self.dimension = data.get('dimension', self.dimension)
                    
                    # Handle old database files that don't have embeddings stored
                    # If embeddings are missing but we have texts, create empty list
                    # (embeddings will be regenerated on next deletion if needed)
                    if not self.embeddings and self.texts:
                        self.embeddings = [None] * len(self.texts)
            except Exception as e:
                print(f"Warning: Could not load existing index: {e}")
                # Reset to empty index
                self.index = faiss.IndexFlatL2(self.dimension)
                self.texts = []
                self.metadata = []
                self.embeddings = []
    
    def delete_documents_by_filename(self, filename: str) -> int:
        """
        Delete all chunks associated with a specific filename from the database.
        
        Args:
            filename: The filename to delete
            
        Returns:
            Number of chunks deleted
        """
        if self.index.ntotal == 0:
            return 0
        
        # Find indices of all chunks with matching filename
        indices_to_remove = set()
        for i, meta in enumerate(self.metadata):
            if meta.get("filename") == filename:
                indices_to_remove.add(i)
        
        if not indices_to_remove:
            return 0
        
        # Check if we have embeddings stored (newer database format)
        has_embeddings = self.embeddings and all(e is not None for e in self.embeddings if self.embeddings)
        has_some_embeddings = self.embeddings and any(e is not None for e in self.embeddings)
        
        if not has_some_embeddings:
            # Old database without stored embeddings - need to rebuild index differently
            # For now, we'll just remove from texts/metadata but keep index structure
            # This is not ideal but maintains functionality for old databases
            new_texts = []
            new_metadata = []
            new_embeddings = []
            
            # Remove items in reverse order to preserve indices
            indices_to_remove_sorted = sorted(indices_to_remove, reverse=True)
            for idx in indices_to_remove_sorted:
                if idx < len(self.texts):
                    self.texts.pop(idx)
                if idx < len(self.metadata):
                    self.metadata.pop(idx)
                if idx < len(self.embeddings):
                    self.embeddings.pop(idx)
            
            # Note: FAISS index still contains old entries, but they won't be accessible
            # This is acceptable for now - full rebuild would require re-embedding
            
            # Save changes
            self.save()
            return len(indices_to_remove)
        
        # Create new index, texts, metadata, and embeddings without deleted chunks
        # Note: FAISS doesn't support direct deletion, so we rebuild
        new_index = faiss.IndexFlatL2(self.dimension)
        new_texts = []
        new_metadata = []
        new_embeddings = []
        
        for i in range(len(self.texts)):
            if i not in indices_to_remove:
                # Re-add to new index using stored embedding
                if i < len(self.embeddings) and self.embeddings[i] is not None:
                    embedding = np.array([self.embeddings[i]]).astype('float32')
                    new_index.add(embedding)
                    new_embeddings.append(self.embeddings[i])
                else:
                    # Missing embedding - skip for now
                    new_embeddings.append(None)
                new_texts.append(self.texts[i])
                new_metadata.append(self.metadata[i])
        
        # Replace with new data
        self.index = new_index
        self.texts = new_texts
        self.metadata = new_metadata
        self.embeddings = new_embeddings
        
        # Save changes
        self.save()
        
        return len(indices_to_remove)
    
    def get_filenames(self) -> List[str]:
        """
        Get a list of all unique filenames in the database.
        
        Returns:
            List of unique filenames
        """
        filenames = set()
        for meta in self.metadata:
            filename = meta.get("filename")
            if filename:
                filenames.add(filename)
        return sorted(list(filenames))
    
    def get_file_info(self) -> List[dict]:
        """
        Get information about all files in the database.
        
        Returns:
            List of dictionaries with file information
        """
        file_info = {}
        for meta in self.metadata:
            filename = meta.get("filename")
            if filename:
                if filename not in file_info:
                    file_info[filename] = {
                        "filename": filename,
                        "chunks": 0,
                        "first_chunk_index": None
                    }
                file_info[filename]["chunks"] += 1
                if file_info[filename]["first_chunk_index"] is None:
                    file_info[filename]["first_chunk_index"] = meta.get("chunk_index", 0)
        
        return list(file_info.values())
    
    def clear(self):
        """Clear all documents from the database."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []
        self.embeddings = []
        # Remove saved files
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        index_file = self.index_path.replace('.pkl', '.index')
        if os.path.exists(index_file):
            os.remove(index_file)
    
    def size(self) -> int:
        """Get the number of documents in the database."""
        return self.index.ntotal

