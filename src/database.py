import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "invoices.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # rows behave like dictionaries
    return conn


def init_db():
    """Create the invoices table if it does not exist yet."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                file           TEXT UNIQUE,
                invoice_number TEXT,
                date           TEXT,
                subtotal       REAL,
                tax            REAL,
                total          REAL,
                status         TEXT,
                issues         TEXT,
                created_at     TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


def save_invoice(invoice):
    """Insert an invoice, or update it if the same file was saved before."""
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO invoices
                (file, invoice_number, date, subtotal, tax, total, status, issues)
            VALUES
                (:file, :invoice_number, :date, :subtotal, :tax, :total, :status, :issues)
            ON CONFLICT(file) DO UPDATE SET
                invoice_number = excluded.invoice_number,
                date           = excluded.date,
                subtotal       = excluded.subtotal,
                tax            = excluded.tax,
                total          = excluded.total,
                status         = excluded.status,
                issues         = excluded.issues
        """, {k: invoice.get(k) for k in (
            "file", "invoice_number", "date", "subtotal",
            "tax", "total", "status", "issues")})


def get_invoices(status=None, min_total=None):
    """Return invoices as a list of dicts, optionally filtered."""
    query = "SELECT * FROM invoices WHERE 1=1"
    params = []
    if status:
        query += " AND status = ?"
        params.append(status)
    if min_total is not None:
        query += " AND total >= ?"
        params.append(min_total)
    query += " ORDER BY id"
    with get_connection() as conn:
        return [dict(row) for row in conn.execute(query, params)]