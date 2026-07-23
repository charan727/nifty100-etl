import re
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

PATTERN = r"(\d+)\s*Years?:?\s*([\d.]+)%"

INPUT_FILE = Path("data/core/analysis.xlsx")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------

def parse_text(text):
    """
    Parse text like:
        10 Years: 21%
        5 Years: 15%

    Returns:
        {
            "period_years": 10,
            "value_pct": 21.0
        }

    Returns None if pattern does not match.
    """

    if pd.isna(text):
        return None

    text = str(text).strip()

    match = re.search(PATTERN, text)

    if match:
        return {
            "period_years": int(match.group(1)),
            "value_pct": float(match.group(2))
        }

    return None


# ---------------------------------------------------------------------
# Load Excel
# ---------------------------------------------------------------------

def load_analysis_file(file_path):
    df = pd.read_excel(file_path, header=1)
    df.columns = df.columns.str.strip()
    return df


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main():

    print("=" * 60)
    print("Loading analysis.xlsx...")
    print("=" * 60)

    df = load_analysis_file(INPUT_FILE)

    print(f"Loaded {len(df)} records\n")

    metrics = [
        "compounded_sales_growth",
        "compounded_profit_growth",
        "stock_price_cagr",
        "roe"
    ]

    parsed_rows = []
    failed_rows = []

    for _, row in df.iterrows():

        company_id = row["company_id"]

        for metric in metrics:

            value = row.get(metric)

            result = parse_text(value)

            if result:

                parsed_rows.append({
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": result["period_years"],
                    "value_pct": result["value_pct"]
                })

            else:

                failed_rows.append({
                    "company_id": company_id,
                    "metric_type": metric,
                    "raw_text": value
                })

    parsed_df = pd.DataFrame(parsed_rows)
    failed_df = pd.DataFrame(failed_rows)

    parsed_output = OUTPUT_DIR / "analysis_parsed.csv"
    failed_output = OUTPUT_DIR / "parse_failures.csv"

    parsed_df.to_csv(parsed_output, index=False)
    failed_df.to_csv(failed_output, index=False)

    print("=" * 60)
    print("Parser Summary")
    print("=" * 60)

    print(f"Total Companies       : {df['company_id'].nunique()}")
    print(f"Parsed Records        : {len(parsed_df)}")
    print(f"Failed Records        : {len(failed_df)}")

    print("\nGenerated Files")
    print("----------------------------")
    print(parsed_output)
    print(failed_output)

    print("\nDay 29 Parser completed successfully.")


if __name__ == "__main__":
    main()