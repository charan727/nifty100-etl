import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_company_profile
)

st.title("Company Profile")

companies = get_companies()

company_list = sorted(companies["id"].dropna().unique())

ticker = st.selectbox(
    "Select Company",
    company_list
)

profile = get_company_profile(ticker)
ratios = get_ratios(ticker)

if profile.empty or ratios.empty:
    st.warning("Ticker not found.")
    st.stop()

company = profile.iloc[0]

st.subheader(company["company_name"])

st.write("Ticker :", company["id"])
st.write("Sector :", company["broad_sector"])
st.write("Sub Sector :", company["sub_sector"])

latest = ratios.sort_values(
    "year",
    ascending=False
).iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric(
    "ROE",
    round(latest["return_on_equity_pct"], 2)
)

col2.metric(
    "ROCE",
    round(latest["return_on_capital_employed_pct"], 2)
)

col3.metric(
    "Net Profit Margin",
    round(latest["net_profit_margin_pct"], 2)
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Debt to Equity",
    round(latest["debt_to_equity"], 2)
)

col5.metric(
    "Revenue CAGR 5Y",
    round(latest["revenue_cagr_5yr"], 2)
)

col6.metric(
    "Free Cash Flow",
    round(latest["free_cash_flow_cr"], 2)
)

st.divider()

st.subheader("Revenue Trend")

fig = px.line(
    ratios.sort_values("year"),
    x="year",
    y="revenue_cagr_5yr",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("ROE vs ROCE")

fig = px.line(
    ratios.sort_values("year"),
    x="year",
    y=[
        "return_on_equity_pct",
        "return_on_capital_employed_pct"
    ],
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Financial History")

st.dataframe(
    ratios.sort_values("year"),
    use_container_width=True
)
st.subheader("Pros & Cons")

pros = []

if latest["return_on_equity_pct"] >= 15:
    pros.append("Good Return on Equity")

if latest["debt_to_equity"] <= 1:
    pros.append("Low Debt")

if latest["free_cash_flow_cr"] > 0:
    pros.append("Positive Free Cash Flow")

for item in pros:
    st.success(item)

cons = []

if latest["return_on_equity_pct"] < 10:
    cons.append("Low ROE")

if latest["debt_to_equity"] > 2:
    cons.append("High Debt")

if latest["free_cash_flow_cr"] <= 0:
    cons.append("Negative Free Cash Flow")

for item in cons:
    st.error(item)

if len(cons) == 0:
    st.info("No major concerns found.")