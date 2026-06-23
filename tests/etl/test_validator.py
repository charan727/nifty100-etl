import pandas as pd
from src.etl.validator import (
    validate_dataframe,
    validate_primary_key
)


def test_validator():
    df = pd.DataFrame({"A": [1, 2, 3]})
    assert validate_dataframe(df) is True


def test_empty_dataframe():
    df = pd.DataFrame()
    assert validate_dataframe(df) is True


def test_duplicate_rows():
    df = pd.DataFrame({
        "A": [1, 1, 2],
        "B": [10, 10, 20]
    })
    assert validate_dataframe(df) is True


def test_missing_values():
    df = pd.DataFrame({
        "A": [1, None, 3]
    })
    assert validate_dataframe(df) is True


def test_primary_key_unique():
    df = pd.DataFrame({
        "id": ["A", "B", "C"]
    })
    validate_primary_key(df, "id")


def test_primary_key_duplicate():
    df = pd.DataFrame({
        "id": ["A", "A", "B"]
    })
    validate_primary_key(df, "id")