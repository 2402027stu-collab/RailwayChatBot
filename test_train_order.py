import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

df = pd.read_sql("""
SELECT *
FROM trains
WHERE number='10103'
""", conn)

print(df.T)

conn.close()