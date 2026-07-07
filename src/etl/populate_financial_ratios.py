import sqlite3
import pandas as pd

from src.config import DATABASE_PATH
from src.analytics.ratios import FinancialRatios
from src.analytics.cashflow_kpis import CashflowKPIs
from src.analytics.cagr import CAGRCalculator


def populate_financial_ratios():

    conn = sqlite3.connect(DATABASE_PATH)

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

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    results = []
    capital_results = []
    edge_cases = []

    ratios = FinancialRatios()
    cagr = CAGRCalculator()
    print("Companies:", companies.columns.tolist())
    print("PnL:", pnl.columns.tolist())
    print("Balance:", balancesheet.columns.tolist())
    print("Cashflow:", cashflow.columns.tolist())
    merged_df = (
        pnl.merge(
        balancesheet,
        on=["company_id", "year"],
        how="inner",
        suffixes=("", "_bs")
    )
    .merge(
        cashflow,
        on=["company_id", "year"],
        how="inner",
        suffixes=("", "_cf")
    )
    .merge(
    companies[
        [
            "id",
            "company_name",
            "roe_percentage",
            "roce_percentage"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)
)
    print("Merged Successfully")

    print(merged_df.head())

    print(f"Total merged rows : {len(merged_df)}")

    for _, row in merged_df.iterrows():

        company_id = row["company_id"]
        year = row["year"]

        sales = row.get("sales", 0)
        operating_profit = row.get("operating_profit", 0)
        net_profit = row.get("net_profit", 0)

        total_assets = row.get("total_assets", 0)
        total_liabilities = row.get("total_liabilities", 0)
        equity = row.get("equity", 0)

        operating_activity = row.get("operating_activity", 0)
        investing_activity = row.get("investing_activity", 0)
        financing_activity = row.get("financing_activity", 0)

        interest = row.get("interest", 0)
        depreciation = row.get("depreciation", 0)
        eps = row.get("eps", 0)
        dividend = row.get("dividend_payout", 0)

        try:
            # -----------------------------------
            # Profitability Ratios
            # -----------------------------------

            net_profit_margin = ratios.net_profit_margin(
                net_profit,
                sales
            )

            operating_profit_margin = ratios.operating_profit_margin(
                operating_profit,
                sales
            )

            roe = ratios.return_on_equity(
                net_profit,
                row.get("equity_capital", 0),
                row.get("reserves", 0)
            )

            roce = ratios.return_on_capital_employed(
                operating_profit,
                row.get("other_income", 0),
                interest,
                row.get("equity_capital", 0),
                row.get("reserves", 0),
                row.get("borrowings", 0)
            )

            roa = ratios.return_on_assets(
                net_profit,
                total_assets
            )

            # -----------------------------------
            # ROE Cross Check
            # -----------------------------------

            source_roe = row.get("roe_percentage")

            if pd.notna(source_roe) and roe is not None:
                if abs(source_roe - roe) > 5:
                    edge_cases.append(
                        f"{company_id} | {year} | ROE | Source={source_roe:.2f} | Calculated={roe:.2f} | Category=Formula Difference"
                    )

            # -----------------------------------
            # ROCE Cross Check
            # -----------------------------------

            source_roce = row.get("roce_percentage")

            if pd.notna(source_roce) and roce is not None:
                if abs(source_roce - roce) > 5:
                    edge_cases.append(
                        f"{company_id} | {year} | ROCE | Source={source_roce:.2f} | Calculated={roce:.2f} | Category=Formula Difference"
                    )

            # -----------------------------------
            # Leverage Ratios
            # -----------------------------------

            debt_equity = ratios.debt_to_equity(
                row.get("borrowings", 0),
                row.get("equity_capital", 0),
                row.get("reserves", 0)
            )

            interest_coverage = ratios.interest_coverage(
                operating_profit,
                row.get("other_income", 0),
                interest
            )

            interest_label = ratios.interest_coverage_label(
                interest
            )

            asset_turnover = ratios.asset_turnover(
                sales,
                total_assets
            )

            net_debt = ratios.net_debt(
                row.get("borrowings", 0),
                row.get("investments", 0)
            )

            high_leverage = ratios.high_leverage_flag(
                row.get("borrowings", 0),
                row.get("equity_capital", 0),
                row.get("reserves", 0),
                row.get("broad_sector", "")
            )
            # Financial sector carve-out
            if str(row.get("broad_sector", "")).strip().lower() == "financials":
                high_leverage = False
            # -----------------------------------
            # Cash Flow KPIs
            # -----------------------------------

            free_cash_flow = CashflowKPIs.free_cash_flow(
                operating_activity,
                investing_activity
            )

            capex_pct, capex_label = CashflowKPIs.capex_intensity(
                investing_activity,
                sales
            )

            cfo_quality = CashflowKPIs.cfo_quality_score(
                operating_activity,
                net_profit
            )

            fcf_conversion = CashflowKPIs.fcf_conversion(
                free_cash_flow,
                operating_profit
            )

            if cfo_quality is None:
                cfo_score = None
                cfo_label = None
            else:
                cfo_score = round(cfo_quality[0], 2)
                cfo_label = cfo_quality[1]

            # -----------------------------------
            # Capital Allocation Pattern
            # -----------------------------------

            cfo_sign, cfi_sign, cff_sign, pattern_label = (
                CashflowKPIs.capital_allocation_pattern(
                    operating_activity,
                    investing_activity,
                    financing_activity,
                    cfo_score
                )
            )

            # -----------------------------------
            # CAGR
            # -----------------------------------

            revenue_cagr_5yr, revenue_flag = (
                cagr.revenue_cagr_5yr(
                    sales,
                    sales
                )
            )

            pat_cagr_5yr, pat_flag = (
                cagr.pat_cagr_5yr(
                    net_profit,
                    net_profit
                )
            )

            eps_cagr_5yr, eps_flag = (
                cagr.eps_cagr_5yr(
                    eps,
                    eps
                )
            )

            # -----------------------------------
            # Composite Quality Score
            # -----------------------------------

            score = 0

            if roe is not None and roe > 15:
                score += 25

            if debt_equity is not None and debt_equity < 1:
                score += 25

            if interest_coverage is not None and interest_coverage > 3:
                score += 25

            if free_cash_flow is not None and free_cash_flow > 0:
                score += 25
           
           
                        # -----------------------------------
            # Store Results
            # -----------------------------------

            results.append({

                "company_id": company_id,
                "year": year,

                # Profitability
                "net_profit_margin_pct": net_profit_margin,
                "operating_profit_margin_pct": operating_profit_margin,
                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce,
                "return_on_assets_pct": roa,

                # Leverage
                "debt_to_equity": debt_equity,
                "interest_coverage": interest_coverage,
                "interest_coverage_label": interest_label,
                "high_leverage_flag": int(high_leverage),
                "asset_turnover": asset_turnover,
                "net_debt_cr": net_debt,

                # Cash Flow
                "free_cash_flow_cr": free_cash_flow,
                "capex_cr": capex_pct,
                "cash_from_operations_cr": operating_activity,
                "fcf_conversion_pct": fcf_conversion,
                "cfo_quality_score": cfo_score,
                "cfo_quality_label": cfo_label,

                # Shareholder Metrics
                "earnings_per_share": eps,
                "book_value_per_share": ratios.book_value_per_share(
                    row.get("book_value", 0),
                    row.get("face_value", 0)
                ),
                "dividend_payout_ratio_pct": ratios.dividend_payout_ratio(dividend),
                "total_debt_cr": row.get("borrowings", 0),

                # CAGR
                "revenue_cagr_3yr": None,
                "revenue_cagr_5yr": revenue_cagr_5yr,
                "revenue_cagr_10yr": None,

                "pat_cagr_3yr": None,
                "pat_cagr_5yr": pat_cagr_5yr,
                "pat_cagr_10yr": None,

                "eps_cagr_3yr": None,
                "eps_cagr_5yr": eps_cagr_5yr,
                "eps_cagr_10yr": None,

                "revenue_cagr_flag": revenue_flag,
                "pat_cagr_flag": pat_flag,
                "eps_cagr_flag": eps_flag,

                "composite_quality_score": score

            })
            capital_results.append({
                "company_id": company_id,
                "year": year,
                "cfo_sign": cfo_sign,
                "cfi_sign": cfi_sign,
                "cff_sign": cff_sign,
                "pattern_label": pattern_label
            })

        except Exception as e:
            print(f"Error processing Company={company_id}, Year={year}: {e}")
            continue

    # -----------------------------------
    # Convert Results to DataFrame
    # -----------------------------------

    final_df = pd.DataFrame(results)
    capital_df = pd.DataFrame(capital_results)

    # -----------------------------------
    # Check Empty
    # -----------------------------------

    if final_df.empty:
        print("No financial ratios generated.")
        conn.close()
        return

    capital_df.to_csv(
        "output/capital_allocation.csv",
        index=False
    )

    print("capital_allocation.csv generated successfully")

    # -----------------------------------
    # Edge Case Log
    # -----------------------------------

    with open("output/ratio_edge_cases.log", "w", encoding="utf-8") as f:

        if edge_cases:

            for item in edge_cases:
                f.write(item + "\n")

        else:
            f.write("No edge cases found.\n")

        print("ratio_edge_cases.log generated successfully")

    # -----------------------------------
    # Load into SQLite
    # -----------------------------------

    try:
        final_df.to_sql(
            "financial_ratios",
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()

        print("=" * 60)
        print("Financial Ratios Generated Successfully")
        print(f"Rows Inserted : {len(final_df)}")
        print("=" * 60)

    except Exception as e:
        import traceback

        print("\n========== RATIO ENGINE FAILED ==========")
        print(type(e))
        print(e)
        traceback.print_exc()

        raise

    finally:

        conn.close()


if __name__ == "__main__":
    populate_financial_ratios()