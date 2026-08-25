import streamlit as st
import sqlite3
import pandas as pd

from city_mapping import get_station_codes


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Indian Railway Assistant",
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
# PREMIUM UI / CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       GLOBAL
       ========================= */

    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(239, 68, 68, 0.10), transparent 28%),
            radial-gradient(circle at 10% 20%, rgba(37, 99, 235, 0.08), transparent 25%),
            #090d14;
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #101620 0%, #0b1018 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.12);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.3rem;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .sidebar-brand {
        padding: 8px 4px 18px 4px;
    }

    .sidebar-logo {
        width: 48px;
        height: 48px;
        border-radius: 15px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #ef4444, #f97316);
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.22);
        font-size: 25px;
        margin-bottom: 10px;
    }

    .sidebar-title {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.3px;
    }

    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
        line-height: 1.5;
    }

    .sidebar-label {
        color: #64748b;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 22px 0 8px 3px;
    }

    .sidebar-footer {
        color: #64748b;
        font-size: 11px;
        line-height: 1.7;
        padding: 12px 3px;
    }

    /* Sidebar Streamlit buttons */
    section[data-testid="stSidebar"] .stButton > button {
        min-height: 44px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.025);
        color: #e2e8f0;
        font-weight: 650;
        text-align: left;
        transition: all 0.2s ease;
        box-shadow: none;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: rgba(239, 68, 68, 0.45);
        background: rgba(239, 68, 68, 0.09);
        transform: translateX(3px);
    }

    /* =========================
       HEADER
       ========================= */

    .top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
        padding: 6px 0 18px 0;
    }

    .brand-row {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-icon {
        width: 54px;
        height: 54px;
        border-radius: 17px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #ef4444, #f97316);
        font-size: 28px;
        box-shadow: 0 12px 35px rgba(239, 68, 68, 0.20);
    }

    .main-title {
        font-size: 29px;
        line-height: 1.1;
        font-weight: 850;
        letter-spacing: -0.8px;
        color: #f8fafc;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 6px;
    }

    .online {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        padding: 9px 14px;
        border-radius: 999px;
        background: rgba(34, 197, 94, 0.08);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #86efac;
        font-size: 12px;
        font-weight: 700;
        white-space: nowrap;
    }

    .online-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22c55e;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.8);
    }

    /* =========================
       HOME HERO
       ========================= */

    .hero {
        position: relative;
        overflow: hidden;
        min-height: 245px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        border-radius: 24px;
        padding: 45px 25px;
        margin: 12px 0 30px 0;
        border: 1px solid rgba(148, 163, 184, 0.13);
        background:
            radial-gradient(circle at 20% 0%, rgba(239, 68, 68, 0.20), transparent 34%),
            radial-gradient(circle at 90% 100%, rgba(37, 99, 235, 0.15), transparent 38%),
            linear-gradient(135deg, #151c27, #11151f 55%, #18151d);
        box-shadow:
            0 20px 60px rgba(0, 0, 0, 0.28),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .hero::before {
        content: "🚆";
        position: absolute;
        right: 8%;
        top: 12%;
        font-size: 70px;
        opacity: 0.07;
        transform: rotate(-8deg);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 240px;
        height: 240px;
        border-radius: 50%;
        border: 1px solid rgba(239, 68, 68, 0.12);
        right: -80px;
        bottom: -130px;
    }

    .hero-badge {
        position: relative;
        z-index: 1;
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        background: rgba(239, 68, 68, 0.10);
        border: 1px solid rgba(239, 68, 68, 0.20);
        color: #fca5a5;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 14px;
    }

    .hero-title {
        position: relative;
        z-index: 1;
        font-size: clamp(27px, 3vw, 40px);
        font-weight: 850;
        letter-spacing: -1px;
        color: #ffffff;
    }

    .hero-subtitle {
        position: relative;
        z-index: 1;
        color: #94a3b8;
        margin-top: 10px;
        font-size: 14px;
    }

    .section-title {
        color: #cbd5e1;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 1.7px;
        margin: 5px 0 12px 2px;
    }

    /* =========================
       QUICK SEARCH BUTTONS
       ========================= */

    .quick-card {
        text-align: center;
        margin-bottom: 8px;
    }

    .quick-icon {
        font-size: 27px;
        margin-bottom: 5px;
    }

    /* Main buttons */
    .stButton > button {
        border-radius: 13px;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: linear-gradient(180deg, #171d28, #111721);
        color: #e2e8f0;
        min-height: 48px;
        font-weight: 700;
        transition: all 0.2s ease;
        box-shadow: 0 8px 25px rgba(0,0,0,0.10);
    }

    .stButton > button:hover {
        border-color: rgba(239, 68, 68, 0.48);
        background: linear-gradient(180deg, #202631, #151a24);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.22);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        border-color: #ef4444;
        color: white;
        box-shadow: 0 10px 28px rgba(239, 68, 68, 0.20);
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #f05252, #e03131);
        border-color: #f87171;
    }

    /* =========================
       PAGE CARDS / INPUTS
       ========================= */

    .page-heading {
        margin: 8px 0 4px 0;
        font-size: 28px;
        font-weight: 850;
        letter-spacing: -0.6px;
    }

    .page-description {
        color: #94a3b8;
        margin-bottom: 22px;
        font-size: 14px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.13);
        background: rgba(17, 23, 33, 0.75);
        box-shadow: 0 12px 35px rgba(0,0,0,0.14);
        margin-bottom: 18px;
    }

    .stTextInput > div > div > input {
        background: #111721;
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 12px;
        min-height: 48px;
    }

    .stTextInput > div > div > input:focus {
        border-color: #ef4444;
        box-shadow: 0 0 0 1px rgba(239, 68, 68, 0.25);
    }

    label {
        color: #cbd5e1 !important;
        font-weight: 650 !important;
    }

    /* =========================
       DATAFRAME / TABLE
       ========================= */

    [data-testid="stDataFrame"] {
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(0,0,0,0.14);
    }

    .result-title {
        font-size: 17px;
        font-weight: 750;
        margin: 22px 0 10px 0;
    }

    /* =========================
       INFO / STATUS
       ========================= */

    .metric-strip {
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin: 10px 0 20px 0;
    }

    .mini-metric {
        padding: 12px 15px;
        border-radius: 13px;
        border: 1px solid rgba(148, 163, 184, 0.12);
        background: #111721;
        min-width: 130px;
    }

    .mini-metric-value {
        font-size: 19px;
        font-weight: 800;
        color: #f8fafc;
    }

    .mini-metric-label {
        color: #64748b;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 3px;
    }

    /* =========================
       DIVIDER
       ========================= */

    hr {
        border-color: rgba(148, 163, 184, 0.12) !important;
    }

    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 800px) {
        .main .block-container {
            padding: 1rem 0.8rem 2rem 0.8rem;
        }

        .main-title {
            font-size: 23px;
        }

        .hero {
            min-height: 210px;
            padding: 30px 18px;
        }

        .hero-title {
            font-size: 27px;
        }
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
        <div class="sidebar-brand">
            <div class="sidebar-logo">🚆</div>
            <div class="sidebar-title">Railway Assistant</div>
            <div class="sidebar-subtitle">
                Indian Railway Information System
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="sidebar-label">NAVIGATION</div>', unsafe_allow_html=True)

    if st.button("🔎  Train Search", use_container_width=True):
        st.session_state.page = "Train Search"
        st.rerun()

    if st.button("🗺️  Route Search", use_container_width=True):
        st.session_state.page = "Route Search"
        st.rerun()

    if st.button("📅  Train Schedule", use_container_width=True):
        st.session_state.page = "Train Schedule"
        st.rerun()

    if st.button("📍  Station Information", use_container_width=True):
        st.session_state.page = "Station Information"
        st.rerun()

    st.markdown('<div class="sidebar-label">QUICK ACCESS</div>', unsafe_allow_html=True)

    if st.button("🏠  Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    st.markdown(
        """
        <div class="sidebar-footer">
            <b>Railway Assistant</b><br>
            Search trains, routes, stations and schedules.<br><br>
            <span style="color:#475569;">Powered by local railway database</span>
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
        <div class="top-header">
            <div class="brand-row">
                <div class="brand-icon">🚆</div>
                <div>
                    <div class="main-title">Indian Railway Assistant</div>
                    <div class="subtitle">
                        Trains&nbsp;&nbsp;•&nbsp;&nbsp;Routes&nbsp;&nbsp;•&nbsp;&nbsp;Stations&nbsp;&nbsp;•&nbsp;&nbsp;Schedules
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        """
        <div style="text-align:right; padding-top:10px;">
            <span class="online">
                <span class="online-dot"></span>
                Railway Database Online
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

    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">SMART RAILWAY SEARCH</div>
            <div class="hero-title">Where would you like to go?</div>
            <div class="hero-subtitle">
                Search trains, discover routes, check schedules and find stations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">QUICK SEARCH</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        if st.button("🚆\nTRAIN SEARCH", use_container_width=True):
            st.session_state.page = "Train Search"
            st.rerun()

    with col2:
        if st.button("🗺️\nROUTE SEARCH", use_container_width=True):
            st.session_state.page = "Route Search"
            st.rerun()

    with col3:
        if st.button("📅\nSCHEDULES", use_container_width=True):
            st.session_state.page = "Train Schedule"
            st.rerun()

    with col4:
        if st.button("📍\nSTATIONS", use_container_width=True):
            st.session_state.page = "Station Information"
            st.rerun()

    st.markdown(
        """
        <div style="
            margin-top:28px;
            padding:18px 20px;
            border-radius:16px;
            border:1px solid rgba(148,163,184,0.10);
            background:rgba(17,23,33,0.55);
            color:#94a3b8;
            text-align:center;
            font-size:13px;
        ">
            💡 <b style="color:#cbd5e1;">Tip:</b>
            Use Route Search to find trains between cities such as
            <b style="color:#f8fafc;">Mumbai → Goa</b> or
            <b style="color:#f8fafc;">Mumbai → Delhi</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TRAIN SEARCH
# ============================================================

def show_train_search():

    st.markdown('<div class="page-heading">🔎 Train Search</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-description">Search for a train using its number or name.</div>',
        unsafe_allow_html=True
    )

    search_text = st.text_input(
        "Train Number or Train Name",
        placeholder="Example: 10103 or Mandovi"
    )

    if st.button("🔍 Search Train", type="primary"):

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
            st.error(f"No train found for '{search_text}'.")
        else:
            st.success(f"🚆 {len(df)} train(s) found.")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# ROUTE SEARCH FUNCTION
# ============================================================

def get_trains_between_route(source_codes, destination_codes):

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

    st.markdown('<div class="page-heading">🗺️ Route Search</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-description">Find trains travelling between two cities or stations.</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

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

    if st.button("🔍 Find Trains", type="primary"):

        if not source.strip() or not destination.strip():
            st.warning("Please enter both source and destination.")
            return

        source_codes = get_station_codes(source)
        destination_codes = get_station_codes(destination)

        if not source_codes:
            st.error(f"No station mapping found for '{source}'.")
            return

        if not destination_codes:
            st.error(f"No station mapping found for '{destination}'.")
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

    st.markdown('<div class="page-heading">📅 Train Schedule</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-description">View the complete station-by-station schedule of a train.</div>',
        unsafe_allow_html=True
    )

    train_number = st.text_input(
        "Enter Train Number",
        placeholder="Example: 10103"
    )

    if st.button("📅 View Schedule", type="primary"):

        if not train_number.strip():
            st.warning("Please enter a train number.")
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

    st.markdown('<div class="page-heading">📍 Station Information</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-description">Search for a railway station using its code or name.</div>',
        unsafe_allow_html=True
    )

    search_station = st.text_input(
        "Station Code or Station Name",
        placeholder="Example: MAO or Madgaon"
    )

    if st.button("🔍 Search Station", type="primary"):

        if not search_station.strip():
            st.warning("Please enter a station code or name.")
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
                f"📍 {len(df)} station(s) found."
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
