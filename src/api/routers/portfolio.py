from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/portfolio/stats")
def portfolio_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS companies,
            ROUND(AVG(roe_percentage),2) AS avg_roe,
            ROUND(AVG(roce_percentage),2) AS avg_roce,
            ROUND(AVG(book_value),2) AS avg_book_value,
            ROUND(AVG(face_value),2) AS avg_face_value
        FROM companies
    """)

    row = cursor.fetchone()

    conn.close()

    return dict(row)