import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

print("===== TABLES =====")
print(pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
))

print("\n===== TRAINS COLUMNS =====")
print(pd.read_sql(
    "PRAGMA table_info(trains);",
    conn
))

conn.close()