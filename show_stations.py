import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

query = """
SELECT DISTINCT from_station_name
FROM trains
ORDER BY from_station_name
LIMIT 100;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()