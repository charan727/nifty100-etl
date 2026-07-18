import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.title("Home Dashboard")

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

if companies.empty or ratios.empty or sectors.empty:
    st.error("Required data is not available.")
    st.stop()

# Latest Year
latest_year = ratios["year"].max()

year = st.sidebar.selectbox(
    "Select Year",
    sorted(ratios["year"].dropna().unique(), reverse=True),
    index=0
)

ratios = ratios[ratios["year"] == year].copy()

# Remove duplicate company rows
ratios = (
    ratios
    .sort_values("year")
    .drop_duplicates(subset="company_id", keep="last")
)

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric(
    "Average ROE",
    f"{ratios['return_on_equity_pct'].mean():.2f}"
)

col2.metric(
    "Median D/E",
    f"{ratios['debt_to_equity'].median():.2f}"
)

col3.metric(
    "Companies",
    len(ratios)
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Median Revenue CAGR",
    f"{ratios['revenue_cagr_5yr'].median():.2f}"
)

col5.metric(
    "Debt Free Companies",
    int((ratios["debt_to_equity"] == 0).sum())
)

if "pe_ratio" in ratios.columns:
    pe = f"{ratios['pe_ratio'].median():.2f}"
else:
    pe = "N/A"

col6.metric(
    "Median P/E",
    pe
)

st.divider()

# Sector Distribution
st.subheader("Sector Distribution")

sector_counts = (
    sectors["broad_sector"]
    .value_counts()
    .reset_index()
)

sector_counts.columns = [
    "Sector",
    "Companies"
]

fig = px.pie(
    sector_counts,
    names="Sector",
    values="Companies",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# Top Companies
st.subheader("Top Companies by Composite Score")

if "composite_quality_score" in ratios.columns:

    top = (
        ratios
        .sort_values(
            "composite_quality_score",
            ascending=False
        )
        .head(5)
    )

    st.dataframe(
        top[
            [
                "company_id",
                "return_on_equity_pct",
                "debt_to_equity",
                "composite_quality_score"
            ]
        ],
        use_container_width=True
    )