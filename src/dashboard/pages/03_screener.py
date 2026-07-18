import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_ratios


st.title("Stock Screener")

# Load data
ratios = get_ratios()
st.write(ratios.columns.tolist())


if ratios.empty:
    st.error("No financial ratio data found.")
    st.stop()

st.sidebar.header("Filters")

roe_min = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    100.0,
    15.0
)

debt_max = st.sidebar.slider(
    "Maximum Debt to Equity",
    0.0,
    10.0,
    2.0
)

fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow",
    0.0,
    10000.0,
    0.0
)

revenue_cagr_min = st.sidebar.slider(
    "Minimum Revenue CAGR 5Y",
    0.0,
    100.0,
    0.0
)

pat_cagr_min = st.sidebar.slider(
    "Minimum PAT CAGR 5Y",
    0.0,
    100.0,
    0.0
)

opm_min = st.sidebar.slider(
    "Minimum Operating Profit Margin",
    0.0,
    100.0,
    0.0
)

pe_max = st.sidebar.slider(
    "Maximum P/E",
    0.0,
    200.0,
    200.0
)

pb_max = st.sidebar.slider(
    "Maximum P/B",
    0.0,
    50.0,
    50.0
)

dividend_min = st.sidebar.slider(
    "Minimum Dividend Yield",
    0.0,
    20.0,
    0.0
)

icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0,
    100.0,
    0.0
)

# Apply filters
filtered = ratios.copy()

filtered = filtered[
    (filtered["return_on_equity_pct"] >= roe_min) &
    (filtered["debt_to_equity"] <= debt_max) &
    (filtered["free_cash_flow_cr"] >= fcf_min) &
    (filtered["revenue_cagr_5yr"] >= revenue_cagr_min) &
    (filtered["pat_cagr_5yr"] >= pat_cagr_min) &
    (filtered["operating_profit_margin_pct"] >= opm_min)
]

if "pe_ratio" in filtered.columns:
    filtered = filtered[
        filtered["pe_ratio"] <= pe_max
    ]

if "price_to_book" in filtered.columns:
    filtered = filtered[
        filtered["price_to_book"] <= pb_max
    ]

if "dividend_yield_pct" in filtered.columns:
    filtered = filtered[
        filtered["dividend_yield_pct"] >= dividend_min
    ]

if "interest_coverage" in filtered.columns:
    filtered = filtered[
        filtered["interest_coverage"] >= icr_min
    ]

st.subheader("Filtered Companies")

st.write(f"Showing **{len(filtered)}** of **{len(ratios)}** records")

st.dataframe(
    filtered,
    use_container_width=True
)