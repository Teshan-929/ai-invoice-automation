from pathlib import Path
import pandas as pd
from src.pipeline import process_invoice, SUPPORTED
from src.database import init_db, save_invoice

BASE_DIR = Path(__file__).parent
INVOICE_DIR = BASE_DIR / "invoices"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    init_db()
    results = []

    for pdf_path in sorted(p for p in INVOICE_DIR.iterdir() if p.suffix.lower() in SUPPORTED):
        try:
            fields = process_invoice(pdf_path)
        except Exception as e:
            fields = {"status": "error", "issues": str(e)}
        fields["file"] = pdf_path.name
        save_invoice(fields)
        results.append(fields)
        print(f"{pdf_path.name:24} {fields.get('status'):13} {fields.get('issues', '')}")

    pd.DataFrame(results).to_csv(OUTPUT_DIR / "results.csv", index=False)
    print(f"\nSaved {len(results)} invoices to invoices.db and output/results.csv")


if __name__ == "__main__":
    main()