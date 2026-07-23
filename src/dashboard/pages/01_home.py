import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_sectors
)

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide"
)

st.title("Nifty 100 Analytics Dashboard")

# -------------------------------------
# Load Data
# -------------------------------------

companies = get_companies()
ratios = get_ratios()
sectors = get_sectors()

if companies.empty:
    st.error("Companies data not found.")
    st.stop()

if ratios.empty:
    st.error("Financial Ratios data not found.")
    st.stop()

# -------------------------------------
# Year Filter
# -------------------------------------

years = sorted(
    ratios["year"].dropna().unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)

ratios = ratios[
    ratios["year"] == selected_year
].copy()

# -------------------------------------
# Merge Company Name
# -------------------------------------

if "id" in companies.columns:
    companies = companies.rename(
        columns={"id": "company_id"}
    )

if "company_name" in companies.columns:

    ratios = ratios.merge(
        companies[
            [
                "company_id",
                "company_name"
            ]
        ],
        on="company_id",
        how="left"
    )

ratios = ratios.drop_duplicates(
    subset="company_id",
    keep="last"
)

# -------------------------------------
# KPI Cards
# -------------------------------------

st.subheader("Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Average ROE",
    f"{ratios['return_on_equity_pct'].mean():.2f}%"
)

c2.metric(
    "Median Debt/Equity",
    f"{ratios['debt_to_equity'].median():.2f}"
)

c3.metric(
    "Companies",
    len(ratios)
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Median Revenue CAGR",
    f"{ratios['revenue_cagr_5yr'].median():.2f}%"
)

c5.metric(
    "Debt Free Companies",
    int(
        (ratios["debt_to_equity"] == 0).sum()
    )
)

if "price_earnings_ratio" in ratios.columns:

    c6.metric(
        "Median PE",
        f"{ratios['price_earnings_ratio'].median():.2f}"
    )

else:

    c6.metric(
        "Median PE",
        "N/A"
    )

st.divider()

# -------------------------------------
# Sector Distribution
# -------------------------------------

st.subheader("Sector Distribution")

if (
    not sectors.empty
    and "broad_sector" in sectors.columns
):

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


# -------------------------------------
# Top Companies by Composite Score
# -------------------------------------

st.subheader("Top Companies by Composite Quality Score")

if "composite_quality_score" in ratios.columns:

    top = (
        ratios
        .sort_values(
            "composite_quality_score",
            ascending=False
        )
        .head(10)
    )

    cols = [
        c for c in [
            "company_id",
            "company_name",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
            "composite_quality_score"
        ]
        if c in top.columns
    ]

    st.dataframe(
        top[cols],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -------------------------------------
# Top ROE Companies
# -------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("Top ROE Companies")

    roe_df = (
        ratios
        .sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    cols = [
        c for c in [
            "company_name",
            "company_id",
            "return_on_equity_pct"
        ]
        if c in roe_df.columns
    ]

    st.dataframe(
        roe_df[cols],
        use_container_width=True,
        hide_index=True
    )

with right:

    st.subheader("Top ROCE Companies")

    roce_df = (
        ratios
        .sort_values(
            "return_on_capital_employed_pct",
            ascending=False
        )
        .head(10)
    )

    cols = [
        c for c in [
            "company_name",
            "company_id",
            "return_on_capital_employed_pct"
        ]
        if c in roce_df.columns
    ]

    st.dataframe(
        roce_df[cols],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -------------------------------------
# Free Cash Flow Leaders
# -------------------------------------

if "free_cash_flow_cr" in ratios.columns:

    st.subheader("Top Free Cash Flow Companies")

    fcf = (
        ratios
        .sort_values(
            "free_cash_flow_cr",
            ascending=False
        )
        .head(10)
    )

    cols = [
        c for c in [
            "company_name",
            "company_id",
            "free_cash_flow_cr"
        ]
        if c in fcf.columns
    ]

    st.dataframe(
        fcf[cols],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -------------------------------------
# Revenue CAGR Leaders
# -------------------------------------

if "revenue_cagr_5yr" in ratios.columns:

    st.subheader("Top Revenue CAGR Companies")

    growth = (
        ratios
        .sort_values(
            "revenue_cagr_5yr",
            ascending=False
        )
        .head(10)
    )

    cols = [
        c for c in [
            "company_name",
            "company_id",
            "revenue_cagr_5yr"
        ]
        if c in growth.columns
    ]

    st.dataframe(
        growth[cols],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# -------------------------------------
# Dataset Summary
# -------------------------------------

st.subheader("Dataset Summary")

summary = pd.DataFrame({
    "Metric": [
        "Selected Year",
        "Companies",
        "Average ROE",
        "Median Debt/Equity",
        "Average ROCE",
        "Average Net Profit Margin"
    ],
    "Value": [
        selected_year,
        len(ratios),
        round(ratios["return_on_equity_pct"].mean(), 2),
        round(ratios["debt_to_equity"].median(), 2),
        round(ratios["return_on_capital_employed_pct"].mean(), 2),
        round(ratios["net_profit_margin_pct"].mean(), 2)
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.success("Home Dashboard Loaded Successfully")