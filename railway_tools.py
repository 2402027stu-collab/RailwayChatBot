# railway_tools.py
# ============================================================
# RailwayChatBot - Railway Database Tools
# ============================================================

import sqlite3
import os
import re


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Database", "railway.db")


# ============================================================
# STATE ALIASES
# ============================================================

STATE_ALIASES = {
    "goa": "Goa",
    "karnataka": "Karnataka",
    "maharashtra": "Maharashtra",
    "kerala": "Kerala",
    "tamil nadu": "Tamil Nadu",
    "tamilnadu": "Tamil Nadu",
    "andhra pradesh": "Andhra Pradesh",
    "telangana": "Telangana",
    "gujarat": "Gujarat",
    "rajasthan": "Rajasthan",
    "delhi": "Delhi",
    "uttar pradesh": "Uttar Pradesh",
    "up": "Uttar Pradesh",
    "madhya pradesh": "Madhya Pradesh",
    "mp": "Madhya Pradesh",
    "west bengal": "West Bengal",
    "odisha": "Odisha",
    "orissa": "Odisha",
    "bihar": "Bihar",
    "jharkhand": "Jharkhand",
    "punjab": "Punjab",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "uttarakhand": "Uttarakhand",
    "assam": "Assam",
    "chhattisgarh": "Chhattisgarh",
    "jammu and kashmir": "Jammu and Kashmir",
    "jammu & kashmir": "Jammu and Kashmir",
    "ladakh": "Ladakh",
}


# ============================================================
# CITY ALIASES
# ============================================================

CITY_ALIASES = {
    "mumbai": ["mumbai", "bombay"],
    "bombay": ["mumbai", "bombay"],

    "delhi": ["delhi", "new delhi"],
    "new delhi": ["delhi", "new delhi"],

    "pune": ["pune"],

    "bangalore": ["bangalore", "bengaluru"],
    "bengaluru": ["bangalore", "bengaluru"],

    "chennai": ["chennai", "madras"],
    "madras": ["chennai", "madras"],

    "kolkata": ["kolkata", "calcutta"],
    "calcutta": ["kolkata", "calcutta"],

    "hyderabad": ["hyderabad"],

    "ahmedabad": ["ahmedabad"],

    "jaipur": ["jaipur"],

    "lucknow": ["lucknow"],

    "nagpur": ["nagpur"],

    "surat": ["surat"],

    "vadodara": ["vadodara", "baroda"],
    "baroda": ["vadodara", "baroda"],

    "nashik": ["nashik", "nasik"],
    "nasik": ["nashik", "nasik"],

    "kochi": ["kochi", "cochin"],
    "cochin": ["kochi", "cochin"],

    "trivandrum": ["trivandrum", "thiruvananthapuram"],
    "thiruvananthapuram": ["trivandrum", "thiruvananthapuram"],

    "mysore": ["mysore", "mysuru"],
    "mysuru": ["mysore", "mysuru"],

    "visakhapatnam": ["visakhapatnam", "vizag"],
    "vizag": ["visakhapatnam", "vizag"],

    "bhubaneswar": ["bhubaneswar"],
    "patna": ["patna"],
    "ranchi": ["ranchi"],
    "indore": ["indore"],
    "bhopal": ["bhopal"],
    "chandigarh": ["chandigarh"],
    "amritsar": ["amritsar"],
    "varanasi": ["varanasi", "banaras"],
    "banaras": ["varanasi", "banaras"],
    "agra": ["agra"],
    "mathura": ["mathura"],

    # Goa cities / common railway locations
    "madgaon": ["madgaon", "madgaon junction"],
    "margao": ["madgaon", "madgaon junction"],
    "thivim": ["thivim"],
    "karmali": ["karmali"],
    "vasco": ["vasco da gama"],
    "vasco da gama": ["vasco da gama"],
    "canacona": ["canacona"],
    "pernem": ["pernem"],
    "verna": ["verna"],
}


# ============================================================
# CITY -> STATE
# ============================================================

