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

    # Remove existing records only (schema remains)
    connection.execute(f"DELETE FROM {table_name}")

    # Insert data into existing table
    df.to_sql(
        name=table_name,
        con=connection,
        if_exists="append",
        index=False
    )

    connection.commit()

    print(f"{table_name} loaded successfully!")

    audit = pd.DataFrame({
        "table_name": [table_name],
        "row_count": [len(df)]
    })

    audit.to_csv(
        "output/load_audit.csv",
        mode="a",
        header=False,
        index=False
    )