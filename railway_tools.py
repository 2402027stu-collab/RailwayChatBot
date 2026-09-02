import sqlite3
from pathlib import Path

# ============================================================
# DATABASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "Database" / "railway.db"


def get_connection():
    return sqlite3.connect(str(DB_PATH))


# ============================================================
# HELPERS
# ============================================================

def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def find_station(place):
    """
    Find station by code, name, city or state.
    """

    place = clean_text(place)

    if not place:
        return []

    conn = get_connection()

    try:
        query = """
            SELECT code, name, state, zone, address
            FROM stations
            WHERE
                UPPER(code) = UPPER(?)
                OR UPPER(name) LIKE UPPER(?)
                OR UPPER(state) LIKE UPPER(?)
                OR UPPER(address) LIKE UPPER(?)
            ORDER BY
                CASE
                    WHEN UPPER(code) = UPPER(?) THEN 1
                    WHEN UPPER(name) = UPPER(?) THEN 2
                    ELSE 3
                END
        """

        pattern = f"%{place}%"

        rows = conn.execute(
            query,
            (
                place,
                pattern,
                pattern,
                pattern,
                place,
                place
            )
        ).fetchall()

        return rows

    finally:
        conn.close()


# ============================================================
# TRAIN SEARCH
# ============================================================

def train_search(train_number):
    """
    Search train by train number.
    """

    train_number = clean_text(train_number)

    conn = get_connection()

    try:
        query = """
            SELECT
                number,
                name,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                duration_h,
                duration_m,
                type,
                distance,
                zone,
                first_ac,
                second_ac,
                third_ac,
                sleeper,
                chair_car
            FROM trains
            WHERE number = ?
        """

        return conn.execute(query, (train_number,)).fetchall()

    finally:
        conn.close()


def train_search_by_name(name):
    """
    Search trains by train name.
    """

    name = clean_text(name)

    conn = get_connection()

    try:
        query = """
            SELECT
                number,
                name,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                duration_h,
                duration_m,
                type,
                distance,
                zone
            FROM trains
            WHERE UPPER(name) LIKE UPPER(?)
            LIMIT 30
        """

        return conn.execute(
            query,
            (f"%{name}%",)
        ).fetchall()

    finally:
        conn.close()


# ============================================================
# STATION SEARCH
# ============================================================

def station_search(place):
    """
    Search station by station name, code, state or address.
    """

    return find_station(place)


# ============================================================
# SCHEDULE SEARCH
# ============================================================

def schedule_search(train_number):
    """
    Get complete schedule of a train.
    """

    train_number = clean_text(train_number)

    conn = get_connection()

    try:
        query = """
            SELECT
                train_number,
                train_name,
                station_code,
                station_name,
                arrival,
                departure,
                day
            FROM schedules
            WHERE train_number = ?
            ORDER BY id
        """

        return conn.execute(
            query,
            (train_number,)
        ).fetchall()

    finally:
        conn.close()


# ============================================================
# TRAIN STATIONS
# ============================================================

def search_train_stations(train_number):
    """
    Return all stations visited by a train.
    """

    rows = schedule_search(train_number)

    if not rows:
        return []

    stations = []

    for row in rows:

        stations.append({
            "train_number": row[0],
            "train_name": row[1],
            "station_code": row[2],
            "station_name": row[3],
            "arrival": row[4],
            "departure": row[5],
            "day": row[6]
        })

    return stations


# ============================================================
# ROUTE SEARCH
# ============================================================

def route_search(source, destination, limit=50):
    """
    Find direct trains between two stations/cities.
    Uses schedules, so intermediate stations are supported.
    """

    source = clean_text(source)
    destination = clean_text(destination)

    if not source or not destination:
        return []

    conn = get_connection()

    try:

        query = """
            SELECT DISTINCT
                s1.train_number,
                s1.train_name,

                s1.station_code,
                s1.station_name,

                s1.arrival,
                s1.departure,
                s1.day,

                s2.station_code,
                s2.station_name,

                s2.arrival,
                s2.departure,
                s2.day

            FROM schedules s1

            JOIN schedules s2
                ON s1.train_number = s2.train_number

            WHERE
                (
                    UPPER(s1.station_name) LIKE UPPER(?)
                    OR UPPER(s1.station_code) = UPPER(?)
                )

                AND

                (
                    UPPER(s2.station_name) LIKE UPPER(?)
                    OR UPPER(s2.station_code) = UPPER(?)
                )

                AND s1.id < s2.id

            ORDER BY s1.train_number

            LIMIT ?
        """

        source_pattern = f"%{source}%"
        destination_pattern = f"%{destination}%"

        return conn.execute(
            query,
            (
                source_pattern,
                source,

                destination_pattern,
                destination,

                limit
            )
        ).fetchall()

    finally:
        conn.close()


