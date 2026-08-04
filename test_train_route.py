import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

df = pd.read_sql(
    """
    SELECT
        train_number,
        station_code,
        station_name,
        id
    FROM schedules
    WHERE train_number='10104'
    ORDER BY id
    """,
    conn
)

print(df)

conn.close()