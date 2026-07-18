import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import (
    get_ratios,
    get_companies
)

st.title("Peer Comparison")

companies = get_companies()

company_list = sorted(companies["id"].unique())

ticker = st.selectbox(
    "Select Company",
    company_list
)

ratios = get_ratios()

company_data = ratios[
    ratios["company_id"] == ticker
]

if company_data.empty:
    st.warning("Company not found")
    st.stop()

latest_year = company_data["year"].max()

peer_df = ratios[
    ratios["year"] == latest_year
].copy()

peer_df = (
    peer_df.sort_values("year")
    .drop_duplicates(subset="company_id", keep="last")
)

peer_df = peer_df.sort_values(
    "composite_quality_score",
    ascending=False
)

st.subheader(f"Comparison - {latest_year}")

st.dataframe(
    peer_df[
        [
            "company_id",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "debt_to_equity",
            "net_profit_margin_pct",
            "composite_quality_score"
        ]
    ],
    use_container_width=True
)

st.divider()

st.subheader("ROE Comparison")

fig = px.bar(
    peer_df,
    x="company_id",
    y="return_on_equity_pct",
    color="return_on_equity_pct",
    text="return_on_equity_pct"
)

fig.update_layout(xaxis_title="Company", yaxis_title="ROE")

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("ROCE Comparison")

fig = px.bar(
    peer_df,
    x="company_id",
    y="return_on_capital_employed_pct",
    color="return_on_capital_employed_pct",
    text="return_on_capital_employed_pct"
)

fig.update_layout(xaxis_title="Company", yaxis_title="ROCE")

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Debt To Equity")

fig = px.bar(
    peer_df,
    x="company_id",
    y="debt_to_equity",
    color="debt_to_equity",
    text="debt_to_equity"
)

fig.update_layout(xaxis_title="Company", yaxis_title="Debt to Equity")

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Composite Quality Score")

fig = px.bar(
    peer_df,
    x="company_id",
    y="composite_quality_score",
    color="composite_quality_score",
    text="composite_quality_score"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Composite Score",
    yaxis=dict(range=[0, 110])
)

st.plotly_chart(fig, use_container_width=True)