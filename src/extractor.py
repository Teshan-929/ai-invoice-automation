import re

AMOUNT = r"(?:Rs\.?|LKR)?\s*([\d,]+(?:\.\d{1,2})?)"


def _to_float(value):
    return float(value.replace(",", "")) if value else None


def _find_amount(label_pattern, text):
    m = re.search(label_pattern + r"\s*[:\-]?\s*" + AMOUNT, text, re.I)
    return _to_float(m.group(1)) if m else None


def extract_fields(text):
    """Pull invoice number, date, subtotal, tax and total out of raw text."""
    invoice = {}

    m = re.search(
        r"\bInv(?:oice)?\s*(?:No\.?|Number|#)\s*[:.#]*\s*([A-Z0-9][A-Z0-9-]*)",
        text, re.I)
    invoice["invoice_number"] = m.group(1) if m else None

    m = re.search(r"(\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2})", text)
    invoice["date"] = m.group(1) if m else None

    invoice["subtotal"] = _find_amount(r"Sub\s*-?\s*total", text)
    invoice["tax"] = _find_amount(r"(?:Tax|VAT)", text)
    invoice["total"] = _find_amount(r"(?<!Sub)(?<!Sub )Total(?:\s*Amount)?", text)

    return invoice