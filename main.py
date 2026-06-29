import pandas as pd

from src.etl.loader import load_excel, load_to_database
from src.etl.database import (
    create_database,
    create_connection,
    execute_schema
)
from src.etl.normaliser import normalize_year, normalize_ticker
from src.etl.validator import (
    validate_dataframe,
    validate_primary_key,
    validate_positive_values
)

# Sprint 2
from src.etl.populate_financial_ratios import populate_financial_ratios


print("=" * 60)
print("NIFTY100 ETL PROJECT")
print("=" * 60)

# ------------------------------------
# Create Database
# ------------------------------------

create_database()
execute_schema()

conn = create_connection()

print("Database Connected Successfully!")

# ------------------------------------
# Core Files
# ------------------------------------

core_files = [
    "companies.xlsx",
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
]

# ------------------------------------
# Supporting Files
# ------------------------------------

supporting_files = [
    "financial_ratios.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

# ------------------------------------
# Load Core Files
# ------------------------------------

for file in core_files:

    print(f"\nLoading {file}...")

    df = load_excel(file)

    df = normalize_year(df)
    df = normalize_ticker(df)

    validate_dataframe(df)

    if "id" in df.columns:
        validate_primary_key(df, "id")

    numeric_columns = [
        "sales",
        "net_profit",
        "operating_profit",
        "total_assets",
        "total_liabilities",
        "equity",
        "eps"
    ]

    for column in numeric_columns:
        validate_positive_values(df, column)

    table_name = file.replace(".xlsx", "")

    load_to_database(df, table_name, conn)

# ------------------------------------
# Load Supporting Files
# ------------------------------------

for file in supporting_files:

    print(f"\nLoading {file}...")

    df = load_excel(file, data_type="supporting")

    df = normalize_year(df)
    df = normalize_ticker(df)

    validate_dataframe(df)

    if "id" in df.columns:
        validate_primary_key(df, "id")

    numeric_columns = [
        "sales",
        "net_profit",
        "operating_profit",
        "total_assets",
        "total_liabilities",
        "equity",
        "eps"
    ]

    for column in numeric_columns:
        validate_positive_values(df, column)

    table_name = file.replace(".xlsx", "")

    load_to_database(df, table_name, conn)

print("\nAll source files loaded successfully.")

# ------------------------------------
# Sprint 2 Financial Ratio Engine
# ------------------------------------

print("\nGenerating Financial Ratios...")

try:
    populate_financial_ratios()
    print("Financial Ratios Generated Successfully!")

except Exception as e:
    print(f"Ratio Engine Failed : {e}")

conn.close()

print("\nDatabase Connection Closed.")