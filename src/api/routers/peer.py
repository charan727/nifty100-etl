from fastapi import APIRouter
from src.api.database import get_connection

router = APIRouter()


@router.get("/peer-groups")
def get_peer_groups():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            peer_group_name,
            COUNT(*) AS company_count
        FROM peer_groups
        GROUP BY peer_group_name
        ORDER BY peer_group_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


@router.get("/peer-groups/{group_name}")
def get_peer_group(group_name: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.peer_group_name,
            p.company_id,
            p.is_benchmark,
            c.company_name,
            c.roe_percentage,
            c.roce_percentage
        FROM peer_groups p
        JOIN companies c
            ON p.company_id = c.id
        WHERE LOWER(p.peer_group_name)=LOWER(?)
        ORDER BY c.company_name
    """, (group_name,))

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return {
            "error": "Peer group not found"
        }

    return [dict(row) for row in rows]