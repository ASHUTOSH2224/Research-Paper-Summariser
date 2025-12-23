"""
PDF Handler Module
Handles downloading PDFs from arXiv and extracting text content.
"""
import requests
import fitz  # PyMuPDF
import io
import re


def get_pdf_url(paper_link: str) -> str:
    """
    Convert arXiv abstract URL to PDF URL.
    
    Example:
        https://arxiv.org/abs/2312.12345 -> https://arxiv.org/pdf/2312.12345.pdf
    """
    # Handle both http and https, with or without www
    pdf_url = paper_link.replace('/abs/', '/pdf/')
    if not pdf_url.endswith('.pdf'):
        pdf_url += '.pdf'
    return pdf_url


def download_pdf(pdf_url: str, timeout: int = 30) -> bytes:
    """
    Download PDF from the given URL.
    
    Args:
        pdf_url: URL to the PDF file
        timeout: Request timeout in seconds
        
    Returns:
        PDF content as bytes
        
    Raises:
        Exception: If download fails
    """
    headers = {
        'User-Agent': 'ResearchSummarizerBot/1.0 (mailto:research@example.com)'
    }
    
    response = requests.get(pdf_url, headers=headers, timeout=timeout)
    response.raise_for_status()
    
    return response.content


def extract_text_from_pdf(pdf_bytes: bytes, max_pages: int = 20) -> str:
    """
    Extract text content from PDF bytes using PyMuPDF.
    
    Args:
        pdf_bytes: PDF file content as bytes
        max_pages: Maximum number of pages to extract (to limit token usage)
        
    Returns:
        Extracted text content
    """
    text_parts = []
    
    # Open PDF from bytes
    pdf_stream = io.BytesIO(pdf_bytes)
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    
    # Extract text from each page (up to max_pages)
    pages_to_extract = min(len(doc), max_pages)
    for page_num in range(pages_to_extract):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():
            text_parts.append(text)
    
    doc.close()
    
    full_text = '\n\n'.join(text_parts)
    
    # Clean up the text
    full_text = clean_extracted_text(full_text)
    
    return full_text


def clean_extracted_text(text: str) -> str:
    """
    Clean up extracted PDF text.
    """
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove common PDF artifacts
    text = re.sub(r'\x00', '', text)  # Null bytes
    
    return text.strip()


def get_paper_content(paper: dict, max_chars: int = 50000) -> str:
    """
    Main entry point: Get full paper content from a paper dict.
    
    Args:
        paper: Paper dictionary with 'link' key
        max_chars: Maximum characters to return (for token limits)
        
    Returns:
        Extracted paper text, or abstract if PDF extraction fails
    """
    try:
        pdf_url = get_pdf_url(paper['link'])
        print(f"  Downloading PDF from: {pdf_url}")
        
        pdf_bytes = download_pdf(pdf_url)
        print(f"  PDF downloaded: {len(pdf_bytes)} bytes")
        
        text = extract_text_from_pdf(pdf_bytes)
        print(f"  Extracted {len(text)} characters of text")
        
        # Truncate if too long (to stay within token limits)
        if len(text) > max_chars:
            text = text[:max_chars] + "\n\n[Content truncated due to length...]"
            print(f"  Truncated to {max_chars} characters")
        
        return text
        
    except Exception as e:
        print(f"  Warning: Failed to get PDF content: {e}")
        print(f"  Falling back to abstract only")
        # Fallback to abstract if PDF extraction fails
        return f"Title: {paper.get('title', 'Unknown')}\n\nAbstract: {paper.get('abstract', 'No abstract available')}"


if __name__ == "__main__":
    # Test with a sample paper
    test_paper = {
        'title': 'Attention Is All You Need',
        'abstract': 'The dominant sequence transduction models...',
        'link': 'https://arxiv.org/abs/1706.03762'
    }
    
    content = get_paper_content(test_paper)
    print(f"\n--- Extracted Content Preview (first 1000 chars) ---\n")
    print(content[:1000])
