import pandas as pd
import sqlite3

# -----------------------------
# Load Clean CSV Files
# -----------------------------
trains = pd.read_csv("Data/clean_trains.csv")
stations = pd.read_csv("Data/clean_stations.csv")
schedules = pd.read_csv("Data/clean_schedules.csv")

# -----------------------------
# Connect to SQLite Database
# -----------------------------
conn = sqlite3.connect("Database/railway.db")

# -----------------------------
# Create Tables
# -----------------------------
trains.to_sql("trains", conn, if_exists="replace", index=False)

stations.to_sql("stations", conn, if_exists="replace", index=False)

schedules.to_sql("schedules", conn, if_exists="replace", index=False)

# -----------------------------
# Save Changes
# -----------------------------
conn.commit()

print("✅ Railway Database Created Successfully!")

# -----------------------------
# Close Database
# -----------------------------
conn.close()