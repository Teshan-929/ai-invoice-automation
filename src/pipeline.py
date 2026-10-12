from src.pdf_reader import read_pdf_text
from src.extractor import extract_fields

def process_invoice(path):
    text = read_pdf_text(path)
    return extract_fields(text)