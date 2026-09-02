import sqlite3
import pandas as pd
import os
import re


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "Database",
    "railway.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create a connection to the railway database.
    """

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Railway database not found:\n{DB_PATH}"
        )

    return sqlite3.connect(DB_PATH)


# ============================================================
# COMMON TRAIN COLUMNS
# ============================================================

TRAIN_COLUMNS = """
    number,
    name,
    from_station_code,
    from_station_name,
    to_station_code,
    to_station_name,
    departure,
    arrival,
    distance,
    duration_h,
    duration_m,
    type,
    zone
"""


# ============================================================
# CLEAN USER INPUT
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    value = str(value).strip()

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


# ============================================================
# GET ALL STATES
# ============================================================

def get_states():

    conn = get_connection()

    try:

        query = """
        SELECT DISTINCT state
        FROM stations
        WHERE state IS NOT NULL
        AND TRIM(state) != ''
        ORDER BY state
        """

        df = pd.read_sql_query(
            query,
            conn
        )

        return df["state"].tolist()

    finally:
        conn.close()


# ============================================================
# FIND STATE
# ============================================================

def find_state(search_text):

    search_text = clean_text(
        search_text
    ).lower()

    if not search_text:
        return None

    states = get_states()

    # Exact match
    for state in states:

        if state.lower() == search_text:
            return state

    # Partial match
    for state in states:

        if search_text in state.lower():
            return state

    return None


# ============================================================
# SEARCH STATIONS
# ============================================================

def find_stations(search_text):

    search_text = clean_text(
        search_text
    )

    if not search_text:
        return pd.DataFrame()

    conn = get_connection()

    try:

        value = f"%{search_text.lower()}%"

        query = """
        SELECT
            state,
            code,
            name,
            zone,
            address
        FROM stations
        WHERE
            LOWER(name) LIKE ?
            OR LOWER(code) LIKE ?
            OR LOWER(state) LIKE ?
            OR LOWER(address) LIKE ?
        ORDER BY
            CASE
                WHEN LOWER(name) = ? THEN 0
                WHEN LOWER(code) = ? THEN 1
                ELSE 2
            END,
            name
        LIMIT 50
        """

        exact = search_text.lower()

        return pd.read_sql_query(
            query,
            conn,
            params=[
                value,
                value,
                value,
                value,
                exact,
                exact
            ]
        )

    finally:
        conn.close()


# ============================================================
# GET STATIONS IN A STATE
# ============================================================

def get_state_stations(state):

    state = clean_text(state)

    conn = get_connection()

    try:

        query = """
        SELECT
            state,
            code,
            name,
            zone,
            address
        FROM stations
        WHERE LOWER(state) = ?
        ORDER BY name
        """

        return pd.read_sql_query(
            query,
            conn,
            params=[
                state.lower()
            ]
        )

    finally:
        conn.close()


# ============================================================
# RESOLVE LOCATION
#
# A location can be:
#
# 1. State
# 2. Station
# 3. Station code
# 4. City/address text
# ============================================================

def resolve_location(location):

    location = clean_text(
        location
    )

    if not location:
        return {
            "type": "unknown",
            "name": "",
            "stations": pd.DataFrame()
        }

    # --------------------------------------------------------
    # FIRST: CHECK STATE
    # --------------------------------------------------------

    state = find_state(location)

    if state:

        stations = get_state_stations(
            state
        )

        return {
            "type": "state",
            "name": state,
            "stations": stations
        }

    # --------------------------------------------------------
    # SECOND: CHECK STATION / CITY
    # --------------------------------------------------------

    stations = find_stations(
        location
    )

    if not stations.empty:

        return {
            "type": "station",
            "name": location,
            "stations": stations
        }

    # --------------------------------------------------------
    # NOTHING FOUND
    # --------------------------------------------------------

    return {
        "type": "unknown",
        "name": location,
        "stations": pd.DataFrame()
    }


# ============================================================
# SEARCH TRAIN BY NUMBER OR NAME
# ============================================================

def search_train(search_text):

    search_text = clean_text(
        search_text
    )

    if not search_text:

        return {
            "status": "error",
            "message": (
                "Please provide a train number "
                "or train name."
            )
        }

    conn = get_connection()

    try:

        value = f"%{search_text.lower()}%"

        query = f"""
        SELECT
            {TRAIN_COLUMNS}
        FROM trains
        WHERE
            LOWER(number) LIKE ?
            OR LOWER(name) LIKE ?
        LIMIT 20
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=[
                value,
                value
            ]
        )

        if df.empty:

            return {
                "status": "not_found",
                "message": (
                    f"No train found for "
                    f"'{search_text}'."
                )
            }

        return {
            "status": "success",
            "trains": df.to_dict(
                orient="records"
            )
        }

    finally:
        conn.close()


