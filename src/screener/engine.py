import sqlite3
import yaml
import pandas as pd
from pathlib import Path

from src.config import DATABASE_PATH


class ScreenerEngine:

    def __init__(self):
        config_path = (
            Path(__file__).resolve().parents[2]
            / "config"
            / "screener_config.yaml"
        )

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.conn = sqlite3.connect(DATABASE_PATH)

    # -----------------------------------------
    # Load financial ratios
    # -----------------------------------------

    def load_data(self):

        query = """
        SELECT
            fr.*,
            s.broad_sector,
            c.company_name
        FROM financial_ratios fr
        LEFT JOIN sectors s
            ON fr.company_id = s.company_id
        LEFT JOIN companies c
            ON fr.company_id = c.id
        """
        df = pd.read_sql(query, self.conn)
    
        

        return df
        
    # -----------------------------------------
    # Apply filters
    # -----------------------------------------

    def apply_filters(self, preset):

        df = self.load_data()
  

        rules = self.config[preset]

        for metric, value in rules.items():

            # -------------------------------
            # ROE
            # -------------------------------

            if metric == "roe_min":

                df = df[
                    df["return_on_equity_pct"] >= value
                ]

            # -------------------------------
            # Debt to Equity
            # -------------------------------

            elif metric == "debt_to_equity_max":

                financials = df[
                    df["broad_sector"] == "Financials"
                ]

                others = df[
                    (df["broad_sector"] != "Financials")
                    &
                    (df["debt_to_equity"] <= value)
                ]

                df = pd.concat(
                    [financials, others],
                    ignore_index=True
                )

            # -------------------------------
            # Free Cash Flow
            # -------------------------------

            elif metric == "free_cash_flow_min":

                df = df[
                    df["free_cash_flow_cr"] >= value
                ]

            # -------------------------------
            # Revenue CAGR
            # -------------------------------

            elif metric == "revenue_cagr_5yr_min":

                df = df[
                    df["revenue_cagr_5yr"] >= value
                ]

            # -------------------------------
            # PAT CAGR
            # -------------------------------

            elif metric == "pat_cagr_5yr_min":

                df = df[
                    df["pat_cagr_5yr"] >= value
                ]

            # -------------------------------
            # Sales
            # -------------------------------

            elif metric == "sales_min":

                if "sales" in df.columns:

                    df = df[
                        df["sales"] >= value
                    ]

                    # -------------------------------
            # PE Ratio
            # -------------------------------
            elif metric == "pe_max":

                if "pe_ratio" in df.columns:
                    df = df[df["pe_ratio"] <= value]

            # -------------------------------
            # PB Ratio
            # -------------------------------
            elif metric == "pb_max":

                if "pb_ratio" in df.columns:
                    df = df[df["pb_ratio"] <= value]

            # -------------------------------
            # Dividend Yield
            # -------------------------------
            elif metric == "dividend_yield_min":

                if "dividend_yield_pct" in df.columns:
                    df = df[df["dividend_yield_pct"] >= value]

            # -------------------------------
            # Dividend Payout
            # -------------------------------
            elif metric == "dividend_payout_ratio_max":

                if "dividend_payout_ratio_pct" in df.columns:
                    df = df[
                        df["dividend_payout_ratio_pct"] <= value
                    ]

            # -------------------------------
            # Revenue CAGR 3 Year
            # -------------------------------
            elif metric == "revenue_cagr_3yr_min":

                if "revenue_cagr_3yr" in df.columns:
                    df = df[
                        df["revenue_cagr_3yr"] >= value
                    ]
        # -------------------------------
        # Debt Free = Infinity
        # -------------------------------

        if "interest_coverage_label" in df.columns:

            df.loc[
                df["interest_coverage_label"] == "Debt Free",
                "interest_coverage"
            ] = float("inf")

        # -------------------------------
        # Sort
        # -------------------------------

        if "composite_quality_score" in df.columns:

            df = df.sort_values(
                "composite_quality_score",
                ascending=False
            )

        return df.reset_index(drop=True)

