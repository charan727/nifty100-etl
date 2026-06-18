from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CORE_DATA_PATH = BASE_DIR / "data" / "core"
SUPPORTING_DATA_PATH = BASE_DIR / "data" / "supporting"

DATABASE_PATH = BASE_DIR / "db" / "nifty100.db"

OUTPUT_PATH = BASE_DIR / "output"