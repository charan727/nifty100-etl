from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")

CORE_DATA_PATH = Path(os.getenv("CORE_DATA_PATH"))
SUPPORTING_DATA_PATH = Path(os.getenv("SUPPORTING_DATA_PATH"))
DATABASE_PATH = Path(os.getenv("DATABASE_PATH"))
OUTPUT_PATH = Path(os.getenv("OUTPUT_PATH"))