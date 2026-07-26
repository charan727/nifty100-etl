from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/sectors")
def get_all_sectors():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.broad_sector AS sector,
            COUNT(*) AS company_count,
            ROUND(AVG(c.roe_percentage),2) AS avg_roe,
            ROUND(AVG(c.roce_percentage),2) AS avg_roce
        FROM sectors s
        JOIN companies c
            ON s.company_id = c.id
        GROUP BY s.broad_sector
        ORDER BY s.broad_sector
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@router.get("/sectors/{sector_name}")
def get_sector_companies(sector_name: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,
            s.sub_sector,
            c.roe_percentage,
            c.roce_percentage,
            c.website
        FROM companies c
        JOIN sectors s
            ON c.id = s.company_id
        WHERE LOWER(s.broad_sector)=LOWER(?)
        ORDER BY c.company_name
    """, (sector_name,))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {
            "error": "Sector not found"
        }

    return [dict(row) for row in rows]