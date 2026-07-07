import pandas as pd

import pandas as pd


def normalize_year(df):

    if "year" in df.columns:

        df["year"] = (
            df["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
        )

        df["year"] = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

        df = df.dropna(subset=["year"])

        df["year"] = df["year"].astype(int)

    return df


def normalize_ticker(df):
    """
    Convert id/company_id/ticker column to uppercase.
    """
    for col in ["id", "company_id", "ticker"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    return df