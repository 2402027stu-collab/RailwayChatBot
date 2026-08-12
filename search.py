import sqlite3
import pandas as pd


# ==========================================
# Search Train by Number
# ==========================================

def get_train_by_number(train_number):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT *
    FROM trains
    WHERE number = ?
    """

    df = pd.read_sql(query, conn, params=(train_number,))

    conn.close()

    return df


# ==========================================
# Search Train by Name
# ==========================================

def get_train_by_name(train_name):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT *
    FROM trains
    WHERE name LIKE ?
    """

    df = pd.read_sql(query, conn, params=(f"%{train_name}%",))

    conn.close()

    return df


# ==========================================
# Search Station
# ==========================================

def get_station(station_code):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT *
    FROM stations
    WHERE code = ?
    """

    df = pd.read_sql(query, conn, params=(station_code.upper(),))

    conn.close()

    return df

# ==========================================
# Search Stations by City Name
# ==========================================

def get_station_codes(city):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT
        code,
        name,
        state
    FROM stations
    WHERE UPPER(name) LIKE UPPER(?)
       OR UPPER(address) LIKE UPPER(?)
    """

    df = pd.read_sql(
        query,
        conn,
        params=(f"%{city}%", f"%{city}%")
    )

    conn.close()

    return df

# ==========================================
# Get Station Codes by City/State
# ==========================================

def get_station_codes(city):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT DISTINCT
        code,
        name,
        state,
        address
    FROM stations
    WHERE
          UPPER(state) LIKE ?
       OR UPPER(address) LIKE ?
       OR UPPER(name) LIKE ?
    ORDER BY name
    """

    keyword = f"%{city.upper()}%"

    df = pd.read_sql(
        query,
        conn,
        params=(
            keyword,
            keyword,
            keyword
        )
    )

    conn.close()

    return df

# ==========================================
# Search Schedule
# ==========================================

def get_schedule(train_number):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT *
    FROM schedules
    WHERE train_number = ?
    """

    df = pd.read_sql(query, conn, params=(train_number,))

    conn.close()

    return df

def get_trains_between(source_list, destination_list):

    conn = sqlite3.connect("Database/railway.db")

    all_trains = pd.DataFrame()

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
        type,
        distance
    FROM trains
    WHERE from_station_code = ?
      AND to_station_code = ?
    """

    for source in source_list:

        for destination in destination_list:

            df = pd.read_sql(
                query,
                conn,
                params=(source, destination)
            )

            if len(df) > 0:
                all_trains = pd.concat([all_trains, df])

    conn.close()

    all_trains = all_trains.drop_duplicates()

    return all_trains


# ==========================================
# Find trains between two stations/cities
# ==========================================

def get_trains_between_route(source_codes, destination_codes):

    conn = sqlite3.connect("Database/railway.db")

    query = """
    SELECT DISTINCT
        t.number AS number,
        t.name AS name,
        t.from_station_name AS source_station,
        t.to_station_name AS destination_station,
        t.type AS type,
        t.distance AS distance

    FROM schedules s1

    JOIN schedules s2
        ON s1.train_number = s2.train_number

    JOIN trains t
        ON CAST(t.number AS TEXT) = CAST(s1.train_number AS TEXT)

    WHERE
        s1.station_code = ?
        AND s2.station_code = ?
        AND s1.id < s2.id
    """

    results = []

    for source in source_codes:

        for destination in destination_codes:

            df = pd.read_sql(
                query,
                conn,
                params=(source, destination)
            )

            if not df.empty:
                results.append(df)

    conn.close()

    # Nothing found
    if not results:
        return pd.DataFrame(columns=[
            "number",
            "name",
            "source_station",
            "destination_station",
            "type",
            "distance"
        ])

    # Combine results
    all_trains = pd.concat(
        results,
        ignore_index=True
    )

    # Remove duplicate trains
    all_trains = all_trains.drop_duplicates(
        subset=["number"]
    )

    # Sort
    all_trains = all_trains.sort_values(
        by="number"
    )

    return all_trains.reset_index(drop=True)
    # ------------------------------------------
    # NO TRAINS FOUND
    # ------------------------------------------

    if len(results) == 0:

        return pd.DataFrame(columns=[
            "number",
            "name",
            "source_station",
            "destination_station",
            "type",
            "distance"
        ])

    # ------------------------------------------
    # COMBINE RESULTS
    # ------------------------------------------

    all_trains = pd.concat(
        results,
        ignore_index=True
    )

    # ------------------------------------------
    # REMOVE DUPLICATES
    # ------------------------------------------

    all_trains = all_trains.drop_duplicates(
        subset=["number"]
    )

    # ------------------------------------------
    # SORT
    # ------------------------------------------

    all_trains = all_trains.sort_values(
        by="number"
    )

    return all_trains.reset_index(drop=True)

# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    print("========== TRAIN NUMBER ==========")
    print(get_train_by_number("04601"))

    print("\n========== TRAIN NAME ==========")
    print(get_train_by_name("Jammu"))

    print("\n========== STATION ==========")
    print(get_station("BDHL"))

    print("\n========== SCHEDULE ==========")
    print(get_schedule("04601"))

    print("\n========== TRAINS BETWEEN ==========")
    print(get_trains_between("JAT", "UHP"))

    print(get_trains_between(["MAO", "THVM", "VSG"], ["CSTM", "MMCT", "LTT", "BDTS", "DR"]))