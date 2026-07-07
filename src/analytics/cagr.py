import logging

logging.basicConfig(
    filename="output/ratio_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class CAGRCalculator:

    NORMAL = "NORMAL"
    TURNAROUND = "TURNAROUND"
    DECLINE_TO_LOSS = "DECLINE_TO_LOSS"
    BOTH_NEGATIVE = "BOTH_NEGATIVE"
    ZERO_BASE = "ZERO_BASE"
    INSUFFICIENT = "INSUFFICIENT"     
    @staticmethod
    def calculate_cagr(start_value, end_value, years):
        """
        Returns:
            (cagr_value, flag)
        """

        try:

            if years is None or years <= 0:
                return None, CAGRCalculator.INSUFFICIENT

            if start_value is None or end_value is None:
                return None, CAGRCalculator.INSUFFICIENT

            if start_value == 0:
                return None, CAGRCalculator.ZERO_BASE

            if start_value > 0 and end_value > 0:
                cagr = (((end_value / start_value) ** (1 / years)) - 1) * 100
                return round(cagr, 2), CAGRCalculator.NORMAL

            if start_value > 0 and end_value < 0:
                return None, CAGRCalculator.DECLINE_TO_LOSS

            if start_value < 0 and end_value > 0:
                return None, CAGRCalculator.TURNAROUND

            if start_value < 0 and end_value < 0:
                return None, CAGRCalculator.BOTH_NEGATIVE

            return None, CAGRCalculator.NORMAL

        except Exception as e:
            logging.error(f"CAGR Error: {e}")
            return None, "ERROR"

    @staticmethod
    def revenue_cagr(start_sales, end_sales, years):
        return CAGRCalculator.calculate_cagr(start_sales, end_sales, years)

    @staticmethod
    def pat_cagr(start_pat, end_pat, years):
        return CAGRCalculator.calculate_cagr(start_pat, end_pat, years)

    @staticmethod
    def eps_cagr(start_eps, end_eps, years):
        return CAGRCalculator.calculate_cagr(start_eps, end_eps, years)

    @staticmethod
    def revenue_cagr_3yr(start_sales, end_sales):
        return CAGRCalculator.revenue_cagr(start_sales, end_sales, 3)

    @staticmethod
    def revenue_cagr_5yr(start_sales, end_sales):
        return CAGRCalculator.revenue_cagr(start_sales, end_sales, 5)

    @staticmethod
    def revenue_cagr_10yr(start_sales, end_sales):
        return CAGRCalculator.revenue_cagr(start_sales, end_sales, 10)

    @staticmethod
    def pat_cagr_3yr(start_pat, end_pat):
        return CAGRCalculator.pat_cagr(start_pat, end_pat, 3)

    @staticmethod
    def pat_cagr_5yr(start_pat, end_pat):
        return CAGRCalculator.pat_cagr(start_pat, end_pat, 5)

    @staticmethod
    def pat_cagr_10yr(start_pat, end_pat):
        return CAGRCalculator.pat_cagr(start_pat, end_pat, 10)

    @staticmethod
    def eps_cagr_3yr(start_eps, end_eps):
        return CAGRCalculator.eps_cagr(start_eps, end_eps, 3)

    @staticmethod
    def eps_cagr_5yr(start_eps, end_eps):
        return CAGRCalculator.eps_cagr(start_eps, end_eps, 5)

    @staticmethod
    def eps_cagr_10yr(start_eps, end_eps):
        return CAGRCalculator.eps_cagr(start_eps, end_eps, 10)