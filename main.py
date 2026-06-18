from src.etl.loader import load_excel


def main():
    print("=" * 50)
    print("NIFTY100 ETL PROJECT")
    print("=" * 50)

    companies = load_excel("companies.xlsx")

    print("\nCompanies Dataset Loaded Successfully")
    print(f"Shape : {companies.shape}")

    print("\nFirst 5 Records:")
    print(companies.head())


if __name__ == "__main__":
    main()