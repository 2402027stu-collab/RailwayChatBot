import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

query = """
SELECT DISTINCT from_station_name
FROM trains
WHERE from_station_name LIKE '%MUMBAI%'
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()