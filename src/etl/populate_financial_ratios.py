import sqlite3
import pandas as pd

from pathlib import Path

DATABASE_PATH = r"C:\Users\chara\OneDrive\Desktop\nifty100-etl\db\nifty100.db"

print("DATABASE =", DATABASE_PATH)
from analytics.ratios import FinancialRatios
from analytics.cashflow_kpis import CashflowKPIs
from analytics.cagr import CAGRCalculator


# ==========================================================
# Helper Functions
# ==========================================================

def safe_value(value, default=0):
    if pd.isna(value):
        return default
    try:
        return float(value)
    except Exception:
        return default


def get_company_history(df, company_id):
    return (
        df[df["company_id"] == company_id]
        .sort_values("year")
        .reset_index(drop=True)
    )


def lookup_year_value(history, current_year, years_back, column):

    target_year = current_year - years_back

    row = history[history["year"] == target_year]

    if row.empty:
        return None

    value = row.iloc[0][column]

    if pd.isna(value):
        return None

    return value


def calculate_cagr(calculator,
                   start_value,
                   end_value,
                   years,
                   metric):

    if (
        start_value is None
        or end_value is None
        or start_value == 0
    ):
        return None, "INSUFFICIENT"

    if metric == "revenue":

        if years == 3:
            return calculator.revenue_cagr_3yr(
                start_value,
                end_value
            )

        if years == 5:
            return calculator.revenue_cagr_5yr(
                start_value,
                end_value
            )

        if years == 10:
            return calculator.revenue_cagr_10yr(
                start_value,
                end_value
            )

    if metric == "pat":

        if years == 3:
            return calculator.pat_cagr_3yr(
                start_value,
                end_value
            )

        if years == 5:
            return calculator.pat_cagr_5yr(
                start_value,
                end_value
            )

        if years == 10:
            return calculator.pat_cagr_10yr(
                start_value,
                end_value
            )

    if metric == "eps":

        if years == 3:
            return calculator.eps_cagr_3yr(
                start_value,
                end_value
            )

        if years == 5:
            return calculator.eps_cagr_5yr(
                start_value,
                end_value
            )

        if years == 10:
            return calculator.eps_cagr_10yr(
                start_value,
                end_value
            )

    return None, "INSUFFICIENT"


# ==========================================================
# Main Function
# ==========================================================

