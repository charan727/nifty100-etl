import streamlit as st
import plotly.express as px

from src.dashboard.utils.db import get_sectors

st.title("Capital Analysis")

sectors = get_sectors()

if sectors.empty:
    st.error("No sector data available.")
    st.stop()

st.subheader("Market Cap Distribution")

cap_filter = st.selectbox(
    "Select Market Cap",
    ["All"] + sorted(sectors["market_cap_category"].dropna().unique().tolist())
)

filtered = sectors.copy()

if cap_filter != "All":
    filtered = filtered[
        filtered["market_cap_category"] == cap_filter
    ]

col1, col2 = st.columns(2)

col1.metric(
    "Companies",
    len(filtered)
)

col2.metric(
    "Average Index Weight",
    f"{filtered['index_weight_pct'].mean():.2f}%"
)

st.divider()

cap_counts = (
    filtered["market_cap_category"]
    .value_counts()
    .reset_index()
)

cap_counts.columns = [
    "Market Cap",
    "Companies"
]

fig = px.pie(
    cap_counts,
    names="Market Cap",
    values="Companies",
    hole=0.45,
    title="Market Cap Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

sector_counts = (
    filtered["broad_sector"]
    .value_counts()
    .reset_index()
)

sector_counts.columns = [
    "Sector",
    "Companies"
]

fig = px.bar(
    sector_counts,
    x="Sector",
    y="Companies",
    color="Companies",
    text="Companies",
    title="Sector-wise Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("Capital Master Data")

st.dataframe(
    filtered,
    use_container_width=True
)