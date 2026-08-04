import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

query = """
SELECT code, name
FROM stations
WHERE name LIKE '%Madgaon%'
   OR name LIKE '%Thivim%'
   OR name LIKE '%Vasco%'
"""

print(pd.read_sql(query, conn))

conn.close()