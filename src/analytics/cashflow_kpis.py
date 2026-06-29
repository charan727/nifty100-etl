"""
Cash Flow KPI Engine
Sprint 2 - Day 11
"""

import logging
import pandas as pd

logging.basicConfig(
    filename="output/ratio_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class CashflowKPIs:

    @staticmethod
    def free_cash_flow(operating_activity, investing_activity):
        return (operating_activity or 0) + (investing_activity or 0)

    @staticmethod
    def cfo_quality_score(cfo, pat):
        if pat is None or pat == 0:
            return None
        ratio = cfo / pat
        if ratio > 1:
            return ratio, "High Quality"
        elif ratio >= 0.5:
            return ratio, "Moderate"
        return ratio, "Accrual Risk"

    @staticmethod
    def capex_intensity(investing_activity, sales):
        if sales is None or sales == 0:
            return None, None
        pct = abs(investing_activity or 0) / sales * 100
        if pct < 3:
            label="Asset Light"
        elif pct <= 8:
            label="Moderate"
        else:
            label="Capital Intensive"
        return round(pct,2), label

    @staticmethod
    def fcf_conversion(fcf, operating_profit):
        if operating_profit is None or operating_profit == 0:
            return None
        return round((fcf/operating_profit)*100,2)

    @staticmethod
    def capital_allocation_pattern(cfo,cfi,cff,cfo_pat_ratio=None):
        s1="+" if (cfo or 0)>=0 else "-"
        s2="+" if (cfi or 0)>=0 else "-"
        s3="+" if (cff or 0)>=0 else "-"
        pattern=f"{s1},{s2},{s3}"
        mapping={
            "+,-,-":"Reinvestor",
            "+,+,-":"Liquidating Assets",
            "-,+,+":"Distress Signal",
            "-,-,+":"Growth Funded by Debt",
            "+,+,+":"Cash Accumulator",
            "-,-,-":"Pre-Revenue",
            "+,-,+":"Mixed",
        }
        label=mapping.get(pattern,"Other")
        if pattern=="+,-,-" and cfo_pat_ratio is not None and cfo_pat_ratio>1:
            label="Shareholder Returns"
        return pattern,label

    @staticmethod
    def export_capital_allocation(df, output_path="output/capital_allocation.csv"):
        cols=["company_id","year","cfo_sign","cfi_sign","cff_sign","pattern_label"]
        df[cols].to_csv(output_path,index=False)
        logging.info("capital_allocation.csv generated")