# ============================================================
# TRAINS TO STATION / CITY / STATE
# ============================================================

def trains_to_station(place, limit=50):
    """
    Find trains whose route reaches a station matching
    the supplied place.
    """

    stations = find_station(place)

    if not stations:
        return []

    station_codes = [
        clean_text(row[0])
        for row in stations
    ]

    station_names = [
        clean_text(row[1])
        for row in stations
    ]

    conn = get_connection()

    try:

        conditions = []
        params = []

        for code in station_codes:
            conditions.append(
                "UPPER(to_station_code) = UPPER(?)"
            )
            params.append(code)

        for name in station_names:
            conditions.append(
                "UPPER(to_station_name) = UPPER(?)"
            )
            params.append(name)

        if not conditions:
            return []

        query = f"""
            SELECT
                number,
                name,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                duration_h,
                duration_m,
                type,
                distance,
                zone
            FROM trains
            WHERE {" OR ".join(conditions)}
            ORDER BY number
            LIMIT ?
        """

        params.append(limit)

        return conn.execute(
            query,
            params
        ).fetchall()

    finally:
        conn.close()


def trains_from_station(place, limit=50):
    """
    Find trains starting from a station/city.
    """

    stations = find_station(place)

    if not stations:
        return []

    station_codes = [
        clean_text(row[0])
        for row in stations
    ]

    station_names = [
        clean_text(row[1])
        for row in stations
    ]

    conn = get_connection()

    try:

        conditions = []
        params = []

        for code in station_codes:
            conditions.append(
                "UPPER(from_station_code) = UPPER(?)"
            )
            params.append(code)

        for name in station_names:
            conditions.append(
                "UPPER(from_station_name) = UPPER(?)"
            )
            params.append(name)

        if not conditions:
            return []

        query = f"""
            SELECT
                number,
                name,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                duration_h,
                duration_m,
                type,
                distance,
                zone
            FROM trains
            WHERE {" OR ".join(conditions)}
            ORDER BY number
            LIMIT ?
        """

        params.append(limit)

        return conn.execute(
            query,
            params
        ).fetchall()

    finally:
        conn.close()


# ============================================================
# SEARCH TRAINS PASSING THROUGH A STATION
# ============================================================

def search_trains_passing_station(place, limit=50):
    """
    Find trains appearing in schedules at a station.
    Useful for questions like:
    'Which trains stop at Madgaon?'
    """

    stations = find_station(place)

    if not stations:
        return []

    codes = [
        clean_text(row[0])
        for row in stations
    ]

    names = [
        clean_text(row[1])
        for row in stations
    ]

    conn = get_connection()

    try:

        conditions = []
        params = []

        for code in codes:
            conditions.append(
                "UPPER(station_code) = UPPER(?)"
            )
            params.append(code)

        for name in names:
            conditions.append(
                "UPPER(station_name) = UPPER(?)"
            )
            params.append(name)

        query = f"""
            SELECT DISTINCT
                train_number,
                train_name,
                station_code,
                station_name,
                arrival,
                departure,
                day
            FROM schedules
            WHERE {" OR ".join(conditions)}
            ORDER BY train_number
            LIMIT ?
        """

        params.append(limit)

        return conn.execute(
            query,
            params
        ).fetchall()

    finally:
        conn.close()


# ============================================================
# DATABASE STATUS
# ============================================================

def database_status():
    """
    Check railway database.
    """

    conn = get_connection()

    try:

        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        ).fetchall()

        result = {
            "database": str(DB_PATH),
            "connected": True,
            "tables": [row[0] for row in tables]
        }

        for table in ["trains", "stations", "schedules"]:

            if table in result["tables"]:

                count = conn.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]

                result[f"{table}_count"] = count

        return result

    finally:
        conn.close()


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

def search_train(train_number):
    return train_search(train_number)


def search_train_by_name(name):
    return train_search_by_name(name)


def search_station(place):
    return station_search(place)


def search_schedule(train_number):
    return schedule_search(train_number)


def search_route(source, destination, limit=50):
    return route_search(source, destination, limit)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🚆 RAILWAY TOOLS TEST")
    print("=" * 60)

    print("\nDatabase:")

    try:
        print(database_status())
    except Exception as e:
        print("Database error:", e)

    print("\nTesting station search: Goa")

    try:
        results = station_search("Goa")

        for row in results[:10]:
            print(row)

        print("Total:", len(results))

    except Exception as e:
        print("Error:", e)

    print("\nTesting route: Madgaon → Pune")

    try:
        results = route_search("Madgaon", "Pune")

        for row in results:
            print(row)

        print("Total:", len(results))

    except Exception as e:
        print("Error:", e)

    print("\nTesting train stations: 12779")

    try:
        results = search_train_stations("12779")

        for row in results[:10]:
            print(row)

        print("Total:", len(results))

    except Exception as e:
        print("Error:", e)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)