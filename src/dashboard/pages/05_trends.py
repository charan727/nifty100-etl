import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_companies,
    get_ratios
)

st.set_page_config(
    page_title="Trend Analysis",
    layout="wide"
)

st.title("Trend Analysis")

# ---------------------------------------
# Load Data
# ---------------------------------------

companies = get_companies()
ratios = get_ratios()

if companies.empty or ratios.empty:
    st.error("Data not available.")
    st.stop()

companies = companies.rename(
    columns={
        "id": "company_id"
    }
)

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

# ---------------------------------------
# Company Selection
# ---------------------------------------

company_list = sorted(
    ratios["company_name"]
    .dropna()
    .unique()
)

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company_data = ratios[
    ratios["company_name"] == selected_company
].copy()

if company_data.empty:
    st.warning("No data available.")
    st.stop()

company_data = (
    company_data
    .sort_values("year")
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="last"
    )
    .fillna(0)
)

latest = company_data.iloc[-1]

# ---------------------------------------
# KPI Cards
# ---------------------------------------

st.subheader(selected_company)

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "ROE",
    round(latest["return_on_equity_pct"], 2)
)

c2.metric(
    "ROCE",
    round(latest["return_on_capital_employed_pct"], 2)
)

c3.metric(
    "Net Profit Margin",
    round(latest["net_profit_margin_pct"], 2)
)

c4.metric(
    "Debt / Equity",
    round(latest["debt_to_equity"], 2)
)

# ---------------------------------------
# Trend Charts
# ---------------------------------------

charts = [
    ("return_on_equity_pct", "ROE Trend"),
    ("return_on_capital_employed_pct", "ROCE Trend"),
    ("net_profit_margin_pct", "Net Profit Margin"),
    ("debt_to_equity", "Debt to Equity"),
    ("free_cash_flow_cr", "Free Cash Flow"),
    ("revenue_cagr_5yr", "Revenue CAGR 5Y"),
    ("pat_cagr_5yr", "PAT CAGR 5Y")
]

for col, title in charts:

    if col not in company_data.columns:
        continue

    st.divider()

    st.subheader(title)

    fig = px.line(
        company_data,
        x="year",
        y=col,
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------
# Financial History
# ---------------------------------------

st.divider()

st.subheader("Financial History")

st.dataframe(
    company_data,
    use_container_width=True,
    hide_index=True
)

st.success("Trend Analysis Loaded Successfully")