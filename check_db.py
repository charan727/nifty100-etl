import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

tables = [
    "companies",
    "market_cap",
    "financial_ratios",
    "sectors"
]

print("\nTable Counts")
print("-" * 30)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"{table:20} : {count}")

conn.close()