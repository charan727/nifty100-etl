import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_sectors
)

st.set_page_config(
    page_title="Sector Analysis",
    layout="wide"
)

st.title("Sector Analysis")

# ---------------------------------------
# Load Data
# ---------------------------------------

sectors = get_sectors()

if sectors.empty:
    st.error("Sector data not found.")
    st.stop()

# ---------------------------------------
# Summary
# ---------------------------------------

st.subheader("Sector Summary")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    sectors["company_id"].nunique()
)

c2.metric(
    "Broad Sectors",
    sectors["broad_sector"].nunique()
)

c3.metric(
    "Sub Sectors",
    sectors["sub_sector"].nunique()
)

st.divider()

# ---------------------------------------
# Sector Distribution
# ---------------------------------------

st.subheader("Broad Sector Distribution")

sector_df = (
    sectors["broad_sector"]
    .value_counts()
    .reset_index()
)

sector_df.columns = [
    "Sector",
    "Companies"
]

fig = px.bar(
    sector_df,
    x="Sector",
    y="Companies",
    color="Companies",
    text="Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# Pie Chart
# ---------------------------------------

st.subheader("Sector Share")

fig = px.pie(
    sector_df,
    names="Sector",
    values="Companies",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# Sector Master
# ---------------------------------------

st.subheader("Sector Master")

display_cols = [
    c for c in [
        "company_id",
        "broad_sector",
        "sub_sector"
    ]
    if c in sectors.columns
]

st.dataframe(
    sectors[display_cols]
    .sort_values(
        ["broad_sector", "sub_sector"]
    ),
    use_container_width=True,
    hide_index=True
)

st.success("Sector Analysis Loaded Successfully")