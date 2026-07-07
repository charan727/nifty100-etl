import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from pathlib import Path

from src.config import DATABASE_PATH


REPORT_PATH = (
    Path(__file__).resolve().parents[2]
    / "reports"
    / "radar_charts"
)

REPORT_PATH.mkdir(parents=True, exist_ok=True)


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
    fr.pat_cagr_5yr,
    fr.revenue_cagr_5yr,
    fr.composite_quality_score,
    pp.peer_group_name
FROM financial_ratios fr
INNER JOIN peer_groups pp
ON fr.company_id = pp.company_id
"""

df = pd.read_sql(query, conn)

conn.close()


# latest year only
df = (
    df.sort_values("year")
      .groupby("company_id")
      .tail(1)
      .reset_index(drop=True)
)


metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score"
]


# Generate one radar chart per company

for _, row in df.iterrows():

    company = row["company_id"]
    peer = row["peer_group_name"]

    peer_df = df[df["peer_group_name"] == peer]

    peer_avg = (
        peer_df[metrics]
        .fillna(0)
        .mean()
        .tolist()
    )

    company_values = (
        row[metrics]
        .fillna(0)
        .tolist()
    )

    labels = [
        "ROE",
        "ROCE",
        "NPM",
        "D/E",
        "FCF",
        "PAT CAGR",
        "REV CAGR",
        "Score"
    ]

    N = len(labels)

    angles = [
        n / float(N) * 2 * pi
        for n in range(N)
    ]

    angles += angles[:1]

    company_values += company_values[:1]
    peer_avg += peer_avg[:1]

    plt.figure(figsize=(8, 8))

    ax = plt.subplot(111, polar=True)

    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    plt.xticks(
        angles[:-1],
        labels
    )

    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_avg,
        linestyle="dashed",
        linewidth=2,
        label="Peer Avg"
    )

    plt.title(
        f"{company} Radar Chart"
    )

    plt.legend(
        loc="upper right"
    )

    plt.savefig(
        REPORT_PATH / f"{company}_radar.png"
    )

    plt.close()

print("===================================")
print("Radar Charts Generated Successfully")
print("Location :", REPORT_PATH)
print("Total Charts :", len(df))
print("===================================")