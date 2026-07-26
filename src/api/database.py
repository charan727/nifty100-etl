import sqlite3
from pathlib import Path


DATABASE_PATH = Path("db") / "nifty100.db"


def get_connection():
    """
    Returns SQLite connection.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn