from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter(prefix="/api/v1", tags=["Documents"])


@router.get("/documents/{company_id}")
def get_documents(company_id: str):

    conn = get_connection()
    conn.row_factory = __import__("sqlite3").Row
    cur = conn.cursor()

    cur.execute("""
        SELECT
            company_id,
            year,
            annual_report
        FROM documents
        WHERE UPPER(company_id)=UPPER(?)
        ORDER BY year DESC
    """, (company_id,))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {"error": "Company not found"}

    return [dict(r) for r in rows]