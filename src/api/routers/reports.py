from pathlib import Path

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Reports"]
)

SECTOR_DIR = Path("reports/sector")


@router.get("/reports/sectors")
def get_sector_reports():

    files = []

    for pdf in sorted(SECTOR_DIR.glob("*.pdf")):
        files.append({
            "sector": pdf.stem,
            "file": str(pdf)
        })

    return files