import streamlit as st

from dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_company_profile
)

st.set_page_config(
    page_title="Reports Center",
    layout="wide"
)

st.title("Reports Center")

# ---------------------------------------
# Load Data
# ---------------------------------------

companies = get_companies()
ratios = get_ratios()

if companies.empty or ratios.empty:
    st.error("Required data not found.")
    st.stop()

company_list = sorted(
    companies["id"]
    .dropna()
    .unique()
)

ticker = st.selectbox(
    "Select Company",
    company_list
)

profile = get_company_profile(ticker)
company_ratios = (
    get_ratios(ticker)
    .sort_values("year")
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="last"
    )
)

# ---------------------------------------
# Company Profile
# ---------------------------------------

st.divider()

st.subheader("Company Profile")

if not profile.empty:

    company = profile.iloc[0]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Company",
        company["company_name"]
    )

    c2.metric(
        "Broad Sector",
        company["broad_sector"]
    )

    c3.metric(
        "Sub Sector",
        company["sub_sector"]
    )

# ---------------------------------------
# Financial Ratios
# ---------------------------------------

st.divider()

st.subheader("Financial Ratios")

st.dataframe(
    company_ratios,
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------
# Download Report
# ---------------------------------------

csv = company_ratios.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Company Report",
    data=csv,
    file_name=f"{ticker}_financial_report.csv",
    mime="text/csv"
)

st.success("Reports Center Loaded Successfully")