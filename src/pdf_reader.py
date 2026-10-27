import pdfplumber

MIN_TEXT_LENGTH = 20  # fewer characters than this = probably a scanned PDF


def read_pdf_text(path):
    """Return all text from a PDF as one string."""
    with pdfplumber.open(path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n".join(pages)


def read_document_text(path):
    """Read a PDF or image. Use OCR when there is no text to read."""
    from src.ocr_processor import ocr_image, ocr_pdf

    suffix = str(path).lower().rsplit(".", 1)[-1]
    if suffix in ("png", "jpg", "jpeg", "tif", "tiff", "bmp"):
        return ocr_image(path)

    text = read_pdf_text(path)
    if len(text.strip()) < MIN_TEXT_LENGTH:
        text = ocr_pdf(path)
    return text