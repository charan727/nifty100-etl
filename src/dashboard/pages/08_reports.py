import streamlit as st

from src.dashboard.utils.db import (
    get_companies,
    get_ratios,
    get_company_profile
)

st.title("Reports Center")

companies = get_companies()
ratios = get_ratios()

if companies.empty or ratios.empty:
    st.error("Required data not found.")
    st.stop()

company_list = sorted(companies["id"].unique())

ticker = st.selectbox(
    "Select Company",
    company_list
)

profile = get_company_profile(ticker)
company_ratios = get_ratios(ticker)

st.divider()

st.subheader("Company Profile")

if not profile.empty:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Company",
        profile.iloc[0]["company_name"]
    )

    c2.metric(
        "Broad Sector",
        profile.iloc[0]["broad_sector"]
    )

    c3.metric(
        "Sub Sector",
        profile.iloc[0]["sub_sector"]
    )

st.divider()

st.subheader("Financial Ratios")

st.dataframe(
    company_ratios,
    use_container_width=True
)

csv = company_ratios.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Company Report",
    csv,
    file_name=f"{ticker}_financial_report.csv",
    mime="text/csv"
)