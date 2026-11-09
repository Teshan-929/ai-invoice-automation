from src.pdf_reader import read_document_text
from src.extractor import extract_fields
from src.validator import validate_invoice

SUPPORTED = (".pdf", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp")


def process_invoice(path):
    text = read_document_text(path)
    invoice = extract_fields(text)
    status, issues = validate_invoice(invoice)
    invoice["status"] = status
    invoice["issues"] = "; ".join(issues)
    return invoice