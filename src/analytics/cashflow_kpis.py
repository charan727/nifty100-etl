
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
        """
        Free Cash Flow = CFO + CFI
        """
        return (operating_activity or 0) + (investing_activity or 0)

    @staticmethod
    def cfo_quality_score(cfo, pat):
        """
        CFO Quality Score
        """

        cfo = 0 if cfo is None else cfo

        if pat is None or pat == 0:
            return 0.0, "Insufficient Data"

        ratio = abs(cfo / pat)

        if ratio > 1:
            return round(ratio, 2), "High Quality"

        elif ratio >= 0.5:
            return round(ratio, 2), "Moderate"

        return round(ratio, 2), "Accrual Risk"

    @staticmethod
    def capex_intensity(investing_activity, sales):
        """
        CapEx Intensity %
        """
        if sales is None or sales == 0:
            return None, None

        pct = abs(investing_activity or 0) / sales * 100

        if pct < 3:
            label = "Asset Light"
        elif pct <= 8:
            label = "Moderate"
        else:
            label = "Capital Intensive"

        return round(pct, 2), label

    @staticmethod
    def fcf_conversion(fcf, operating_profit):
        """
        FCF Conversion %
        """
        if operating_profit is None or operating_profit == 0:
            return None
        return round((fcf / operating_profit) * 100, 2)

    @staticmethod
    def sign(value):
        """
        Returns +, -, or 0
        """
        if value is None:
            return "0"

        if value > 0:
            return "+"

        if value < 0:
            return "-"

        return "0"

    @staticmethod
    def capital_allocation_pattern(cfo, cfi, cff, cfo_quality=None):
        """
        Returns:
            cfo_sign,
            cfi_sign,
            cff_sign,
            pattern_label
        """

        cfo_sign = CashflowKPIs.sign(cfo)
        cfi_sign = CashflowKPIs.sign(cfi)
        cff_sign = CashflowKPIs.sign(cff)

        pattern = "Unknown"

        if cfo_sign == "+" and cfi_sign == "-" and cff_sign == "-":
            pattern = "Reinvestor"

            if cfo_quality is not None:
                score = cfo_quality[0] if isinstance(cfo_quality, tuple) else cfo_quality

                if score >= 1:
                    pattern = "Shareholder Returns"

        elif cfo_sign == "+" and cfi_sign == "+" and cff_sign == "-":
            pattern = "Liquidating Assets"

        elif cfo_sign == "-" and cfi_sign == "+" and cff_sign == "+":
            pattern = "Distress Signal"

        elif cfo_sign == "-" and cfi_sign == "-" and cff_sign == "+":
            pattern = "Growth Funded by Debt"

        elif cfo_sign == "+" and cfi_sign == "+" and cff_sign == "+":
            pattern = "Cash Accumulator"

        elif cfo_sign == "-" and cfi_sign == "-" and cff_sign == "-":
            pattern = "Pre-Revenue"

        elif cfo_sign == "+" and cfi_sign == "-" and cff_sign == "+":
            pattern = "Mixed"

        return (
            cfo_sign,
            cfi_sign,
            cff_sign,
            pattern
        )

    
        
    @staticmethod
    def export_capital_allocation(
        df,
        output_path="output/capital_allocation.csv"
    ):
        """
        Export Capital Allocation CSV
        """

        required_columns = [
            "company_id",
            "year",
            "cfo_sign",
            "cfi_sign",
            "cff_sign",
            "pattern_label"
        ]

        export_df = df[required_columns].copy()

        export_df.to_csv(
            output_path,
            index=False
        )

        logging.info(
            f"Capital allocation CSV exported successfully: {output_path}"
        )
                