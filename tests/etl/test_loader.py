import pandas as pd
import pytest

from src.etl.loader import load_excel


# ----------------------------
# Core Data Files
# ----------------------------

CORE_FILES = [
    "companies.xlsx",
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx",
]


# ----------------------------
# Supporting Files
# ----------------------------

SUPPORTING_FILES = [
    "financial_ratios.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
]


# ----------------------------
# Core File Tests
# ----------------------------

@pytest.mark.parametrize("file_name", CORE_FILES)
def test_load_core_files(file_name):
    df = load_excel(file_name)

    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) > 0


# ----------------------------
# Supporting File Tests
# ----------------------------

@pytest.mark.parametrize("file_name", SUPPORTING_FILES)
def test_load_supporting_files(file_name):
    df = load_excel(file_name, "supporting")

    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) > 0


# ----------------------------
# DataFrame Validation
# ----------------------------

@pytest.mark.parametrize(
    "file_name,folder",
    [(f, None) for f in CORE_FILES] +
    [(f, "supporting") for f in SUPPORTING_FILES]
)
def test_dataframe_is_valid(file_name, folder):

    if folder:
        df = load_excel(file_name, folder)
    else:
        df = load_excel(file_name)

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0
    assert df.shape[1] > 0


@pytest.mark.parametrize(
    "file_name,folder",
    [(f, None) for f in CORE_FILES] +
    [(f, "supporting") for f in SUPPORTING_FILES]
)
def test_dataframe_has_column_names(file_name, folder):

    if folder:
        df = load_excel(file_name, folder)
    else:
        df = load_excel(file_name)

    assert all(str(col).strip() != "" for col in df.columns)


@pytest.mark.parametrize(
    "file_name,folder",
    [(f, None) for f in CORE_FILES] +
    [(f, "supporting") for f in SUPPORTING_FILES]
)
def test_dataframe_not_all_null(file_name, folder):

    if folder:
        df = load_excel(file_name, folder)
    else:
        df = load_excel(file_name)

    assert not df.isnull().all().all()