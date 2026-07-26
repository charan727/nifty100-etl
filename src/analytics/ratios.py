"""
Financial Ratio Engine
Sprint 2 - Day 08/09
"""

import logging

logging.basicConfig(
    filename="output/ratio_engine.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FinancialRatios:

    @staticmethod
    def net_profit_margin(net_profit, sales):
        try:
            if sales is None or sales == 0:
                return None
            return round((net_profit / sales) * 100, 2)
        except Exception as e:
            logging.error(f"Net Profit Margin Error: {e}")
            return None

    @staticmethod
    def operating_profit_margin(operating_profit, sales):
        try:
            if sales is None or sales == 0:
                return None
            return round((operating_profit / sales) * 100, 2)
        except Exception as e:
            logging.error(f"Operating Profit Margin Error: {e}")
            return None

    @staticmethod
    def validate_opm(calculated_opm, source_opm):
        if calculated_opm is None or source_opm is None:
            return False
        if abs(calculated_opm - source_opm) > 1:
            logging.warning(f"OPM mismatch | Calculated={calculated_opm}, Source={source_opm}")
            return True
        return False

    @staticmethod
    def return_on_equity(net_profit, equity_capital, reserves):
        try:
            capital = (equity_capital or 0) + (reserves or 0)
            if capital <= 0:
                return None
            return round((net_profit / capital) * 100, 2)
        except Exception as e:
            logging.error(f"ROE Error: {e}")
            return None

    @staticmethod
    def return_on_capital_employed(operating_profit, other_income, interest,
                                   equity_capital, reserves, borrowings):
        try:
            capital = (equity_capital or 0) + (reserves or 0) + (borrowings or 0)
            if capital <= 0:
                return None
            ebit = (operating_profit or 0) + (other_income or 0) - (interest or 0)
            return round((ebit / capital) * 100, 2)
        except Exception as e:
            logging.error(f"ROCE Error: {e}")
            return None

    @staticmethod
    def return_on_assets(net_profit, total_assets):
        try:
            if total_assets is None or total_assets == 0:
                return None
            return round((net_profit / total_assets) * 100, 2)
        except Exception as e:
            logging.error(f"ROA Error: {e}")
            return None

    @staticmethod
    def debt_to_equity(borrowings, equity_capital, reserves):
        try:
            borrowings = borrowings or 0
            capital = (equity_capital or 0) + (reserves or 0)
            if borrowings == 0:
                return 0
            if capital <= 0:
                return None
            return round(borrowings / capital, 2)
        except Exception as e:
            logging.error(f"Debt to Equity Error: {e}")
            return None

    @staticmethod
    def high_leverage_flag(borrowings, equity_capital, reserves, sector):
        ratio = FinancialRatios.debt_to_equity(borrowings, equity_capital, reserves)
        if ratio is None:
            return False
        return ratio > 2 and (sector or "").lower() != "financials"

    @staticmethod
    def interest_coverage(operating_profit, other_income, interest):
        try:
            if interest is None or interest == 0:
                return None
            return round(
    ((operating_profit or 0) + (other_income or 0)) / interest,
    2
)
        except Exception as e:
            logging.error(f"Interest Coverage Error: {e}")
            return None

    @staticmethod
    def interest_coverage_label(interest):
        if interest in (None, 0):
            return "Debt Free"
        return "Interest Bearing"

    @staticmethod
    def interest_warning(icr):
        return icr is not None and icr < 1.5

    @staticmethod
    def net_debt(borrowings, investments):
        return round((borrowings or 0) - (investments or 0),2)

    @staticmethod
    def asset_turnover(sales, total_assets):
        try:
            if total_assets is None or total_assets == 0:
                return None
            return round((sales or 0)/total_assets,2)
        except Exception as e:
            logging.error(f"Asset Turnover Error: {e}")
            return None

    @staticmethod
    def book_value_per_share(book_value, face_value):
        try:
            if face_value is None or face_value == 0:
                return None
            return round(book_value/face_value,2)
        except Exception as e:
            logging.error(f"Book Value Error: {e}")
            return None

    @staticmethod
    def dividend_payout_ratio(dividend_payout):
        if dividend_payout is None:
            return None
        return round(dividend_payout,2)


    @staticmethod
    def dividend_yield(dividend_per_share, market_price):
        try:
            if market_price is None or market_price == 0:
                return None
            return round((dividend_per_share / market_price) * 100, 2)
        except Exception as e:
            logging.error(f"Dividend Yield Error: {e}")
            return None

    @staticmethod
    def earnings_per_share(net_profit, shares_outstanding):
        try:
            if shares_outstanding is None or shares_outstanding == 0:
                return None
            return round(net_profit / shares_outstanding, 2)
        except Exception as e:
            logging.error(f"EPS Error: {e}")
            return None

    @staticmethod
    def current_ratio(current_assets, current_liabilities):
        try:
            if current_liabilities is None or current_liabilities == 0:
                return None
            return round(current_assets / current_liabilities, 2)
        except Exception as e:
            logging.error(f"Current Ratio Error: {e}")
            return None

    @staticmethod
    def quick_ratio(current_assets, inventory, current_liabilities):
        try:
            if current_liabilities is None or current_liabilities == 0:
                return None
            return round((current_assets - (inventory or 0)) / current_liabilities, 2)
        except Exception as e:
            logging.error(f"Quick Ratio Error: {e}")
            return None

    @staticmethod
    def working_capital(current_assets, current_liabilities):
        return round((current_assets or 0) - (current_liabilities or 0), 2)

    @staticmethod
    def debt_ratio(total_liabilities, total_assets):
        try:
            if total_assets is None or total_assets == 0:
                return None
            return round(total_liabilities / total_assets, 2)
        except Exception as e:
            logging.error(f"Debt Ratio Error: {e}")
            return None

    @staticmethod
    def equity_ratio(total_equity, total_assets):
        try:
            if total_assets is None or total_assets == 0:
                return None
            return round(total_equity / total_assets, 2)
        except Exception as e:
            logging.error(f"Equity Ratio Error: {e}")
            return None

    @staticmethod
    def price_to_earnings(market_price, eps):
        try:
            if eps is None or eps == 0:
                return None
            return round(market_price / eps, 2)
        except Exception as e:
            logging.error(f"P/E Error: {e}")
            return None

    @staticmethod
    def price_to_book(market_price, book_value_per_share):
        try:
            if book_value_per_share is None or book_value_per_share == 0:
                return None
            return round(market_price / book_value_per_share, 2)
        except Exception as e:
            logging.error(f"P/B Error: {e}")
            return None

    @staticmethod
    def enterprise_value(market_cap, total_debt, cash):
        try:
            return round((market_cap or 0) + (total_debt or 0) - (cash or 0), 2)
        except Exception as e:
            logging.error(f"Enterprise Value Error: {e}")
            return None

    @staticmethod
    def ev_to_ebitda(enterprise_value, ebitda):
        try:
            if ebitda is None or ebitda == 0:
                return None
            return round(enterprise_value / ebitda, 2)
        except Exception as e:
            logging.error(f"EV/EBITDA Error: {e}")
            return None