# ============================================================
# SEARCH ROUTE
#
# Handles:
#
# Mumbai -> Goa
# Thivim -> Karnataka
# Goa -> Mumbai
# Karnataka -> Goa
# Mumbai -> Madgaon
# ============================================================

def search_route(source, destination):

    source = clean_text(source)
    destination = clean_text(destination)

    if not source or not destination:

        return {
            "status": "error",
            "message": (
                "Both source and destination "
                "are required."
            )
        }

    # --------------------------------------------------------
    # RESOLVE SOURCE
    # --------------------------------------------------------

    source_info = resolve_location(
        source
    )

    # --------------------------------------------------------
    # RESOLVE DESTINATION
    # --------------------------------------------------------

    destination_info = resolve_location(
        destination
    )

    # --------------------------------------------------------
    # SOURCE NOT FOUND
    # --------------------------------------------------------

    if source_info["type"] == "unknown":

        return {
            "status": "not_found",
            "message": (
                f"I couldn't find a railway station "
                f"or state matching '{source}'."
            )
        }

    # --------------------------------------------------------
    # DESTINATION NOT FOUND
    # --------------------------------------------------------

    if destination_info["type"] == "unknown":

        return {
            "status": "not_found",
            "message": (
                f"I couldn't find a railway station "
                f"or state matching '{destination}'."
            )
        }

    source_stations = source_info[
        "stations"
    ]

    destination_stations = destination_info[
        "stations"
    ]

    if source_stations.empty:

        return {
            "status": "not_found",
            "message": (
                f"No stations found for {source}."
            )
        }

    if destination_stations.empty:

        return {
            "status": "not_found",
            "message": (
                f"No stations found for {destination}."
            )
        }

    source_codes = (
        source_stations[
            "code"
        ]
        .dropna()
        .astype(str)
        .tolist()
    )

    destination_codes = (
        destination_stations[
            "code"
        ]
        .dropna()
        .astype(str)
        .tolist()
    )

    if not source_codes:

        return {
            "status": "not_found",
            "message": (
                f"No valid railway codes found "
                f"for {source}."
            )
        }

    if not destination_codes:

        return {
            "status": "not_found",
            "message": (
                f"No valid railway codes found "
                f"for {destination}."
            )
        }

    # --------------------------------------------------------
    # SEARCH TRAINS
    # --------------------------------------------------------

    conn = get_connection()

    try:

        source_placeholders = ",".join(
            ["?"] * len(source_codes)
        )

        destination_placeholders = ",".join(
            ["?"] * len(destination_codes)
        )

        query = f"""
        SELECT
            {TRAIN_COLUMNS}
        FROM trains
        WHERE
            from_station_code IN
            ({source_placeholders})
            AND
            to_station_code IN
            ({destination_placeholders})
        ORDER BY departure
        LIMIT 20
        """

        params = (
            source_codes +
            destination_codes
        )

        df = pd.read_sql_query(
            query,
            conn,
            params=params
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if not df.empty:

            return {
                "status": "success",
                "source": source,
                "destination": destination,
                "source_type":
                    source_info["type"],
                "destination_type":
                    destination_info["type"],
                "source_stations":
                    source_stations.to_dict(
                        orient="records"
                    ),
                "destination_stations":
                    destination_stations.to_dict(
                        orient="records"
                    ),
                "trains":
                    df.to_dict(
                        orient="records"
                    )
            }

        # ----------------------------------------------------
        # NO DIRECT TRAINS
        # ----------------------------------------------------

        return {
            "status": "not_found",
            "message": (
                f"No direct trains found from "
                f"{source} to {destination}."
            ),
            "source": source,
            "destination": destination,
            "source_stations":
                source_stations.to_dict(
                    orient="records"
                ),
            "destination_stations":
                destination_stations.to_dict(
                    orient="records"
                )
        }

    finally:
        conn.close()


# ============================================================
# TRAINS TO LOCATION
#
# Example:
#
# Which trains go to Goa?
# Which trains go to Karnataka?
# Which trains go to Madgaon?
# ============================================================

def search_trains_to_station(location):

    location = clean_text(
        location
    )

    if not location:

        return {
            "status": "error",
            "message": (
                "Please provide a destination."
            )
        }

    info = resolve_location(
        location
    )

    if info["type"] == "unknown":

        return {
            "status": "not_found",
            "message": (
                f"I couldn't find a station "
                f"or state named '{location}'."
            )
        }

    stations = info["stations"]

    codes = (
        stations["code"]
        .dropna()
        .astype(str)
        .tolist()
    )

    if not codes:

        return {
            "status": "not_found",
            "message": (
                f"No railway stations found "
                f"for {location}."
            )
        }

    conn = get_connection()

    try:

        placeholders = ",".join(
            ["?"] * len(codes)
        )

        query = f"""
        SELECT
            {TRAIN_COLUMNS}
        FROM trains
        WHERE
            to_station_code IN
            ({placeholders})
        ORDER BY departure
        LIMIT 20
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=codes
        )

        if df.empty:

            return {
                "status": "not_found",
                "message": (
                    f"No trains found going "
                    f"to {location}."
                ),
                "destination_stations":
                    stations.to_dict(
                        orient="records"
                    )
            }

        return {
            "status": "success",
            "destination": location,
            "destination_type":
                info["type"],
            "destination_stations":
                stations.to_dict(
                    orient="records"
                ),
            "trains":
                df.to_dict(
                    orient="records"
                )
        }

    finally:
        conn.close()


# ============================================================
# TRAINS FROM LOCATION
#
# Example:
#
# Which trains start from Goa?
# Which trains start from Mumbai?
# ============================================================

def search_trains_from_station(location):

    location = clean_text(
        location
    )

    if not location:

        return {
            "status": "error",
            "message": (
                "Please provide a source."
            )
        }

    info = resolve_location(
        location
    )

    if info["type"] == "unknown":

        return {
            "status": "not_found",
            "message": (
                f"I couldn't find a station "
                f"or state named '{location}'."
            )
        }

    stations = info["stations"]

    codes = (
        stations["code"]
        .dropna()
        .astype(str)
        .tolist()
    )

    if not codes:

        return {
            "status": "not_found",
            "message": (
                f"No railway stations found "
                f"for {location}."
            )
        }

    conn = get_connection()

    try:

        placeholders = ",".join(
            ["?"] * len(codes)
        )

        query = f"""
        SELECT
            {TRAIN_COLUMNS}
        FROM trains
        WHERE
            from_station_code IN
            ({placeholders})
        ORDER BY departure
        LIMIT 100
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=codes
        )

        if df.empty:

            return {
                "status": "not_found",
                "message": (
                    f"No trains found starting "
                    f"from {location}."
                ),
                "source_stations":
                    stations.to_dict(
                        orient="records"
                    )
            }

        return {
            "status": "success",
            "source": location,
            "source_type":
                info["type"],
            "source_stations":
                stations.to_dict(
                    orient="records"
                ),
            "trains":
                df.to_dict(
                    orient="records"
                )
        }

    finally:
        conn.close()


