import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_ratios,
    get_companies
)

st.set_page_config(
    page_title="Peer Comparison",
    layout="wide"
)

st.title("Peer Comparison")

# ---------------------------------------
# Load Data
# ---------------------------------------

ratios = get_ratios()
companies = get_companies()

if ratios.empty:
    st.error("Financial ratio data not found.")
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

selected = ratios[
    ratios["company_name"] == selected_company
]

if selected.empty:
    st.warning("Company not found.")
    st.stop()

latest_year = selected["year"].max()

peer_df = ratios[
    ratios["year"] == latest_year
].copy()

peer_df = (
    peer_df
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
    .drop_duplicates(
        subset="company_id",
        keep="first"
    )
)

st.subheader(f"Comparison - {latest_year}")

display_cols = [
    "company_name",
    "company_id",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "debt_to_equity",
    "net_profit_margin_pct",
    "composite_quality_score"
]

display_cols = [
    c for c in display_cols
    if c in peer_df.columns
]

st.dataframe(
    peer_df[display_cols],
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------------------------------
# ROE
# ---------------------------------------

st.subheader("ROE Comparison")

fig = px.bar(
    peer_df,
    x="company_name",
    y="return_on_equity_pct",
    color="return_on_equity_pct",
    text="return_on_equity_pct"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="ROE"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# ROCE
# ---------------------------------------

st.subheader("ROCE Comparison")

fig = px.bar(
    peer_df,
    x="company_name",
    y="return_on_capital_employed_pct",
    color="return_on_capital_employed_pct",
    text="return_on_capital_employed_pct"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="ROCE"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# Debt / Equity
# ---------------------------------------

st.subheader("Debt to Equity")

fig = px.bar(
    peer_df,
    x="company_name",
    y="debt_to_equity",
    color="debt_to_equity",
    text="debt_to_equity"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Debt / Equity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# Composite Score
# ---------------------------------------

st.subheader("Composite Quality Score")

fig = px.bar(
    peer_df,
    x="company_name",
    y="composite_quality_score",
    color="composite_quality_score",
    text="composite_quality_score"
)

fig.update_layout(
    xaxis_title="Company",
    yaxis_title="Composite Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success("Peer Comparison Loaded Successfully")