from datetime import datetime

TOLERANCE = 0.01  # allowed rounding difference


def _valid_date(value):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            datetime.strptime(value, fmt)
            return True
        except (ValueError, TypeError):
            pass
    return False


def validate_invoice(invoice):
    """Return (status, issues). status is 'verified' or 'needs_review'."""
    issues = []

    if not invoice.get("invoice_number"):
        issues.append("Missing invoice number")

    if not _valid_date(invoice.get("date")):
        issues.append("Missing or invalid date")

    total = invoice.get("total")
    if total is None:
        issues.append("Missing total")
    elif total < 0:
        issues.append("Total is negative")

    subtotal, tax = invoice.get("subtotal"), invoice.get("tax")
    if subtotal is not None and tax is not None and total is not None:
        expected = subtotal + tax
        if abs(expected - total) > TOLERANCE:
            issues.append(
                f"Subtotal + tax = {expected:,.2f} but total is {total:,.2f}")
    else:
        issues.append("Could not check subtotal + tax (missing value)")

    status = "verified" if not issues else "needs_review"
    return status, issues