import sqlite3
import pandas as pd

conn = sqlite3.connect("Database/railway.db")

df = pd.read_sql(
    """
    PRAGMA table_info(schedules);
    """,
    conn
)

print(df)

conn.close()