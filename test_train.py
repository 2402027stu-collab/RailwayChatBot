import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

query = """
SELECT number,
       from_station_code,
       to_station_code,
       from_station_name,
       to_station_name
FROM trains
WHERE number = '10104'
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()