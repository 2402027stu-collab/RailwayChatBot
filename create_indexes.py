import sqlite3

conn = sqlite3.connect("Database/railway.db")
cursor = conn.cursor()

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_train_number
ON schedules(train_number);
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_station_code
ON schedules(station_code);
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_train_station
ON schedules(train_number, station_code);
""")

conn.commit()
conn.close()

print("✅ Indexes created successfully!")