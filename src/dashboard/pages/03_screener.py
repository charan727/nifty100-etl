import streamlit as st
import pandas as pd

from dashboard.utils.db import (
    get_ratios,
    get_companies
)

st.set_page_config(
    page_title="Stock Screener",
    layout="wide"
)

st.title("Stock Screener")

# ---------------------------------------
# Load Data
# ---------------------------------------

ratios = get_ratios()
companies = get_companies()

if ratios.empty:
    st.error("Financial ratios not found.")
    st.stop()

companies = companies.rename(
    columns={
        "id": "company_id"
    }
)

df = ratios.merge(
    companies[
        [
            "company_id",
            "company_name"
        ]
    ],
    how="left",
    on="company_id"
)

# ---------------------------------------
# Sidebar Filters
# ---------------------------------------

st.sidebar.header("Filters")

years = sorted(
    df["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Year",
    years
)

roe = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    100.0,
    15.0
)

debt = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    10.0,
    2.0
)

fcf = st.sidebar.slider(
    "Minimum Free Cash Flow",
    float(df["free_cash_flow_cr"].min()),
    float(df["free_cash_flow_cr"].max()),
    0.0
)

revenue = st.sidebar.slider(
    "Minimum Revenue CAGR 5Y",
    -100.0,
    100.0,
    0.0
)

pat = st.sidebar.slider(
    "Minimum PAT CAGR 5Y",
    -100.0,
    100.0,
    0.0
)

# ---------------------------------------
# Apply Filters
# ---------------------------------------

filtered = df[
    (df["year"] == selected_year)
    &
    (df["return_on_equity_pct"] >= roe)
    &
    (df["debt_to_equity"] <= debt)
    &
    (df["free_cash_flow_cr"] >= fcf)
    &
    (df["revenue_cagr_5yr"] >= revenue)
    &
    (df["pat_cagr_5yr"] >= pat)
].copy()

# Remove duplicate companies
filtered = (
    filtered
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
    .drop_duplicates(
        subset="company_id",
        keep="first"
    )
)

# ---------------------------------------
# Results
# ---------------------------------------

st.subheader("Results")

st.write(
    f"Showing {len(filtered)} companies"
)

display_cols = [
    "company_name",
    "company_id",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score"
]

display_cols = [
    c for c in display_cols
    if c in filtered.columns
]

st.dataframe(
    filtered[display_cols],
    use_container_width=True,
    hide_index=True
)

st.success("Screener Loaded Successfully")