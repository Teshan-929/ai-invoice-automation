from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HEADERS = ["File", "Invoice No", "Date", "Subtotal", "Tax", "Total", "Status", "Issues"]
KEYS = ["file", "invoice_number", "date", "subtotal", "tax", "total", "status", "issues"]

HEADER_FILL = PatternFill("solid", fgColor="1F3A5F")
REVIEW_FILL = PatternFill("solid", fgColor="FDE2E2")
OK_FILL = PatternFill("solid", fgColor="E3F4E8")


def generate_excel_report(invoices, path):
    """Write invoices to a formatted .xlsx file and return the path."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"

    ws.append(HEADERS)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(horizontal="center")

    for inv in invoices:
        ws.append([inv.get(k) for k in KEYS])
        row = ws.max_row
        for col in (4, 5, 6):  # subtotal, tax, total
            ws.cell(row, col).number_format = "#,##0.00"
        fill = OK_FILL if inv.get("status") == "verified" else REVIEW_FILL
        ws.cell(row, 7).fill = fill
        if inv.get("status") != "verified":
            for col in range(1, len(HEADERS) + 1):
                ws.cell(row, col).fill = REVIEW_FILL

    for i, header in enumerate(HEADERS, start=1):
        longest = max([len(str(header))] + [
            len(str(ws.cell(r, i).value or "")) for r in range(2, ws.max_row + 1)])
        ws.column_dimensions[get_column_letter(i)].width = min(longest + 3, 60)
    ws.freeze_panes = "A2"

    # Summary sheet
    summary = wb.create_sheet("Summary")
    verified = [i for i in invoices if i.get("status") == "verified"]
    review = [i for i in invoices if i.get("status") != "verified"]
    rows = [
        ("Report generated", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Total invoices", len(invoices)),
        ("Verified", len(verified)),
        ("Needs review", len(review)),
        ("Total value (all)", sum(i.get("total") or 0 for i in invoices)),
        ("Total value (verified only)", sum(i.get("total") or 0 for i in verified)),
    ]
    for label, value in rows:
        summary.append([label, value])
        summary.cell(summary.max_row, 1).font = Font(bold=True)
    for r in (5, 6):
        summary.cell(r, 2).number_format = "#,##0.00"
    summary.column_dimensions["A"].width = 30
    summary.column_dimensions["B"].width = 20

    wb.save(path)
    return path