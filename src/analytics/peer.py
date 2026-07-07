import sqlite3
import pandas as pd
from src.config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH)

print("===== Financial Ratios =====")

df = pd.read_sql("""
SELECT DISTINCT company_id
FROM financial_ratios
LIMIT 20
""", conn)

print(df)

print("\n=========================\n")

print("===== Peer Groups =====")

df2 = pd.read_sql("""
SELECT company_id, peer_group_name
FROM peer_groups
LIMIT 20
""", conn)

print(df2)

conn.close()
print("\nCalculating Percentile Ranks...\n")

conn = sqlite3.connect(DATABASE_PATH)

query = """
SELECT
    fr.company_id,
    fr.year,
    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.net_profit_margin_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.eps_cagr_5yr,
    fr.interest_coverage,
    fr.asset_turnover,
    pg.peer_group_name
FROM financial_ratios fr
INNER JOIN peer_groups pg
ON fr.company_id = pg.company_id
"""

df = pd.read_sql(query, conn)

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover"
]

result = []

for metric in metrics:

    temp = df.copy()

    temp["percentile_rank"] = (
        temp.groupby("peer_group_name")[metric]
        .rank(pct=True)
    )

    temp["metric"] = metric

    temp["value"] = temp[metric]

result.append(
    temp[
        [
            "company_id",
            "peer_group_name",
            "year",
            "metric",
            "value",
            "percentile_rank"
        ]
    ]
)

peer_df = pd.concat(result)

print(peer_df.head())
# ---------------------------------------
# Save to SQLite
# ---------------------------------------

peer_df.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

print("\npeer_percentiles table created successfully!")
print("Rows Inserted :", len(peer_df))

conn.close()