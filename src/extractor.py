import re

def extract_fields(text):
    """Pull invoice number, date and total out of raw text."""
    invoice = {}

    m = re.search(
        r"(?:Invoice\s*(?:No|Number|#)|Inv\s*#?)\s*[:.#]*\s*([A-Z0-9][A-Z0-9-]*)",
        text, re.I)
    invoice["invoice_number"] = m.group(1) if m else None

    m = re.search(r"(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})", text)
    invoice["date"] = m.group(1) if m else None

    m = re.search(
        r"(?<!Sub)Total(?:\s*Amount)?\s*[:\-]?\s*(?:Rs\.?|LKR)?\s*([\d,]+(?:\.\d{1,2})?)",
        text, re.I)
    invoice["total"] = float(m.group(1).replace(",", "")) if m else None

    return invoice