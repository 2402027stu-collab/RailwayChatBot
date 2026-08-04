import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

query = """
SELECT number,
       name,
       from_station_name,
       to_station_name,
       distance
FROM trains
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()