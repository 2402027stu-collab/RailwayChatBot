import streamlit as st
import sqlite3
import pandas as pd

from city_mapping import get_station_codes


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Railway Assistant",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# DATABASE
# ============================================================

DB_PATH = "Database/railway.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0d1117;
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #11151d;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            135deg,
            #141a24,
            #17131d
        );
        border: 1px solid #293241;
        border-radius: 18px;
        padding: 45px;
        text-align: center;
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 30px;
        font-weight: 700;
        color: white;
    }

    .hero-subtitle {
        color: #9ca3af;
        margin-top: 8px;
    }

    /* Section title */
    .section-title {
        color: #d1d5db;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Result title */
    .result-title {
        font-size: 18px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    /* Status */
    .online {
        background-color: #13251d;
        border: 1px solid #214d39;
        border-radius: 20px;
        padding: 8px 15px;
        color: #7ee2ae;
        display: inline-block;
        font-size: 13px;
    }

    /* Hide Streamlit default menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:22px;
            font-weight:700;
            padding:10px 0;
        ">
            🚆 Railway Assistant
        </div>

        <div style="
            color:#9ca3af;
            font-size:13px;
            margin-bottom:25px;
        ">
            Indian Railway Information System
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    if st.button(
        "🔎 Train Search",
        use_container_width=True
    ):
        st.session_state.page = "Train Search"

    if st.button(
        "🗺️ Route Search",
        use_container_width=True
    ):
        st.session_state.page = "Route Search"

    if st.button(
        "📅 Train Schedule",
        use_container_width=True
    ):
        st.session_state.page = "Train Schedule"

    if st.button(
        "📍 Station Information",
        use_container_width=True
    ):
        st.session_state.page = "Station Information"

    st.divider()

    if st.button(
        "🏠 Home",
        use_container_width=True
    ):
        st.session_state.page = "Home"

    st.divider()

    st.markdown(
        """
        <div style="
            color:#7f8794;
            font-size:12px;
            line-height:1.8;
        ">
            <b>Railway Assistant</b><br>
            Powered by local railway database
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        """
        <div class="main-title">
            🚆 Indian Railway Assistant
        </div>

        <div class="subtitle">
            Trains • Routes • Stations • Schedules
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:

    st.markdown(
        """
        <div style="
            text-align:right;
            margin-top:10px;
        ">
            <span class="online">
                🟢 Railway Database Online
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# HOME
# ============================================================
def show_home():

    # Hero section
    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                Where would you like to go?
            </div>
            <div class="hero-subtitle">
                Ask about trains, stations, routes or schedules
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-title">
            QUICK SEARCH
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(
            "🚆\n\nTRAIN SEARCH",
            use_container_width=True
        ):
            st.session_state.page = "Train Search"
            st.rerun()

    with col2:
        if st.button(
            "🗺️\n\nROUTE SEARCH",
            use_container_width=True
        ):
            st.session_state.page = "Route Search"
            st.rerun()

    with col3:
        if st.button(
            "📅\n\nSCHEDULES",
            use_container_width=True
        ):
            st.session_state.page = "Train Schedule"
            st.rerun()

    with col4:
        if st.button(
            "📍\n\nSTATIONS",
            use_container_width=True
        ):
            st.session_state.page = "Station Information"
            st.rerun()
# ============================================================
# TRAIN SEARCH
# ============================================================

def show_train_search():

    st.header("🔎 Train Search")

    st.write(
        "Search for a train using its train number or name."
    )

    search_text = st.text_input(
        "Train Number or Train Name",
        placeholder="Example: 10103 or Mandovi"
    )

    if st.button(
        "🔍 Search Train",
        type="primary"
    ):

        if not search_text.strip():

            st.warning("Please enter a train number or train name.")
            return

        conn = get_connection()

        query = """
        SELECT
            number,
            name,
            from_station_name AS source_station,
            to_station_name AS destination_station,
            type,
            distance
        FROM trains
        WHERE
            CAST(number AS TEXT) LIKE ?
            OR LOWER(name) LIKE ?
        ORDER BY number
        """

        search_value = search_text.strip().lower()

        df = pd.read_sql(
            query,
            conn,
            params=(
                f"%{search_text.strip()}%",
                f"%{search_value}%"
            )
        )

        conn.close()

        if df.empty:

            st.error(
                f"No train found for '{search_text}'."
            )

        else:

            st.success(
                f"{len(df)} train(s) found."
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# ROUTE SEARCH
# ============================================================

def get_trains_between_route(
    source_codes,
    destination_codes
):

    conn = get_connection()

    query = """
    SELECT DISTINCT

        t.number AS number,

        t.name AS name,

        CASE
            WHEN s1.station_name IS NOT NULL
            THEN s1.station_name
            ELSE t.from_station_name
        END AS source_station,

        CASE
            WHEN s2.station_name IS NOT NULL
            THEN s2.station_name
            ELSE t.to_station_name
        END AS destination_station,

        t.type AS type,

        t.distance AS distance

    FROM schedules s1

    JOIN schedules s2

        ON s1.train_number = s2.train_number

    JOIN trains t

        ON CAST(t.number AS TEXT)
        = CAST(s1.train_number AS TEXT)

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

    if not results:

        return pd.DataFrame(
            columns=[
                "number",
                "name",
                "source_station",
                "destination_station",
                "type",
                "distance"
            ]
        )

    all_trains = pd.concat(
        results,
        ignore_index=True
    )

    all_trains = all_trains.drop_duplicates(
        subset=["number"]
    )

    all_trains = all_trains.sort_values(
        by="number"
    )

    return all_trains.reset_index(drop=True)


# ============================================================
# ROUTE SEARCH PAGE
# ============================================================

def show_route_search():

    st.header("🗺️ Route Search")

    st.write(
        "Find trains travelling between two cities."
    )

    col1, col2 = st.columns(2)

    with col1:

        source = st.text_input(
            "From",
            placeholder="Example: Mumbai"
        )

    with col2:

        destination = st.text_input(
            "To",
            placeholder="Example: Goa"
        )

    if st.button(
        "🔍 Find Trains",
        type="primary"
    ):

        if not source.strip() or not destination.strip():

            st.warning(
                "Please enter both source and destination."
            )

            return

        source_codes = get_station_codes(source)

        destination_codes = get_station_codes(destination)

        if not source_codes:

            st.error(
                f"No station mapping found for '{source}'."
            )

            return

        if not destination_codes:

            st.error(
                f"No station mapping found for '{destination}'."
            )

            return

        with st.spinner("Searching railway database..."):

            df = get_trains_between_route(
                source_codes,
                destination_codes
            )

        if df.empty:

            st.warning(
                f"No trains found from "
                f"{source.title()} to "
                f"{destination.title()}."
            )

        else:

            st.success(
                f"🚆 {len(df)} train(s) found from "
                f"{source.title()} to "
                f"{destination.title()}."
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# TRAIN SCHEDULE
# ============================================================

def show_train_schedule():

    st.header("📅 Train Schedule")

    st.write(
        "View the complete schedule of a train."
    )

    train_number = st.text_input(
        "Enter Train Number",
        placeholder="Example: 10103"
    )

    if st.button(
        "📅 View Schedule",
        type="primary"
    ):

        if not train_number.strip():

            st.warning(
                "Please enter a train number."
            )

            return

        conn = get_connection()

        train_query = """
        SELECT
            number,
            name,
            from_station_name AS source_station,
            to_station_name AS destination_station,
            type,
            distance
        FROM trains
        WHERE CAST(number AS TEXT) = ?
        """

        train_df = pd.read_sql(
            train_query,
            conn,
            params=(train_number.strip(),)
        )

        if train_df.empty:

            conn.close()

            st.error(
                f"Train {train_number} was not found."
            )

            return

        st.subheader(
            f"🚆 {train_df.iloc[0]['number']} - "
            f"{train_df.iloc[0]['name']}"
        )

        schedule_query = """
        SELECT

            id,

            station_code,

            station_name,

            arrival,

            departure,

            day

        FROM schedules

        WHERE CAST(train_number AS TEXT) = ?

        ORDER BY id
        """

        schedule_df = pd.read_sql(
            schedule_query,
            conn,
            params=(train_number.strip(),)
        )

        conn.close()

        if schedule_df.empty:

            st.warning(
                "No schedule data found for this train."
            )

        else:

            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# STATION INFORMATION
# ============================================================

def show_station_information():

    st.header("📍 Station Information")

    st.write(
        "Search for a railway station using its station code or name."
    )

    search_station = st.text_input(
        "Station Code or Station Name",
        placeholder="Example: MAO or Madgaon"
    )

    if st.button(
        "🔍 Search Station",
        type="primary"
    ):

        if not search_station.strip():

            st.warning(
                "Please enter a station code or name."
            )

            return

        conn = get_connection()

        query = """
        SELECT
            code,
            name,
            state,
            address
        FROM stations
        WHERE
            LOWER(code) = ?
            OR LOWER(name) LIKE ?
        ORDER BY name
        """

        value = search_station.strip().lower()

        df = pd.read_sql(
            query,
            conn,
            params=(
                value,
                f"%{value}%"
            )
        )

        conn.close()

        if df.empty:

            st.error(
                f"No station found for '{search_station}'."
            )

        else:

            st.success(
                f"{len(df)} station(s) found."
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "Home":

    show_home()

elif st.session_state.page == "Train Search":

    show_train_search()

elif st.session_state.page == "Route Search":

    show_route_search()

elif st.session_state.page == "Train Schedule":

    show_train_schedule()

elif st.session_state.page == "Station Information":

    show_station_information()