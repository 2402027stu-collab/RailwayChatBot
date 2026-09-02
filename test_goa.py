import sqlite3

conn = sqlite3.connect("Database/railway.db")

cursor = conn.cursor()

print("\nSTATIONS MATCHING GOA\n")
print("=" * 60)

cursor.execute("""
    SELECT state, code, name, zone
    FROM stations
    WHERE LOWER(state) LIKE '%goa%'
    ORDER BY name
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

print("\nTOTAL:", len(rows))

print("\nTRAINS WITH GOA IN DESTINATION\n")
print("=" * 60)

cursor.execute("""
    SELECT number, name, from_station_name, to_station_name
    FROM trains
    WHERE LOWER(to_station_name) LIKE '%goa%'
    LIMIT 20
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

print("\nTOTAL:", len(rows))

conn.close()