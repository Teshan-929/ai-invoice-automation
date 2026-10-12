import pdfplumber

def read_pdf_text(path):
    """Return all text from a PDF as one string."""
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages)