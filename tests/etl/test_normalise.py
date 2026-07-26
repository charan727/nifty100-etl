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


def test_normalize_empty_year():
    df = pd.DataFrame({"year": ["", None, "2022"]})
    df = normalize_year(df)
    assert df["year"].dtype == "int64"


def test_normalize_year_float():
    df = pd.DataFrame({"year": [2020.0, 2021.0]})
    df = normalize_year(df)
    assert df["year"].tolist() == [2020, 2021]


def test_normalize_year_spaces():
    df = pd.DataFrame({"year": [" 2020 ", " 2021 "]})
    df = normalize_year(df)
    assert df["year"].tolist() == [2020, 2021]


def test_normalize_year_mixed():
    df = pd.DataFrame({"year": ["2020", 2021, 2022.0]})
    df = normalize_year(df)
    assert df["year"].tolist() == [2020, 2021, 2022]


def test_normalize_ticker_lowercase():
    df = pd.DataFrame({"ticker": ["tcs", "infy"]})
    df = normalize_ticker(df)
    assert all(df["ticker"].str.isupper())


def test_normalize_ticker_spaces():
    df = pd.DataFrame({"ticker": [" tcs ", " infy "]})
    df = normalize_ticker(df)
    assert df["ticker"].tolist() == ["TCS", "INFY"]


def test_normalize_ticker_already_upper():
    df = pd.DataFrame({"ticker": ["TCS", "INFY"]})
    df = normalize_ticker(df)
    assert df["ticker"].tolist() == ["TCS", "INFY"]


def test_normalize_company_id_spaces():
    df = pd.DataFrame({"company_id": [" reliance ", " hdfcbank "]})
    df = normalize_ticker(df)
    assert df["company_id"].tolist() == ["RELIANCE", "HDFCBANK"]


def test_normalize_id_mixed():
    df = pd.DataFrame({"id": [" tCs ", "InFy"]})
    df = normalize_ticker(df)
    assert df["id"].tolist() == ["TCS", "INFY"]


def test_dataframe_shape_preserved():
    df = pd.DataFrame({
        "ticker": ["tcs", "infy"],
        "year": ["2020", "2021"]
    })
    rows_before = df.shape[0]
    df = normalize_year(df)
    df = normalize_ticker(df)
    assert df.shape[0] == rows_before