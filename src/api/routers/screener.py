from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter()


@router.get("/screener")
def stock_screener(
    min_roe: float = Query(0),
    min_roce: float = Query(0),
    min_book_value: float = Query(0),
    min_face_value: float = Query(0),
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            company_name,
            roe_percentage,
            roce_percentage,
            book_value,
            face_value,
            website
        FROM companies
        WHERE
            COALESCE(roe_percentage,0) >= ?
            AND COALESCE(roce_percentage,0) >= ?
            AND COALESCE(book_value,0) >= ?
            AND COALESCE(face_value,0) >= ?
        ORDER BY roe_percentage DESC
        """,
        (
            min_roe,
            min_roce,
            min_book_value,
            min_face_value,
        ),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]