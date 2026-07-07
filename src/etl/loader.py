import pandas as pd
from src.config import CORE_DATA_PATH, SUPPORTING_DATA_PATH


def load_excel(file_name, data_type="core"):
    """
    Load Excel file from core or supporting folder.
    """

    if data_type == "supporting":
        file_path = SUPPORTING_DATA_PATH / file_name
    else:
        file_path = CORE_DATA_PATH / file_name

    # Different header rows
    if file_name in [
        "financial_ratios.xlsx",
        "market_cap.xlsx",
        "peer_groups.xlsx",
        "sectors.xlsx",
        "stock_prices.xlsx"
    ]:
        df = pd.read_excel(file_path, header=0)
    else:
        df = pd.read_excel(file_path, header=1)

    return df


def load_to_database(df, table_name, connection):
    """
    Load DataFrame into SQLite table.
    """

    print(f"\nLoading table : {table_name}")
    print("Columns in Excel :", df.columns.tolist())

    cursor = connection.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    db_columns = [row[1] for row in cursor.fetchall()]

    print("Columns in DB :", db_columns)

    # Keep only matching columns
    common_columns = [c for c in df.columns if c in db_columns]

    df = df[common_columns]

    connection.execute(f"DELETE FROM {table_name}")

    df.to_sql(
        table_name,
        connection,
        if_exists="append",
        index=False
    )

    connection.commit()

    print(f"{table_name} loaded successfully!")