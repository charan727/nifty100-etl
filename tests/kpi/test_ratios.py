import pytest

from src.analytics.ratios import FinancialRatios


# -----------------------------
# Net Profit Margin
# -----------------------------

def test_net_profit_margin():
    assert FinancialRatios.net_profit_margin(100, 1000) == 10.0


def test_net_profit_margin_zero_sales():
    assert FinancialRatios.net_profit_margin(100, 0) is None


# -----------------------------
# Operating Profit Margin
# -----------------------------

def test_operating_profit_margin():
    assert FinancialRatios.operating_profit_margin(200, 1000) == 20.0


def test_validate_opm_match():
    assert FinancialRatios.validate_opm(20, 20) is False


def test_validate_opm_mismatch():
    assert FinancialRatios.validate_opm(20, 25) is True


# -----------------------------
# ROE
# -----------------------------

def test_return_on_equity():
    assert FinancialRatios.return_on_equity(100, 200, 300) == 20.0


def test_return_on_equity_negative_capital():
    assert FinancialRatios.return_on_equity(100, -200, -100) is None


# -----------------------------
# ROCE
# -----------------------------

def test_return_on_capital_employed():
    value = FinancialRatios.return_on_capital_employed(
        300,
        20,
        20,
        500,
        500,
        500
    )
    assert round(value, 2) == 20.0


# -----------------------------
# ROA
# -----------------------------

def test_return_on_assets():
    assert FinancialRatios.return_on_assets(100, 1000) == 10.0


def test_return_on_assets_zero():
    assert FinancialRatios.return_on_assets(100, 0) is None


# -----------------------------
# Debt To Equity
# -----------------------------

def test_debt_to_equity():
    assert FinancialRatios.debt_to_equity(500, 250, 250) == 1.0


def test_debt_to_equity_debt_free():
    assert FinancialRatios.debt_to_equity(0, 250, 250) == 0


# -----------------------------
# High Leverage
# -----------------------------

def test_high_leverage_flag():
    assert FinancialRatios.high_leverage_flag(
        2000,
        100,
        100,
        "IT"
    ) is True


def test_high_leverage_financial_sector():
    assert FinancialRatios.high_leverage_flag(
        2000,
        100,
        100,
        "Financials"
    ) is False


# -----------------------------
# Interest Coverage
# -----------------------------

def test_interest_coverage():
    assert FinancialRatios.interest_coverage(
        500,
        100,
        100
    ) == 6.0


def test_interest_coverage_zero_interest():
    assert FinancialRatios.interest_coverage(
        500,
        100,
        0
    ) is None


def test_interest_label():
    assert FinancialRatios.interest_coverage_label(0) == "Debt Free"


def test_interest_warning():
    assert FinancialRatios.interest_warning(1.2) is True


# -----------------------------
# Net Debt
# -----------------------------

def test_net_debt():
    assert FinancialRatios.net_debt(1000, 200) == 800


# -----------------------------
# Asset Turnover
# -----------------------------

def test_asset_turnover():
    assert FinancialRatios.asset_turnover(1000, 500) == 2.0


# -----------------------------
# Book Value
# -----------------------------

def test_book_value_per_share():
    assert FinancialRatios.book_value_per_share(500, 10) == 50.0


# -----------------------------
# Dividend
# -----------------------------

def test_dividend_payout():
    assert FinancialRatios.dividend_payout_ratio(35.55) == 35.55


def test_dividend_yield():
    assert FinancialRatios.dividend_yield(10, 200) == 5.0


# -----------------------------
# EPS
# -----------------------------

def test_eps():
    assert FinancialRatios.earnings_per_share(1000, 100) == 10.0


# -----------------------------
# Liquidity
# -----------------------------

def test_current_ratio():
    assert FinancialRatios.current_ratio(500, 250) == 2.0


def test_quick_ratio():
    assert FinancialRatios.quick_ratio(
        500,
        100,
        200
    ) == 2.0


def test_working_capital():
    assert FinancialRatios.working_capital(
        500,
        300
    ) == 200


# -----------------------------
# Debt / Equity Ratio
# -----------------------------

def test_debt_ratio():
    assert FinancialRatios.debt_ratio(
        400,
        1000
    ) == 0.4


def test_equity_ratio():
    assert FinancialRatios.equity_ratio(
        600,
        1000
    ) == 0.6


# -----------------------------
# Market Ratios
# -----------------------------

def test_price_to_earnings():
    assert FinancialRatios.price_to_earnings(
        500,
        25
    ) == 20.0


def test_price_to_book():
    assert FinancialRatios.price_to_book(
        500,
        100
    ) == 5.0


# -----------------------------
# Enterprise Value
# -----------------------------

def test_enterprise_value():
    assert FinancialRatios.enterprise_value(
        1000,
        500,
        100
    ) == 1400


def test_ev_to_ebitda():
    assert FinancialRatios.ev_to_ebitda(
        1400,
        200
    ) == 7.0