CITY_STATES = {
    "mumbai": "Maharashtra",
    "bombay": "Maharashtra",
    "pune": "Maharashtra",

    "bangalore": "Karnataka",
    "bengaluru": "Karnataka",
    "mysore": "Karnataka",
    "mysuru": "Karnataka",

    "chennai": "Tamil Nadu",
    "madras": "Tamil Nadu",

    "hyderabad": "Telangana",

    "ahmedabad": "Gujarat",

    "jaipur": "Rajasthan",

    "lucknow": "Uttar Pradesh",

    "nagpur": "Maharashtra",

    "surat": "Gujarat",

    "vadodara": "Gujarat",
    "baroda": "Gujarat",

    "nashik": "Maharashtra",
    "nasik": "Maharashtra",

    "kochi": "Kerala",
    "cochin": "Kerala",

    "trivandrum": "Kerala",
    "thiruvananthapuram": "Kerala",

    "visakhapatnam": "Andhra Pradesh",
    "vizag": "Andhra Pradesh",

    "bhubaneswar": "Odisha",

    "patna": "Bihar",

    "ranchi": "Jharkhand",

    "indore": "Madhya Pradesh",

    "bhopal": "Madhya Pradesh",

    "chandigarh": "Chandigarh",

    "amritsar": "Punjab",

    "varanasi": "Uttar Pradesh",
    "banaras": "Uttar Pradesh",

    "agra": "Uttar Pradesh",

    "mathura": "Uttar Pradesh",

    "kolkata": "West Bengal",
    "calcutta": "West Bengal",

    "delhi": "Delhi",
    "new delhi": "Delhi",

    # Goa
    "madgaon": "Goa",
    "margao": "Goa",
    "thivim": "Goa",
    "karmali": "Goa",
    "vasco": "Goa",
    "vasco da gama": "Goa",
    "canacona": "Goa",
    "pernem": "Goa",
    "verna": "Goa",
}


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """Connect to railway database."""

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Railway database not found:\n{DB_PATH}"
        )

    return sqlite3.connect(DB_PATH)


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(value):
    """Normalize user input."""

    if value is None:
        return ""

    value = str(value).strip().lower()

    value = re.sub(r"[,\.\-_]+", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip()


# ============================================================
# TRAIN NUMBER CLEANER
# ============================================================

def clean_train_number(train_number):

    if train_number is None:
        return ""

    match = re.search(r"\d{3,6}", str(train_number))

    if match:
        return match.group()

    return str(train_number).strip()


# ============================================================
# RESOLVE PLACE
# ============================================================

def resolve_place(place):
    """
    Resolve:
        Station code
        Station name
        City
        State
    """

    original = str(place).strip()
    normalized = normalize_text(original)

    if not normalized:
        return {
            "query": original,
            "codes": [],
            "stations": [],
            "states": [],
            "matched_by": "none"
        }

    # --------------------------------------------------------
    # IMPORTANT:
    # STATE CHECK MUST COME BEFORE STATION CODE.
    #
    # Example:
    # Goa -> state Goa
    # Karnataka -> state Karnataka
    # Maharashtra -> state Maharashtra
    # --------------------------------------------------------

    state_name = STATE_ALIASES.get(normalized)

    conn = get_connection()

    try:

        cur = conn.cursor()

        # ====================================================
        # 1. STATE SEARCH
        # ====================================================

        if state_name:

            cur.execute(
                """
                SELECT code, name, state, zone, address
                FROM stations
                WHERE LOWER(TRIM(state)) = LOWER(?)
                ORDER BY name
                """,
                (state_name,)
            )

            rows = cur.fetchall()

            if rows:

                return {
                    "query": original,
                    "codes": list(
                        dict.fromkeys(row[0] for row in rows)
                    ),
                    "stations": [
                        {
                            "code": row[0],
                            "name": row[1],
                            "state": row[2],
                            "zone": row[3],
                            "address": row[4]
                        }
                        for row in rows
                    ],
                    "states": [state_name],
                    "matched_by": "state"
                }

        # ====================================================
        # 2. EXACT STATION CODE
        # ====================================================

        cur.execute(
            """
            SELECT code, name, state, zone, address
            FROM stations
            WHERE UPPER(TRIM(code)) = UPPER(?)
            """,
            (original,)
        )

        rows = cur.fetchall()

        if rows:

            return {
                "query": original,
                "codes": list(
                    dict.fromkeys(row[0] for row in rows)
                ),
                "stations": [
                    {
                        "code": row[0],
                        "name": row[1],
                        "state": row[2],
                        "zone": row[3],
                        "address": row[4]
                    }
                    for row in rows
                ],
                "states": list(
                    dict.fromkeys(row[2] for row in rows)
                ),
                "matched_by": "station_code"
            }

        # ====================================================
        # 3. EXACT STATION NAME
        # ====================================================

        cur.execute(
            """
            SELECT code, name, state, zone, address
            FROM stations
            WHERE LOWER(TRIM(name)) = ?
            """,
            (normalized,)
        )

        rows = cur.fetchall()

        if rows:

            return {
                "query": original,
                "codes": list(
                    dict.fromkeys(row[0] for row in rows)
                ),
                "stations": [
                    {
                        "code": row[0],
                        "name": row[1],
                        "state": row[2],
                        "zone": row[3],
                        "address": row[4]
                    }
                    for row in rows
                ],
                "states": list(
                    dict.fromkeys(row[2] for row in rows)
                ),
                "matched_by": "station_name"
            }

        # ====================================================
        # 4. CITY SEARCH
        # ====================================================

        aliases = CITY_ALIASES.get(normalized)

        if aliases:

            city_state = CITY_STATES.get(normalized)

            conditions = []
            params = []

            for alias in aliases:

                conditions.append(
                    "LOWER(name) LIKE ?"
                )

                params.append(f"%{alias}%")

            query = f"""
                SELECT code, name, state, zone, address
                FROM stations
                WHERE (
                    {" OR ".join(conditions)}
                )
            """

            if city_state:

                query += """
                    AND LOWER(state) = LOWER(?)
                """

                params.append(city_state)

            query += " ORDER BY name LIMIT 200"

            cur.execute(query, params)

            rows = cur.fetchall()

            if rows:

                return {
                    "query": original,
                    "codes": list(
                        dict.fromkeys(row[0] for row in rows)
                    ),
                    "stations": [
                        {
                            "code": row[0],
                            "name": row[1],
                            "state": row[2],
                            "zone": row[3],
                            "address": row[4]
                        }
                        for row in rows
                    ],
                    "states": list(
                        dict.fromkeys(row[2] for row in rows)
                    ),
                    "matched_by": "city"
                }

        # ====================================================
        # 5. PARTIAL STATION NAME
        # ====================================================

        cur.execute(
            """
            SELECT code, name, state, zone, address
            FROM stations
            WHERE LOWER(name) LIKE ?
            ORDER BY LENGTH(name)
            LIMIT 100
            """,
            (f"%{normalized}%",)
        )

        rows = cur.fetchall()

        if rows:

            return {
                "query": original,
                "codes": list(
                    dict.fromkeys(row[0] for row in rows)
                ),
                "stations": [
                    {
                        "code": row[0],
                        "name": row[1],
                        "state": row[2],
                        "zone": row[3],
                        "address": row[4]
                    }
                    for row in rows
                ],
                "states": list(
                    dict.fromkeys(row[2] for row in rows)
                ),
                "matched_by": "partial_station_name"
            }

        # ====================================================
        # NOTHING FOUND
        # ====================================================

        return {
            "query": original,
            "codes": [],
            "stations": [],
            "states": [],
            "matched_by": "none"
        }

    finally:

        conn.close()


# ============================================================
# TRAIN SEARCH
# ============================================================

def train_search(train_number):

    number = clean_train_number(train_number)

    if not number:
        return []

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                number,
                name,
                type,
                zone,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                duration_h,
                duration_m,
                distance,
                classes,
                sleeper,
                third_ac,
                second_ac,
                first_ac,
                chair_car,
                first_class,
                return_train
            FROM trains
            WHERE number = ?
            """,
            (number,)
        )

        rows = cur.fetchall()

        columns = [
            "number",
            "name",
            "type",
            "zone",
            "from_station_code",
            "from_station_name",
            "to_station_code",
            "to_station_name",
            "departure",
            "arrival",
            "duration_h",
            "duration_m",
            "distance",
            "classes",
            "sleeper",
            "third_ac",
            "second_ac",
            "first_ac",
            "chair_car",
            "first_class",
            "return_train"
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:

        conn.close()


# ============================================================
# TRAIN NAME SEARCH
# ============================================================

def train_search_by_name(name, limit=20):

    if not name:
        return []

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                number,
                name,
                type,
                zone,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                duration_h,
                duration_m,
                distance,
                classes
            FROM trains
            WHERE LOWER(name) LIKE ?
            ORDER BY number
            LIMIT ?
            """,
            (
                f"%{normalize_text(name)}%",
                limit
            )
        )

        rows = cur.fetchall()

        columns = [
            "number",
            "name",
            "type",
            "zone",
            "from_station_code",
            "from_station_name",
            "to_station_code",
            "to_station_name",
            "departure",
            "arrival",
            "duration_h",
            "duration_m",
            "distance",
            "classes"
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:

        conn.close()


# ============================================================
# STATION SEARCH
# ============================================================

def station_search(place):

    return resolve_place(place)


# ============================================================
# SCHEDULE SEARCH
# ============================================================

def schedule_search(train_number, limit=500):

    number = clean_train_number(train_number)

    if not number:
        return []

    conn = get_connection()

    try:

        cur = conn.cursor()

        cur.execute(
            """
            SELECT
                train_number,
                train_name,
                station_code,
                station_name,
                arrival,
                departure,
                day,
                id
            FROM schedules
            WHERE train_number = ?
            ORDER BY id
            LIMIT ?
            """,
            (number, limit)
        )

        rows = cur.fetchall()

        columns = [
            "train_number",
            "train_name",
            "station_code",
            "station_name",
            "arrival",
            "departure",
            "day",
            "id"
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:

        conn.close()


# ============================================================
# TRAIN STATIONS
# ============================================================

def search_train_stations(train_number):

    return schedule_search(train_number)


# ============================================================
# ROUTE SEARCH
# ============================================================

def route_search(source, destination, limit=50):
    """
    Search routes between:
        Station -> Station
        City -> City
        State -> State
        Station -> State
        State -> Station
        City -> State
        State -> City
    """

    source_result = resolve_place(source)
    destination_result = resolve_place(destination)

    source_codes = source_result["codes"]
    destination_codes = destination_result["codes"]

    # --------------------------------------------------------
    # Source not found
    # --------------------------------------------------------

    if not source_codes:

        return {
            "source": source,
            "destination": destination,
            "source_found": False,
            "destination_found": bool(destination_codes),
            "results": [],
            "count": 0,
            "message": f"Could not find source: {source}"
        }

    # --------------------------------------------------------
    # Destination not found
    # --------------------------------------------------------

    if not destination_codes:

        return {
            "source": source,
            "destination": destination,
            "source_found": True,
            "destination_found": False,
            "results": [],
            "count": 0,
            "message": f"Could not find destination: {destination}"
        }

    # SQLite safety
    source_codes = source_codes[:800]
    destination_codes = destination_codes[:800]

    conn = get_connection()

    try:

        cur = conn.cursor()

        source_placeholders = ",".join(
            "?" for _ in source_codes
        )

        destination_placeholders = ",".join(
            "?" for _ in destination_codes
        )

        query = f"""
            SELECT
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
                s2.day,

                s1.id,
                s2.id

            FROM schedules s1

            INNER JOIN schedules s2
                ON s1.train_number = s2.train_number

            WHERE s1.station_code IN ({source_placeholders})

              AND s2.station_code IN ({destination_placeholders})

              AND s1.id < s2.id

            ORDER BY
                s1.train_number,
                s1.id,
                s2.id
        """

        cur.execute(
            query,
            source_codes + destination_codes
        )

        rows = cur.fetchall()

        results = []

        seen_trains = set()

        for row in rows:

            train_number = str(row[0])

            if train_number in seen_trains:
                continue

            seen_trains.add(train_number)

            results.append(
                {
                    "train_number": row[0],
                    "train_name": row[1],

                    "source_code": row[2],
                    "source_station": row[3],
                    "source_arrival": row[4],
                    "source_departure": row[5],
                    "source_day": row[6],

                    "destination_code": row[7],
                    "destination_station": row[8],
                    "destination_arrival": row[9],
                    "destination_departure": row[10],
                    "destination_day": row[11]
                }
            )

            if len(results) >= limit:
                break

        return {
            "source": source,
            "destination": destination,

            "source_found": True,
            "destination_found": True,

            "source_matched_by":
                source_result["matched_by"],

            "destination_matched_by":
                destination_result["matched_by"],

            "source_station_count":
                len(source_codes),

            "destination_station_count":
                len(destination_codes),

            "results": results,
            "count": len(results)
        }

    finally:

        conn.close()


# ============================================================
# TRAINS FROM STATION / CITY / STATE
# ============================================================

def search_trains_from_station(place, limit=50):

    resolved = resolve_place(place)

    codes = resolved["codes"]

    if not codes:
        return []

    codes = codes[:800]

    conn = get_connection()

    try:

        cur = conn.cursor()

        placeholders = ",".join(
            "?" for _ in codes
        )

        query = f"""
            SELECT
                train_number,
                train_name,
                station_code,
                station_name,
                arrival,
                departure,
                day
            FROM schedules
            WHERE station_code IN ({placeholders})
            ORDER BY train_number
            LIMIT ?
        """

        cur.execute(
            query,
            codes + [limit]
        )

        rows = cur.fetchall()

        columns = [
            "train_number",
            "train_name",
            "station_code",
            "station_name",
            "arrival",
            "departure",
            "day"
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:

        conn.close()


# ============================================================
# TRAINS TO STATION / CITY / STATE
# ============================================================

def search_trains_to_station(place, limit=50):

    # Schedule database does not distinguish
    # "from" and "to" at an intermediate stop.
    # Therefore this returns trains reaching/stopping there.

    return search_trains_from_station(place, limit)


# ============================================================
# PASSING TRAINS
# ============================================================

def search_trains_passing_station(place, limit=50):

    return search_trains_from_station(place, limit)


# ============================================================
# TERMINATING TRAINS
# ============================================================

def search_trains_terminating_at(place, limit=50):

    resolved = resolve_place(place)

    codes = resolved["codes"]

    if not codes:
        return []

    codes = codes[:800]

    conn = get_connection()

    try:

        cur = conn.cursor()

        placeholders = ",".join(
            "?" for _ in codes
        )

        query = f"""
            SELECT
                number,
                name,
                type,
                zone,
                from_station_code,
                from_station_name,
                to_station_code,
                to_station_name,
                departure,
                arrival,
                distance
            FROM trains
            WHERE to_station_code IN ({placeholders})
            ORDER BY number
            LIMIT ?
        """

        cur.execute(
            query,
            codes + [limit]
        )

        rows = cur.fetchall()

        columns = [
            "number",
            "name",
            "type",
            "zone",
            "from_station_code",
            "from_station_name",
            "to_station_code",
            "to_station_name",
            "departure",
            "arrival",
            "distance"
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    finally:

        conn.close()


# ============================================================
# DATABASE STATUS
# ============================================================

def database_status():

    conn = get_connection()

    try:

        cur = conn.cursor()

        tables = {}

        for table in [
            "trains",
            "stations",
            "schedules"
        ]:

            cur.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            tables[table] = cur.fetchone()[0]

        return {
            "database": DB_PATH,
            "database_exists": os.path.exists(DB_PATH),
            "tables": tables
        }

    finally:

        conn.close()


# ============================================================
# COMPATIBILITY FUNCTIONS
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


def trains_from_station(place, limit=50):
    return search_trains_from_station(place, limit)


def trains_to_station(place, limit=50):
    return search_trains_to_station(place, limit)


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("RAILWAY TOOLS TEST")
    print("=" * 70)

    try:

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        status = database_status()

        print("\nDATABASE:")
        print(status["database"])

        print("\nDATABASE COUNTS:")

        for table, count in status["tables"].items():
            print(f"{table}: {count}")

        # ----------------------------------------------------
        # GOA
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("TEST: Goa")
        print("-" * 70)

        result = resolve_place("Goa")

        print("Matched by:", result["matched_by"])
        print("Stations:", len(result["codes"]))

        for station in result["stations"][:10]:

            print(
                station["code"],
                "|",
                station["name"],
                "|",
                station["state"]
            )

        # ----------------------------------------------------
        # MAHARASHTRA
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("TEST: Maharashtra")
        print("-" * 70)

        result = resolve_place("Maharashtra")

        print("Matched by:", result["matched_by"])
        print("Stations:", len(result["codes"]))

        for station in result["stations"][:10]:

            print(
                station["code"],
                "|",
                station["name"],
                "|",
                station["state"]
            )

        # ----------------------------------------------------
        # GOA -> MAHARASHTRA
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("TEST: Goa -> Maharashtra")
        print("-" * 70)

        result = route_search(
            "Goa",
            "Maharashtra",
            20
        )

        print("Source matched by:",
              result.get("source_matched_by"))

        print("Destination matched by:",
              result.get("destination_matched_by"))

        print("Results:",
              result.get("count", 0))

        for train in result.get("results", []):

            print(
                train["train_number"],
                "|",
                train["train_name"],
                "|",
                train["source_station"],
                "->",
                train["destination_station"]
            )

        # ----------------------------------------------------
        # MADGAON -> PUNE
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("TEST: Madgaon -> Pune")
        print("-" * 70)

        result = route_search(
            "Madgaon",
            "Pune",
            10
        )

        print("Results:",
              result.get("count", 0))

        for train in result.get("results", []):

            print(
                train["train_number"],
                "|",
                train["train_name"],
                "|",
                train["source_station"],
                "->",
                train["destination_station"]
            )

        # ----------------------------------------------------
        # THIVIM -> KARNATAKA
        # ----------------------------------------------------

        print("\n" + "-" * 70)
        print("TEST: Thivim -> Karnataka")
        print("-" * 70)

        result = route_search(
            "Thivim",
            "Karnataka",
            10
        )

        print("Results:",
              result.get("count", 0))

        for train in result.get("results", []):

            print(
                train["train_number"],
                "|",
                train["train_name"],
                "|",
                train["source_station"],
                "->",
                train["destination_station"]
            )

        print("\n" + "=" * 70)
        print("ALL TESTS COMPLETED")
        print("=" * 70)

    except Exception as e:

        print("\nERROR:")
        print(e)