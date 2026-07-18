import streamlit as st

from src.dashboard.utils.db import (
    get_sectors
)

st.title("Sector Analysis")

sectors = get_sectors()

if sectors.empty:
    st.error("Sector data not found.")
    st.stop()

st.subheader("Sector Master Data")

st.write(f"Total Records : {len(sectors)}")
st.divider()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Companies",
    sectors["company_id"].nunique()
)

col2.metric(
    "Broad Sectors",
    sectors["broad_sector"].nunique()
)

col3.metric(
    "Sub Sectors",
    sectors["sub_sector"].nunique()
)

st.divider()
st.dataframe(
    sectors,
    use_container_width=True
)
import plotly.express as px

st.subheader("Broad Sector Distribution")

sector_count = (
    sectors["broad_sector"]
    .value_counts()
    .reset_index()
)

sector_count.columns = [
    "Sector",
    "Companies"
]

fig = px.bar(
    sector_count,
    x="Sector",
    y="Companies",
    color="Companies",
    text="Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)