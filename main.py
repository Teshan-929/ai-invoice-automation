import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.pipeline import process_invoice, SUPPORTED
from src.database import init_db, save_invoice, get_invoices
from src.report_generator import generate_excel_report

app = FastAPI(title="AI Invoice Processing")

UPLOAD_DIR = Path(__file__).parent / "invoices" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = Path(__file__).parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
STATIC_DIR = Path(__file__).parent / "static"

init_db()


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/process-invoice")
async def process_invoice_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(SUPPORTED):
        raise HTTPException(status_code=400, detail="Upload a PDF, PNG or JPG file")

    save_path = UPLOAD_DIR / Path(file.filename).name
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    data = process_invoice(save_path)
    data["file"] = save_path.name
    save_invoice(data)
    return {"file": save_path.name, "data": data}


@app.get("/invoices")
def list_invoices(status: Optional[str] = None, min_total: Optional[float] = None):
    """List saved invoices. Try ?status=needs_review or ?min_total=100000"""
    return get_invoices(status=status, min_total=min_total)


@app.get("/report/excel")
def download_excel_report(status: Optional[str] = None):
    """Download all (or filtered) invoices as an Excel report."""
    path = generate_excel_report(get_invoices(status=status), OUTPUT_DIR / "invoice_report.xlsx")
    return FileResponse(
        path, filename="invoice_report.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")