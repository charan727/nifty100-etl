import pandas as pd
from src.etl.normaliser import normalize_year, normalize_ticker


def test_normalize_year():
    df = pd.DataFrame({"year": ["2020", "2021", "2022"]})
    df = normalize_year(df)
    assert df["year"].dtype == "int64"


def test_normalize_year_with_invalid_value():
    df = pd.DataFrame({"year": ["2020", "ABC", None]})
    df = normalize_year(df)
    assert df["year"].dtype == "int64"


def test_normalize_ticker_id():
    df = pd.DataFrame({"id": [" tcs ", "infy", " RELIANCE "]})
    df = normalize_ticker(df)
    assert df["id"].tolist() == ["TCS", "INFY", "RELIANCE"]


def test_normalize_company_id():
    df = pd.DataFrame({"company_id": [" tcs ", "infy"]})
    df = normalize_ticker(df)
    assert df["company_id"].tolist() == ["TCS", "INFY"]


def test_normalize_ticker_column():
    df = pd.DataFrame({"ticker": [" tcs ", "infy"]})
    df = normalize_ticker(df)
    assert df["ticker"].tolist() == ["TCS", "INFY"]