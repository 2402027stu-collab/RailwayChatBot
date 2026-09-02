import sqlite3

DB_PATH = "Database/railway.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("RAILWAY DATABASE STRUCTURE")
print("=" * 60)

# Get tables
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

tables = cursor.fetchall()

print("\nTABLES:")
for table in tables:
    print("-", table[0])


# Get columns and sample data
for table in tables:

    table_name = table[0]

    print("\n" + "=" * 60)
    print("TABLE:", table_name)
    print("=" * 60)

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    print("\nCOLUMNS:")

    for column in columns:
        print(
            f"  {column[1]} "
            f"({column[2]})"
        )

    print("\nSAMPLE DATA:")

    cursor.execute(
        f"SELECT * FROM {table_name} LIMIT 3"
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)


conn.close()

print("\n" + "=" * 60)
print("DONE")
print("=" * 60)