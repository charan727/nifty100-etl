import pandas as pd


def normalize_year(df):
    """
    Convert year column to integer.
    """
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce").fillna(0).astype(int)

    return df


def normalize_ticker(df):
    """
    Convert id/company_id/ticker column to uppercase.
    """
    for col in ["id", "company_id", "ticker"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    return df