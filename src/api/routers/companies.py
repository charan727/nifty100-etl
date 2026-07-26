from fastapi import APIRouter, Query
from src.api.database import get_connection

router = APIRouter()


@router.get("/companies")
def get_companies():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            company_name,
            website,
            face_value,
            book_value,
            roce_percentage,
            roe_percentage
        FROM companies
        ORDER BY company_name
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@router.get("/companies/{company_id}")
def get_company(company_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE
            LOWER(id)=LOWER(?)
            OR LOWER(company_name) LIKE ?
        LIMIT 1
        """,
        (
            company_id,
            f"%{company_id.lower()}%"
        )
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {"error": "Company not found"}

    return dict(row)


@router.get("/search")
def search_companies(name: str = Query(...)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            company_name
        FROM companies
        WHERE
            LOWER(company_name) LIKE ?
            OR LOWER(id) LIKE ?
        ORDER BY company_name
        """,
        (
            f"%{name.lower()}%",
            f"%{name.lower()}%"
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]