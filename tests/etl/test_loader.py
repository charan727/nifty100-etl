from src.etl.loader import load_excel


def test_load_companies():
    df = load_excel("companies.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_analysis():
    df = load_excel("analysis.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_balancesheet():
    df = load_excel("balancesheet.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_cashflow():
    df = load_excel("cashflow.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_documents():
    df = load_excel("documents.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_profitandloss():
    df = load_excel("profitandloss.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_prosandcons():
    df = load_excel("prosandcons.xlsx")
    assert df is not None
    assert len(df) > 0


def test_load_financial_ratios():
    df = load_excel("financial_ratios.xlsx", "supporting")
    assert df is not None
    assert len(df) > 0


def test_load_peer_groups():
    df = load_excel("peer_groups.xlsx", "supporting")
    assert df is not None
    assert len(df) > 0


def test_load_sectors():
    df = load_excel("sectors.xlsx", "supporting")
    assert df is not None
    assert len(df) > 0


def test_load_stock_prices():
    df = load_excel("stock_prices.xlsx", "supporting")
    assert df is not None
    assert len(df) > 0