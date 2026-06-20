import pandas as pd


def validate_dataframe(df):
    """
    Perform basic data quality validation.
    """

    print("\nRunning Data Quality Checks...")

    # DQ-01: Empty DataFrame
    if df.empty:
        print("[ERROR] DataFrame is empty.")
    else:
        print("[OK] DataFrame contains data.")

    # DQ-02: Duplicate Rows
    duplicates = df.duplicated().sum()
    print(f"Duplicate Rows : {duplicates}")

    # DQ-03: Missing Values
    missing = df.isnull().sum().sum()
    print(f"Missing Values : {missing}")

    # DQ-04: Column Count
    print(f"Total Columns : {len(df.columns)}")

    # DQ-05: Row Count
    print(f"Total Rows : {len(df)}")

    with open("output/validation_failures.csv", "a") as f:
        f.write(f"{len(df)},{duplicates},{missing}\n")

    return True


def validate_primary_key(df, column):
    """
    Check whether the given column contains duplicate values.
    """

    if column not in df.columns:
        print(f"[WARNING] {column} column not found.")
        return False

    duplicates = df[column].duplicated().sum()

    if duplicates == 0:
        print(f"[OK] {column} is unique.")
        return True
    else:
        print(f"[ERROR] {duplicates} duplicate {column} values found.")
        return False


def validate_positive_values(df, column):
    """
    DQ-06: Check whether numeric column contains negative values.
    """

    if column not in df.columns:
        print(f"[WARNING] {column} column not found.")
        return True

    invalid = (df[column] < 0).sum()

    if invalid == 0:
        print(f"[OK] {column} contains valid values.")
        return True
    else:
        print(f"[ERROR] {invalid} negative values found in {column}.")
        return False