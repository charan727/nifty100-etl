import streamlit as st
import plotly.express as px
import pandas as pd

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

st.title("Trend Analysis")

companies = get_companies()

company_list = sorted(companies["id"].dropna().unique())

ticker = st.selectbox(
    "Select Company",
    company_list
)

ratios = get_ratios(ticker)

if ratios.empty:
    st.warning("No data available.")
    st.stop()

ratios = ratios.sort_values("year").fillna(0)

latest = ratios.iloc[-1]

st.subheader(f"Company : {ticker}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "ROE",
    round(latest.get("return_on_equity_pct", 0), 2)
)

col2.metric(
    "ROCE",
    round(latest.get("return_on_capital_employed_pct", 0), 2)
)

col3.metric(
    "Net Profit Margin",
    round(latest.get("net_profit_margin_pct", 0), 2)
)

col4.metric(
    "Debt / Equity",
    round(latest.get("debt_to_equity", 0), 2)
)

chart_columns = [
    ("return_on_equity_pct", "ROE Trend"),
    ("return_on_capital_employed_pct", "ROCE Trend"),
    ("net_profit_margin_pct", "Net Profit Margin Trend"),
    ("debt_to_equity", "Debt To Equity Trend"),
    ("revenue_cagr_5yr", "Revenue CAGR Trend"),
    ("pat_cagr_5yr", "PAT CAGR Trend"),
    ("free_cash_flow_cr", "Free Cash Flow Trend")
]

for column, title in chart_columns:

    st.divider()
    st.subheader(title)

    if column in ratios.columns:

        fig = px.line(
            ratios,
            x="year",
            y=column,
            markers=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(f"{column} not available.")

st.divider()

st.subheader("Financial History")

st.dataframe(
    ratios,
    use_container_width=True
)