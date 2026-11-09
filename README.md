# AI Invoice Processing & Business Automation System

Reads invoices (PDF, scans and photos), extracts the key fields, checks that the numbers add up, and stores everything in a database. Only invoices that look wrong need a human to look at them.

![Screenshot](docs/screenshot.png)

## Features

- **Reads PDFs, scans and photos**: uses PDF text when available, and falls back to OCR (Tesseract) for scanned PDFs, PNG and JPG files
- **Extracts** invoice number, date, subtotal, tax and total, across different layouts (`Invoice No`, `Inv #`, `Total Amount`, several date formats)
- **Validates** each invoice: subtotal + tax = total, valid date, missing fields
- **Flags** each invoice as `verified` or `needs_review`, with the reason
- **Stores** results in SQLite (re-processing the same file updates it instead of duplicating it)
- **Web upload page** to process several files at once and filter the results
- **Excel report** with highlighted problem rows and a summary sheet
- **REST API** with automatic interactive docs

## Tech stack

Python · FastAPI · pdfplumber · Tesseract OCR (pytesseract) · SQLite · pandas · openpyxl · HTML/CSS/JavaScript

## How it works

```
PDF / image
    │
    ├─ has text? ──► read PDF text
    └─ scan/photo? ─► OCR (Tesseract)
    │
    ▼
Extract fields (regex)
    │
    ▼
Validate (subtotal + tax = total, date, required fields)
    │
    ├─ OK ──────► verified
    └─ problem ─► needs_review (with reason)
    │
    ▼
SQLite ──► Web page · REST API · Excel report · CSV
```

## Project structure

```
├── main.py              # FastAPI app (web page + API)
├── run_batch.py         # process a whole folder -> database + CSV
├── requirements.txt
├── static/
│   └── index.html       # upload page
├── src/
│   ├── pdf_reader.py    # read PDF text, choose OCR when needed
│   ├── ocr_processor.py # OCR for scans and images
│   ├── extractor.py     # extract invoice fields
│   ├── validator.py     # check the values
│   ├── pipeline.py      # connects the steps
│   ├── database.py      # SQLite storage
│   └── report_generator.py  # Excel report
├── invoices/            # sample invoices
└── output/              # generated reports
```

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install Tesseract OCR (needed for scans and photos)

- **Windows:** install from the UB Mannheim Tesseract builds. If `tesseract` is not found afterwards, open `src/ocr_processor.py` and set the path, for example:
  `pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"`
- **macOS:** `brew install tesseract`
- **Linux:** `sudo apt install tesseract-ocr`

PDFs that contain real text work without Tesseract.

### 3. Run it

**Web app and API**

```bash
uvicorn main:app --reload
```

- Upload page: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs

**Batch mode** (process every file in `invoices/`)

```bash
python run_batch.py
```

Results go to `invoices.db` and `output/results.csv`.

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/process-invoice` | Upload a PDF, PNG or JPG. Returns the extracted and validated data |
| `GET` | `/invoices` | List saved invoices. Filters: `?status=needs_review`, `?min_total=100000` |
| `GET` | `/report/excel` | Download the Excel report (optional `?status=`) |

## Example output

```json
{
  "invoice_number": "INV-1023",
  "date": "08/10/2026",
  "subtotal": 32500.0,
  "tax": 3250.0,
  "total": 35750.0,
  "status": "verified",
  "issues": ""
}
```

An invoice where the numbers don't add up:

```json
{
  "invoice_number": "ME-5050",
  "subtotal": 10000.0,
  "tax": 1000.0,
  "total": 50000.0,
  "status": "needs_review",
  "issues": "Subtotal + tax = 11,000.00 but total is 50,000.00"
}
```

## Limitations

- Extraction uses regular expressions, so unusual layouts may return empty fields. The validator flags these for review instead of guessing.
- OCR accuracy depends on image quality. Blurry or skewed photos may be misread.
- Line items (product, quantity, unit price) are not extracted yet.
- The web page has no login, so it is intended for local use.
- Sample invoices in `invoices/` are fictional.

## Roadmap

- [x] PDF text extraction
- [x] Validation rules and review status
- [x] SQLite storage and REST API
- [x] OCR for scanned invoices and photos
- [x] Web upload page and Excel report
- [ ] Line-item extraction with quantity × price checks
- [ ] LLM-based extraction for complex layouts
- [ ] Supplier field and duplicate invoice detection
- [ ] Authentication
- [ ] Docker and cloud deployment

## What I learned

Building this covered PDF and OCR processing, text extraction with regular expressions, data validation, database design, REST API development with FastAPI, and Git/GitHub workflow.
