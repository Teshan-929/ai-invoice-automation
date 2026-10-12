import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from src.pipeline import process_invoice

app = FastAPI(title="AI Invoice Processing")

UPLOAD_DIR = Path(__file__).parent / "invoices" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Invoice Processing & Business Automation System"}

@app.post("/process-invoice")
async def process_invoice_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported for now")

    save_path = UPLOAD_DIR / Path(file.filename).name
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return {"file": file.filename, "data": process_invoice(save_path)}