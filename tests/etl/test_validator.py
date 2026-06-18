def validate_primary_key(df, column):
    duplicates = df[column].duplicated().sum()

    if duplicates == 0:
        print(f"[OK] {column} is unique.")
    else:
        print(f"[ERROR] {duplicates} duplicate {column} values found.")