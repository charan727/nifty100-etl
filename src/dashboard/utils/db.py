import sqlite3
import pandas as pd
import streamlit as st

from config import DATABASE_PATH


# -------------------------------------------------------
# Companies
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


# -------------------------------------------------------
# Financial Ratios
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(ticker=None, year=None):

    conn = sqlite3.connect(DATABASE_PATH)

    query = "SELECT * FROM financial_ratios"
    params = []

    if ticker is not None:
        query += " WHERE company_id LIKE ?"
        params.append(ticker)

        if year is not None:
            query += " AND year = ?"
            params.append(year)

    elif year is not None:
        query += " WHERE year = ?"
        params.append(year)

    df = pd.read_sql(query, conn, params=params)

    conn.close()

    
    

    return df


# -------------------------------------------------------
# Profit & Loss
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(ticker):

    conn = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# -------------------------------------------------------
# Balance Sheet
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(ticker):

    conn = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# -------------------------------------------------------
# Cash Flow
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(ticker):

    conn = sqlite3.connect(DATABASE_PATH)

    df = pd.read_sql(
        """
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        """,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# -------------------------------------------------------
# Company Profile
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_company_profile(ticker):

    conn = sqlite3.connect(DATABASE_PATH)

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,
        s.sub_sector
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    WHERE c.id = ?
    """

    df = pd.read_sql(
        query,
        conn,
        params=[ticker]
    )

    conn.close()

    return df


# -------------------------------------------------------
# Sectors
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM sectors
            """,
            conn
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df


# -------------------------------------------------------
# Peers
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_peers(group_name):

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM peer_percentiles
            WHERE peer_group_name = ?
            """,
            conn,
            params=[group_name]
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df


# -------------------------------------------------------
# Valuation
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_valuation(ticker):

    conn = sqlite3.connect(DATABASE_PATH)

    try:
        df = pd.read_sql(
            """
            SELECT *
            FROM valuation_summary
            WHERE company_id = ?
            """,
            conn,
            params=[ticker]
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()

    return df