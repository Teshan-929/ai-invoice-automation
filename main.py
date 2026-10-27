import shutil
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from src.pipeline import process_invoice, SUPPORTED
from src.database import init_db, save_invoice, get_invoices

app = FastAPI(title="AI Invoice Processing")

UPLOAD_DIR = Path(__file__).parent / "invoices" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

init_db()


@app.get("/")
def home():
    return {"message": "AI Invoice Processing & Business Automation System"}


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