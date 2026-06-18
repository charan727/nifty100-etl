import sqlite3
from pathlib import Path
from src.config import DATABASE_PATH


def create_database():
    """
    Create SQLite database.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    print("Database created successfully!")
    conn.close()


def create_connection():
    """
    Create SQLite connection.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def execute_schema():
    """
    Execute schema.sql and create all tables.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    schema_path = Path(__file__).resolve().parents[2] / "db" / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    print("All tables created successfully!")