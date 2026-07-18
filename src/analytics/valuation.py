import pandas as pd
from pathlib import Path

from src.etl.database import create_connection

OUTPUT_PATH = Path("output")
OUTPUT_PATH.mkdir(exist_ok=True)


class ValuationEngine:

    def __init__(self):
        self.conn = create_connection()

    def load_data(self):
        """
        Load required tables from SQLite
        """

        companies = pd.read_sql("""
            SELECT
                id AS company_id,
                company_name
            FROM companies
        """, self.conn)

        sectors = pd.read_sql("""
            SELECT
                company_id,
                broad_sector
            FROM sectors
        """, self.conn)

        market_cap = pd.read_sql("""
            SELECT
                company_id,
                year,
                market_cap_crore,
                enterprise_value_crore,
                pe_ratio,
                pb_ratio,
                ev_ebitda,
                dividend_yield_pct
            FROM market_cap
        """, self.conn)

        ratios = pd.read_sql("""
            SELECT
                company_id,
                year,
                free_cash_flow_cr
            FROM financial_ratios
        """, self.conn)

        return companies, sectors, market_cap, ratios

    def prepare_dataframe(self):
        companies, sectors, market_cap, ratios = self.load_data()

        # Remove duplicate company-year records
        market_cap = market_cap.drop_duplicates(
            subset=["company_id", "year"]
        )

        ratios = ratios.drop_duplicates(
            subset=["company_id", "year"]
        )

        df = (
            market_cap
            .merge(companies, on="company_id", how="left")
            .merge(sectors, on="company_id", how="left")
            .merge(ratios, on=["company_id", "year"], how="left")
        )

        return df

    def calculate_fcf_yield(self, df):
        """
        FCF Yield %
        """

        df["FCF_yield_pct"] = (
            df["free_cash_flow_cr"] /
            df["market_cap_crore"]
        ) * 100

        df["FCF_yield_pct"] = df["FCF_yield_pct"].round(2)

        return df

    def calculate_sector_median_pe(self, df):
        """
        Latest year sector PE median
        """

        latest_year = df["year"].max()

        latest_df = df[df["year"] == latest_year].copy()

        sector_pe = (
            latest_df
            .groupby("broad_sector")["pe_ratio"]
            .median()
            .reset_index()
        )

        sector_pe.rename(
            columns={
                "pe_ratio": "sector_median_pe"
            },
            inplace=True
        )

        df = df.merge(
            sector_pe,
            on="broad_sector",
            how="left"
        )

        return df

    def calculate_company_median_pe(self, df):
        """
        5-Year Median PE
        """

        median_pe = (
            df.groupby("company_id")["pe_ratio"]
            .median()
            .reset_index()
        )

        median_pe.rename(
            columns={
                "pe_ratio": "five_year_median_pe"
            },
            inplace=True
        )

        df = df.merge(
            median_pe,
            on="company_id",
            how="left"
        )

        return df

    def main():
        engine = ValuationEngine()

        df = engine.prepare_dataframe()

        df = engine.calculate_fcf_yield(df)

        df = engine.calculate_sector_median_pe(df)

        df = engine.calculate_company_median_pe(df)

        print(df.head())

    def apply_valuation_flags(self, df):
        """
        Compare company PE with sector median PE
        """

        df["PE_vs_sector_median_pct"] = (
            (df["pe_ratio"] - df["sector_median_pe"])
            / df["sector_median_pe"]
        ) * 100

        df["PE_vs_sector_median_pct"] = (
            df["PE_vs_sector_median_pct"]
            .round(2)
        )

        conditions = [
            df["pe_ratio"] > (df["sector_median_pe"] * 1.50),
            df["pe_ratio"] < (df["sector_median_pe"] * 0.70),
        ]

        choices = [
            "Overvalued",
            "Undervalued",
        ]

        df["valuation_flag"] = pd.Series(
            pd.NA,
            index=df.index,
            dtype="object"
        )

        df.loc[conditions[0], "valuation_flag"] = choices[0]
        df.loc[conditions[1], "valuation_flag"] = choices[1]
        df["valuation_flag"] = df["valuation_flag"].fillna("Fair")

        return df

    def export_reports(self, df):

        OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

        summary = df[
            [
                "company_id",
                "company_name",
                "broad_sector",
                "year",
                "market_cap_crore",
                "enterprise_value_crore",
                "pe_ratio",
                "pb_ratio",
                "ev_ebitda",
                "dividend_yield_pct",
                "free_cash_flow_cr",
                "FCF_yield_pct",
                "five_year_median_pe",
                "sector_median_pe",
                "PE_vs_sector_median_pct",
                "valuation_flag",
            ]
        ]

        summary.to_excel(
            OUTPUT_PATH / "valuation_summary.xlsx",
            index=False
        )

        flags = summary[
            summary["valuation_flag"] != "Fair"
        ]

        flags.to_csv(
            OUTPUT_PATH / "valuation_flags.csv",
            index=False
        )

        print("\nValuation reports generated successfully.")
        print(f"Rows : {len(summary)}")
        print(f"Flagged Companies : {len(flags)}")

    def run(self):

        df = self.prepare_dataframe()

        df = self.calculate_fcf_yield(df)

        df = self.calculate_sector_median_pe(df)

        df = self.calculate_company_median_pe(df)

        df = self.apply_valuation_flags(df)

        self.export_reports(df)


def main():

    engine = ValuationEngine()

    engine.run()


if __name__ == "__main__":
    main()