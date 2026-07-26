from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/ratios/{company_id}")
def get_company_ratios(company_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,
            return_on_capital_employed_pct,
            return_on_assets_pct,
            debt_to_equity,
            interest_coverage,
            asset_turnover,
            earnings_per_share,
            book_value_per_share,
            revenue_cagr_3yr,
            revenue_cagr_5yr,
            pat_cagr_3yr,
            pat_cagr_5yr,
            composite_quality_score
        FROM financial_ratios
        WHERE UPPER(company_id) = UPPER(?)
        ORDER BY year DESC
        """,
        (company_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {
            "error": "Financial ratios not found"
        }

    return [dict(row) for row in rows]