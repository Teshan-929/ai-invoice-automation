from src.pdf_reader import read_pdf_text
from src.extractor import extract_fields
from src.validator import validate_invoice


def process_invoice(path):
    text = read_pdf_text(path)
    invoice = extract_fields(text)
    status, issues = validate_invoice(invoice)
    invoice["status"] = status
    invoice["issues"] = "; ".join(issues)
    return invoice