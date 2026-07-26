from fastapi import APIRouter

from src.api.database import get_connection

router = APIRouter()


@router.get("/health")
def health():

    conn = get_connection()

    cursor = conn.cursor()

    tables = [
        "companies",
        "financial_ratios",
        "balancesheet",
        "cashflow",
        "profitandloss"
    ]

    counts = {}

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        counts[table] = cursor.fetchone()[0]

    conn.close()

    return {
        "status": "ok",
        "version": "1.0.0",
        "db_row_counts": counts
    }