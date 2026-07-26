from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM companies")
    companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM sectors")
    sectors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM peer_groups")
    peer_groups = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM financial_ratios")
    ratios = cursor.fetchone()[0]

    conn.close()

    return {
        "companies": companies,
        "sectors": sectors,
        "peer_groups": peer_groups,
        "financial_ratios": ratios
    }