from pathlib import Path

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/v1",
    tags=["Tearsheet"]
)

REPORT_DIR = Path("reports/tearsheets")


@router.get("/tearsheet/{company_name}")
def get_tearsheet(company_name: str):

    for pdf in REPORT_DIR.glob("*.pdf"):
        if company_name.lower() in pdf.stem.lower():
            return {
                "company": pdf.stem,
                "file": str(pdf)
            }

    return {"error": "Tearsheet not found"}