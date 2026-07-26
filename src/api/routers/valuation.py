from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/valuation/{company_id}")
def get_company_valuation(company_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            company_id,
            year,
            market_cap_crore,
            enterprise_value_crore,
            pe_ratio,
            pb_ratio,
            ev_ebitda,
            dividend_yield_pct
        FROM market_cap
        WHERE UPPER(company_id)=UPPER(?)
        ORDER BY year DESC
        """,
        (company_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"error": "Valuation data not found"}

    return [dict(row) for row in rows]