def populate_financial_ratios():

    conn = sqlite3.connect(DATABASE_PATH)

    ratios = FinancialRatios()
    cashflow = CashflowKPIs()
    cagr = CAGRCalculator()

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balancesheet = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflows = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
    )

    # Read companies once
    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    print(companies.columns.tolist())


    merged_df = (
        pnl
        .merge(
            balancesheet,
            on=["company_id", "year"],
            how="inner"
        )
        .merge(
            cashflows,
            on=["company_id", "year"],
            how="inner"
        )
        .merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left",
    suffixes=("", "_company")
)
    )

    merged_df = merged_df.sort_values(
        ["company_id", "year"]
    )

    results = []

    print("=" * 60)
    print("Financial Ratio Engine Started")
    print("=" * 60)

    for _, row in merged_df.iterrows():
        print("Processing:", row["company_id"], row["year"])

        company_id = row["company_id"]
        current_year = row["year"]

        history = get_company_history(
            merged_df,
            company_id
        )

        sales = safe_value(row["sales"])
        operating_profit = safe_value(row["operating_profit"])
        other_income = safe_value(row["other_income"])
        interest = safe_value(row["interest"])
        net_profit = safe_value(row["net_profit"])
        eps = safe_value(row["eps"])
        dividend = safe_value(row["dividend_payout"])

        equity = safe_value(row["equity_capital"])
        reserves = safe_value(row["reserves"])
        borrowings = safe_value(row["borrowings"])
        investments = safe_value(row["investments"])
        total_assets = safe_value(row["total_assets"])

        operating_activity = safe_value(
            row["operating_activity"]
        )

        investing_activity = safe_value(
            row["investing_activity"]
        )

        financing_activity = safe_value(
            row["financing_activity"]
        )

        revenue3 = lookup_year_value(
            history,
            current_year,
            3,
            "sales"
        )

        revenue5 = lookup_year_value(
            history,
            current_year,
            5,
            "sales"
        )

        revenue10 = lookup_year_value(
            history,
            current_year,
            10,
            "sales"
        )

        pat3 = lookup_year_value(
            history,
            current_year,
            3,
            "net_profit"
        )

        pat5 = lookup_year_value(
            history,
            current_year,
            5,
            "net_profit"
        )

        pat10 = lookup_year_value(
            history,
            current_year,
            10,
            "net_profit"
        )

        eps3 = lookup_year_value(
            history,
            current_year,
            3,
            "eps"
        )

        eps5 = lookup_year_value(
            history,
            current_year,
            5,
            "eps"
        )

        eps10 = lookup_year_value(
            history,
            current_year,
            10,
            "eps"
        )

        revenue_cagr_3yr, revenue_cagr_3yr_flag = calculate_cagr(
            cagr, revenue3, sales, 3, "revenue"
        )

        revenue_cagr_5yr, revenue_cagr_5yr_flag = calculate_cagr(
            cagr, revenue5, sales, 5, "revenue"
        )

        revenue_cagr_10yr, revenue_cagr_10yr_flag = calculate_cagr(
            cagr, revenue10, sales, 10, "revenue"
        )

        pat_cagr_3yr, pat_cagr_3yr_flag = calculate_cagr(
            cagr, pat3, net_profit, 3, "pat"
        )

        pat_cagr_5yr, pat_cagr_5yr_flag = calculate_cagr(
            cagr, pat5, net_profit, 5, "pat"
        )

        pat_cagr_10yr, pat_cagr_10yr_flag = calculate_cagr(
            cagr, pat10, net_profit, 10, "pat"
        )

        eps_cagr_3yr, eps_cagr_3yr_flag = calculate_cagr(
            cagr, eps3, eps, 3, "eps"
        )

        eps_cagr_5yr, eps_cagr_5yr_flag = calculate_cagr(
            cagr, eps5, eps, 5, "eps"
        )

        eps_cagr_10yr, eps_cagr_10yr_flag = calculate_cagr(
            cagr, eps10, eps, 10, "eps"
        )

        net_profit_margin = ratios.net_profit_margin(
            net_profit,
            sales,
        )

        operating_profit_margin = ratios.operating_profit_margin(
            operating_profit,
            sales,
        )

        roe = ratios.return_on_equity(
            net_profit,
            equity,
            reserves,
        )

        roce = ratios.return_on_capital_employed(
            operating_profit,
            other_income,
            interest,
            equity,
            reserves,
            borrowings,
        )

        roa = ratios.return_on_assets(
            net_profit,
            total_assets,
        )

        debt_equity = ratios.debt_to_equity(
            borrowings,
            equity,
            reserves,
        )

        high_leverage = ratios.high_leverage_flag(
            borrowings,
            equity,
            reserves,
            row.get("sector"),
        )

        interest_coverage = ratios.interest_coverage(
            operating_profit,
            other_income,
            interest,
        )

        interest_label = ratios.interest_coverage_label(
            interest,
        )

        interest_warning = ratios.interest_warning(
            interest_coverage,
        )

        net_debt = ratios.net_debt(
            borrowings,
            investments,
        )

        asset_turnover = ratios.asset_turnover(
            sales,
            total_assets,
        )

        book_value = equity + reserves

        book_value_per_share = ratios.book_value_per_share(
            book_value,
            equity if equity != 0 else None,
        )

        dividend_payout_ratio = ratios.dividend_payout_ratio(
            dividend,
        )

        free_cash_flow = cashflow.free_cash_flow(
            operating_activity,
            investing_activity,
        )

        cfo_quality_score, cfo_quality_label = cashflow.cfo_quality_score(
            operating_activity,
            net_profit,
        )

        capex_intensity, capex_label = cashflow.capex_intensity(
            investing_activity,
            sales,
        )

        fcf_conversion = cashflow.fcf_conversion(
            free_cash_flow,
            operating_profit,
        )

        (
            cfo_sign,
            cfi_sign,
            cff_sign,
            pattern_label,
        ) = cashflow.capital_allocation_pattern(
            operating_activity,
            investing_activity,
            financing_activity,
            (cfo_quality_score, cfo_quality_label),
        )
                # ======================================================
        # Composite Quality Score
        # ======================================================

        quality_score = 0

        if roe is not None and roe >= 15:
            quality_score += 1

        if roce is not None and roce >= 15:
            quality_score += 1

        if debt_equity is not None and debt_equity <= 1:
            quality_score += 1

        if interest_coverage is not None and interest_coverage >= 3:
            quality_score += 1

        if free_cash_flow is not None and free_cash_flow > 0:
            quality_score += 1

        if cfo_quality_score is not None and cfo_quality_score >= 1:
            quality_score += 1

        if revenue_cagr_5yr is not None and revenue_cagr_5yr >= 10:
            quality_score += 1

        if pat_cagr_5yr is not None and pat_cagr_5yr >= 10:
            quality_score += 1

        if eps_cagr_5yr is not None and eps_cagr_5yr >= 10:
            quality_score += 1

        quality_score = round((quality_score / 9) * 100, 2)

        # ======================================================
        # Store Result
        # ======================================================

        results.append({

            "company_id": company_id,
            "year": current_year,

            "net_profit_margin": net_profit_margin,
            "operating_profit_margin": operating_profit_margin,

            "roe": roe,
            "roce": roce,
            "roa": roa,

            "debt_equity": debt_equity,
            "high_leverage": int(high_leverage),

            "interest_coverage": interest_coverage,
            "interest_label": interest_label,
            "interest_warning": int(interest_warning),

            "net_debt": net_debt,
            "asset_turnover": asset_turnover,

            "book_value_per_share": book_value_per_share,

            "dividend_payout_ratio": dividend_payout_ratio,

            "free_cash_flow": free_cash_flow,

            "cfo_quality_score": cfo_quality_score,
            "cfo_quality_label": cfo_quality_label,

            "capex_intensity": capex_intensity,
            "capex_label": capex_label,

            "fcf_conversion": fcf_conversion,

            "cfo_sign": cfo_sign,
            "cfi_sign": cfi_sign,
            "cff_sign": cff_sign,

            "pattern_label": pattern_label,

            "revenue_cagr_3yr": revenue_cagr_3yr,
            "revenue_cagr_5yr": revenue_cagr_5yr,
            "revenue_cagr_10yr": revenue_cagr_10yr,

            "pat_cagr_3yr": pat_cagr_3yr,
            "pat_cagr_5yr": pat_cagr_5yr,
            "pat_cagr_10yr": pat_cagr_10yr,

            "eps_cagr_3yr": eps_cagr_3yr,
            "eps_cagr_5yr": eps_cagr_5yr,
            "eps_cagr_10yr": eps_cagr_10yr,

            "revenue_cagr_3yr_flag": revenue_cagr_3yr_flag,
            "revenue_cagr_5yr_flag": revenue_cagr_5yr_flag,
            "revenue_cagr_10yr_flag": revenue_cagr_10yr_flag,

            "pat_cagr_3yr_flag": pat_cagr_3yr_flag,
            "pat_cagr_5yr_flag": pat_cagr_5yr_flag,
            "pat_cagr_10yr_flag": pat_cagr_10yr_flag,

            "eps_cagr_3yr_flag": eps_cagr_3yr_flag,
            "eps_cagr_5yr_flag": eps_cagr_5yr_flag,
            "eps_cagr_10yr_flag": eps_cagr_10yr_flag,

            "quality_score": quality_score

        })

    # ======================================================
    # Convert Results
    # ======================================================

    result_df = pd.DataFrame(results)
    # ------------------------------------------------------------------
    # Create Final DataFrame
    # ------------------------------------------------------------------

    required_columns = [
        "company_id",
        "year",
        "net_profit_margin",
        "operating_profit_margin",
        "roe",
        "roce",
        "roa",
        "debt_equity",
        "high_leverage",
        "interest_coverage",
        "interest_label",
        "interest_warning",
        "net_debt",
        "asset_turnover",
        "book_value_per_share",
        "dividend_payout_ratio",
        "free_cash_flow",
        "cfo_quality_score",
        "cfo_quality_label",
        "capex_intensity",
        "capex_label",
        "fcf_conversion",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label",
        "revenue_cagr_3yr",
        "revenue_cagr_5yr",
        "revenue_cagr_10yr",
        "pat_cagr_3yr",
        "pat_cagr_5yr",
        "pat_cagr_10yr",
        "eps_cagr_3yr",
        "eps_cagr_5yr",
        "eps_cagr_10yr",
        "revenue_cagr_3yr_flag",
        "revenue_cagr_5yr_flag",
        "revenue_cagr_10yr_flag",
        "pat_cagr_3yr_flag",
        "pat_cagr_5yr_flag",
        "pat_cagr_10yr_flag",
        "eps_cagr_3yr_flag",
        "eps_cagr_5yr_flag",
        "eps_cagr_10yr_flag",
        "quality_score"
    ]

    result_df = result_df[required_columns]
   
   
    print(f"Calculated Financial Ratios : {len(result_df)} records")
    return result_df


OUTPUT_FILE = "output/financial_ratios.csv"


if __name__ == "__main__":

    result_df = populate_financial_ratios()

    result_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"CSV Saved : {OUTPUT_FILE}")