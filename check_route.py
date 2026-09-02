import sqlite3

DB_PATH = "Database/railway.db"


def check_route():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    source = "MAO"
    destination = "PUNE"

    print("=" * 70)
    print("MADGAON (MAO) → PUNE (PUNE) ROUTE CHECK")
    print("=" * 70)

    query = """
        SELECT
            train_number,
            train_name,
            COUNT(DISTINCT station_code) AS station_count
        FROM schedules
        WHERE station_code IN (?, ?)
        GROUP BY train_number, train_name
        HAVING COUNT(DISTINCT station_code) = 2
        ORDER BY train_number
    """

    cursor.execute(query, (source, destination))
    trains = cursor.fetchall()

    if not trains:
        print("\n❌ No train was found that has BOTH:")
        print("   MAO  →  MADGAON")
        print("   PUNE →  PUNE JN")
    else:
        print(f"\n✅ Found {len(trains)} train(s):\n")

        for train_number, train_name, station_count in trains:
            print("-" * 70)
            print(f"Train Number : {train_number}")
            print(f"Train Name   : {train_name}")

            # Get MAO details
            cursor.execute(
                """
                SELECT arrival, departure, day
                FROM schedules
                WHERE train_number = ?
                AND station_code = ?
                LIMIT 1
                """,
                (train_number, source)
            )

            source_data = cursor.fetchone()

            # Get PUNE details
            cursor.execute(
                """
                SELECT arrival, departure, day
                FROM schedules
                WHERE train_number = ?
                AND station_code = ?
                LIMIT 1
                """,
                (train_number, destination)
            )

            destination_data = cursor.fetchone()

            print(f"From         : MADGAON (MAO)")
            print(f"Arrival      : {source_data[0] if source_data else 'N/A'}")
            print(f"Departure    : {source_data[1] if source_data else 'N/A'}")
            print(f"Day          : {source_data[2] if source_data else 'N/A'}")

            print()
            print(f"To           : PUNE JN (PUNE)")
            print(f"Arrival      : {destination_data[0] if destination_data else 'N/A'}")
            print(f"Departure    : {destination_data[1] if destination_data else 'N/A'}")
            print(f"Day          : {destination_data[2] if destination_data else 'N/A'}")

    conn.close()

    print("\n" + "=" * 70)


if __name__ == "__main__":
    check_route()