import pdfplumber
import pytesseract
from PIL import Image

# Windows only: uncomment this line if Tesseract is not found automatically
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_image(path):
    """Read text from an image file (png, jpg...)."""
    with Image.open(path) as img:
        return pytesseract.image_to_string(img.convert("L"))


def ocr_pdf(path):
    """Read text from a scanned PDF by turning each page into an image."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            image = page.to_image(resolution=300).original.convert("L")
            pages.append(pytesseract.image_to_string(image))
    return "\n".join(pages)