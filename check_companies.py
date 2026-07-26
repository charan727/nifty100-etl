import sqlite3

conn = sqlite3.connect("db/nifty100.db")

print("===== COLUMNS =====")
for row in conn.execute("PRAGMA table_info(companies)"):
    print(row)

print("\n===== SAMPLE DATA =====")
for row in conn.execute("SELECT * FROM companies LIMIT 5"):
    print(row)

conn.close()