# ============================================================
# SEARCH STATION INFORMATION
# ============================================================

def search_station(search_text):

    search_text = clean_text(
        search_text
    )

    if not search_text:

        return {
            "status": "error",
            "message": (
                "Please provide a station "
                "name or code."
            )
        }

    df = find_stations(
        search_text
    )

    if df.empty:

        return {
            "status": "not_found",
            "message": (
                f"No station found for "
                f"'{search_text}'."
            )
        }

    return {
        "status": "success",
        "stations":
            df.to_dict(
                orient="records"
            )
    }


# ============================================================
# TRAIN SCHEDULE
# ============================================================

def search_schedule(train_number):

    train_number = clean_text(
        train_number
    )

    if not train_number:

        return {
            "status": "error",
            "message": (
                "Please provide a train number."
            )
        }

    conn = get_connection()

    try:

        query = """
        SELECT
            arrival,
            day,
            train_name,
            station_name,
            station_code,
            train_number,
            departure
        FROM schedules
        WHERE train_number = ?
        ORDER BY id
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=[
                train_number
            ]
        )

        if df.empty:

            return {
                "status": "not_found",
                "message": (
                    f"No schedule found for "
                    f"train {train_number}."
                )
            }

        return {
            "status": "success",
            "train_number":
                train_number,
            "schedule":
                df.to_dict(
                    orient="records"
                )
        }

    finally:
        conn.close()


# ============================================================
# TRAIN STOPPING STATIONS
# ============================================================

def search_train_stations(train_number):

    train_number = clean_text(
        train_number
    )

    if not train_number:

        return {
            "status": "error",
            "message": (
                "Please provide a train number."
            )
        }

    conn = get_connection()

    try:

        query = """
        SELECT
            day,
            station_name,
            station_code,
            arrival,
            departure,
            train_number
        FROM schedules
        WHERE train_number = ?
        ORDER BY id
        """

        df = pd.read_sql_query(
            query,
            conn,
            params=[
                train_number
            ]
        )

        if df.empty:

            return {
                "status": "not_found",
                "message": (
                    f"No stopping station "
                    f"information found for "
                    f"train {train_number}."
                )
            }

        return {
            "status": "success",
            "train_number":
                train_number,
            "stations":
                df.to_dict(
                    orient="records"
                )
        }

    finally:
        conn.close()


# ============================================================
# DATABASE STATUS
# ============================================================

def database_status():

    conn = get_connection()

    try:

        result = {}

        tables = [
            "trains",
            "stations",
            "schedules"
        ]

        for table in tables:

            query = f"""
            SELECT COUNT(*) AS count
            FROM {table}
            """

            df = pd.read_sql_query(
                query,
                conn
            )

            result[table] = int(
                df.iloc[0]["count"]
            )

        return result

    finally:
        conn.close()


# ============================================================
# DATABASE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("🚆 RAILWAY DATABASE TOOLS TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    print("\n📊 DATABASE STATUS")

    try:

        status = database_status()

        for table, count in status.items():

            print(
                f"{table:<15}: {count}"
            )

    except Exception as e:

        print("❌ Error:")
        print(e)

    # --------------------------------------------------------
    # GOA
    # --------------------------------------------------------

    print("\n🌴 GOA STATIONS")

    try:

        result = search_trains_to_station(
            "Goa"
        )

        if result["status"] == "success":

            print(
                "Goa stations:",
                len(
                    result[
                        "destination_stations"
                    ]
                )
            )

            print(
                "Trains:",
                len(
                    result["trains"]
                )
            )

        else:

            print(
                result["message"]
            )

    except Exception as e:

        print("❌ Goa error:")
        print(e)

    # --------------------------------------------------------
    # THIVIM -> KARNATAKA
    # --------------------------------------------------------

    print("\n🛤️ THIVIM -> KARNATAKA")

    try:

        result = search_route(
            "Thivim",
            "Karnataka"
        )

        if result["status"] == "success":

            print(
                "Trains found:",
                len(
                    result["trains"]
                )
            )

            for train in result["trains"][:10]:

                print(
                    train["number"],
                    "-",
                    train["name"],
                    "|",
                    train[
                        "from_station_name"
                    ],
                    "->",
                    train[
                        "to_station_name"
                    ]
                )

        else:

            print(
                result["message"]
            )

    except Exception as e:

        print("❌ Route error:")
        print(e)

    # --------------------------------------------------------
    # KARMALI
    # --------------------------------------------------------

    print("\n📍 KARMALI STATION")

    try:

        result = search_station(
            "Karmali"
        )

        print(
            result
        )

    except Exception as e:

        print("❌ Station error:")
        print(e)

    # --------------------------------------------------------
    # TRAIN 04601
    # --------------------------------------------------------

    print("\n🚆 TRAIN 04601")

    try:

        result = search_train(
            "04601"
        )

        print(
            result
        )

    except Exception as e:

        print("❌ Train error:")
        print(e)

    print("\n" + "=" * 70)
    print("✅ DATABASE TOOL TEST COMPLETED")
    print("=" * 70)