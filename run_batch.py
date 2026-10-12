from pathlib import Path
import pandas as pd
from src.pipeline import process_invoice

BASE_DIR = Path(__file__).parent
INVOICE_DIR = BASE_DIR / "invoices"
OUTPUT_DIR = BASE_DIR / "output"

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    results = []

    for pdf_path in sorted(INVOICE_DIR.glob("*.pdf")):
        try:
            fields = process_invoice(pdf_path)
        except Exception as e:
            fields = {"error": str(e)}
        fields["file"] = pdf_path.name
        results.append(fields)
        print(pdf_path.name, "->", fields)

    pd.DataFrame(results).to_csv(OUTPUT_DIR / "results.csv", index=False)
    print(f"\nSaved {len(results)} invoices to output/results.csv")

if __name__ == "__main__":
    main()