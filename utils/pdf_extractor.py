"""
Utility module for extracting text from PDF files.
"""
import PyPDF2
from io import BytesIO
from typing import Optional


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file_content: Binary content of the PDF file
        
    Returns:
        Extracted text as a string
        
    Raises:
        ValueError: If the PDF cannot be read or is empty
    """
    try:
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        if len(pdf_reader.pages) == 0:
            raise ValueError("PDF file is empty - no pages found")
        
        text = ""
        for page_num, page in enumerate(pdf_reader.pages, 1):
            page_text = page.extract_text()
            if page_text.strip():
                text += f"\n--- Page {page_num} ---\n"
                text += page_text
        
        if not text.strip():
            raise ValueError("PDF file contains no extractable text")
            
        return text.strip()
    
    except Exception as e:
        raise ValueError(f"Error reading PDF: {str(e)}")

