import sqlite3
import pandas as pd

from src.config import DATABASE_PATH
from src.analytics.ratios import FinancialRatios
from src.analytics.cashflow_kpis import CashflowKPIs


def populate_financial_ratios():

    conn = sqlite3.connect(DATABASE_PATH)

    # -----------------------------
    # Read Tables
    # -----------------------------

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    # -----------------------------
    # Remove duplicate ids
    # -----------------------------

    pnl = pnl.drop(columns=["id"], errors="ignore")
    bs = bs.drop(columns=["id"], errors="ignore")
    cf = cf.drop(columns=["id"], errors="ignore")
    sectors = sectors.drop(columns=["id"], errors="ignore")

    companies = companies.rename(
        columns={"id": "company_master_id"}
    )

    # -----------------------------
    # Merge
    # -----------------------------

    df = pnl.merge(
        bs,
        on=["company_id", "year"],
        how="left"
    )

    df = df.merge(
        cf,
        on=["company_id", "year"],
        how="left"
    )

    df = df.merge(
        companies,
        left_on="company_id",
        right_on="company_master_id",
        how="left"
    )

    df = df.merge(
        sectors[["company_id", "broad_sector"]],
        on="company_id",
        how="left"
    )

    results = []
    results = []

    for _, row in df.iterrows():

        # -----------------------------
        # Profitability Ratios
        # -----------------------------

        # -----------------------------
        # Profitability Ratios
        # -----------------------------

        net_profit_margin = FinancialRatios.net_profit_margin(
            row["net_profit"],
            row["sales"]
        )

        operating_profit_margin = FinancialRatios.operating_profit_margin(
            row["operating_profit"],
            row["sales"]
        )

        FinancialRatios.validate_opm(
            operating_profit_margin,
            row["opm_percentage"]
        )

        roe = FinancialRatios.return_on_equity(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"]
        )

        roce = FinancialRatios.return_on_capital_employed(
            row["operating_profit"],
            row["other_income"],
            row["interest"],
            row["equity_capital"],
            row["reserves"],
            row["borrowings"]
        )

        roa = FinancialRatios.return_on_assets(
            row["net_profit"],
            row["total_assets"]
        )

        # -----------------------------
        # Leverage
        # -----------------------------

        debt_equity = FinancialRatios.debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        )

        high_leverage = FinancialRatios.high_leverage_flag(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"],
            row["broad_sector"] if pd.notna(row["broad_sector"]) else ""
        )

        interest_coverage = FinancialRatios.interest_coverage(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        )

        interest_label = FinancialRatios.interest_coverage_label(
            row["interest"]
        )

        asset_turnover = FinancialRatios.asset_turnover(
            row["sales"],
            row["total_assets"]
        )

        net_debt = FinancialRatios.net_debt(
            row["borrowings"],
            row["investments"]
        )

        # -----------------------------
        # Cash Flow KPIs
        # -----------------------------

        free_cash_flow = CashflowKPIs.free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        )

        capex_pct, _ = CashflowKPIs.capex_intensity(
            row["investing_activity"],
            row["sales"]
        )

        cfo_quality = CashflowKPIs.cfo_quality_score(
            row["operating_activity"],
            row["net_profit"]
        )

        fcf_conversion = CashflowKPIs.fcf_conversion(
            free_cash_flow,
            row["operating_profit"]
        )

        if cfo_quality is None:
            cfo_score = None
            cfo_label = None
        else:
            cfo_score = round(cfo_quality[0], 2)
            cfo_label = cfo_quality[1]

        results.append({

            "company_id": row["company_id"],
            "year": row["year"],

            "net_profit_margin_pct": net_profit_margin,
            "operating_profit_margin_pct": operating_profit_margin,
            "return_on_equity_pct": roe,
            "return_on_capital_employed_pct": roce,
            "return_on_assets_pct": roa,

            "debt_to_equity": debt_equity,
            "interest_coverage": interest_coverage,
            "interest_coverage_label": interest_label,
            "high_leverage_flag": 1 if high_leverage else 0,

            "asset_turnover": asset_turnover,
            "net_debt_cr": net_debt,

            "free_cash_flow_cr": free_cash_flow,
            "capex_cr": capex_pct,
            "cash_from_operations_cr": row["operating_activity"],
            "fcf_conversion_pct": fcf_conversion,

            "cfo_quality_score": cfo_score,
            "cfo_quality_label": cfo_label,

            "earnings_per_share": row["eps"],

            "book_value_per_share":
                FinancialRatios.book_value_per_share(
                    row["book_value"],
                    row["face_value"]
                ),

            "dividend_payout_ratio_pct":
                FinancialRatios.dividend_payout_ratio(
                    row["dividend_payout"]
                ),

            "total_debt_cr": row["borrowings"],

            "revenue_cagr_3yr": None,
            "revenue_cagr_5yr": None,
            "revenue_cagr_10yr": None,

            "pat_cagr_3yr": None,
            "pat_cagr_5yr": None,
            "pat_cagr_10yr": None,

            "eps_cagr_3yr": None,
            "eps_cagr_5yr": None,
            "eps_cagr_10yr": None,

            "revenue_cagr_flag": None,
            "pat_cagr_flag": None,
            "eps_cagr_flag": None,

            "composite_quality_score": None

        })
            # -----------------------------
    # Load into SQLite
    # -----------------------------

    final_df = pd.DataFrame(results)

    if final_df.empty:
        print("No financial ratios generated.")
        conn.close()
        return

    conn.execute("DELETE FROM financial_ratios")

    final_df.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    print("=" * 60)
    print("Financial Ratios Generated Successfully")
    print(f"Rows Inserted : {len(final_df)}")
    print("=" * 60)

    conn.close()