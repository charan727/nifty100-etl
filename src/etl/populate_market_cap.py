import pandas as pd

from src.etl.database import create_connection
from src.config import SUPPORTING_DATA_PATH


def populate_market_cap():

    conn = create_connection()

    file_path = SUPPORTING_DATA_PATH / "market_cap.xlsx"

    df = pd.read_excel(file_path)

    df.to_sql(
        "market_cap",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    print(f"{len(df)} rows inserted into market_cap table.")

    conn.close()


if __name__ == "__main__":
    populate_market_cap()