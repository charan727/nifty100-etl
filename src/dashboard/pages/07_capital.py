import streamlit as st
import plotly.express as px

from dashboard.utils.db import get_sectors

st.set_page_config(
    page_title="Capital Analysis",
    layout="wide"
)

st.title("Capital Analysis")

# ---------------------------------------
# Load Data
# ---------------------------------------

sectors = get_sectors()

if sectors.empty:
    st.error("No sector data available.")
    st.stop()

# ---------------------------------------
# Market Cap Filter
# ---------------------------------------

market_caps = sorted(
    sectors["market_cap_category"]
    .dropna()
    .unique()
)

cap_filter = st.selectbox(
    "Select Market Cap",
    ["All"] + market_caps
)

filtered = sectors.copy()

if cap_filter != "All":
    filtered = filtered[
        filtered["market_cap_category"] == cap_filter
    ]

# ---------------------------------------
# Summary
# ---------------------------------------

c1, c2, c3 = st.columns(3)

c1.metric(
    "Companies",
    len(filtered)
)

c2.metric(
    "Broad Sectors",
    filtered["broad_sector"].nunique()
)

c3.metric(
    "Average Index Weight",
    f"{filtered['index_weight_pct'].mean():.2f}%"
)

st.divider()

# ---------------------------------------
# Market Cap Distribution
# ---------------------------------------

cap_df = (
    filtered["market_cap_category"]
    .value_counts()
    .reset_index()
)

cap_df.columns = [
    "Market Cap",
    "Companies"
]

fig = px.pie(
    cap_df,
    names="Market Cap",
    values="Companies",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ---------------------------------------
# Sector Distribution
# ---------------------------------------

sector_df = (
    filtered["broad_sector"]
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
# Capital Master
# ---------------------------------------

display_cols = [
    c for c in [
        "company_id",
        "market_cap_category",
        "index_weight_pct",
        "broad_sector",
        "sub_sector"
    ]
    if c in filtered.columns
]

st.dataframe(
    filtered[display_cols]
    .sort_values(
        ["market_cap_category", "company_id"]
    ),
    use_container_width=True,
    hide_index=True
)

st.success("Capital Analysis Loaded Successfully")