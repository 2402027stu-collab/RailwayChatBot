import streamlit as st
import sqlite3
import pandas as pd
import os

# ============================================================
# AI ROUTER
# ============================================================

try:
    from ai_router import ask_railway_ai
    AI_AVAILABLE = True
except Exception:
    AI_AVAILABLE = False


# ============================================================
# PAGE CONFIG
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "Database", "railway.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def check_database():
    if not os.path.exists(DB_PATH):
        return False
    return True


# ============================================================
# DATABASE HELPERS
# ============================================================

def get_tables():

    try:
        conn = get_connection()

        query = """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df["name"].tolist()

    except Exception:
        return []


def get_table_columns(table_name):

    try:

        conn = get_connection()

        query = f'PRAGMA table_info("{table_name}")'

        df = pd.read_sql_query(query, conn)

        conn.close()

        return df["name"].tolist()

    except Exception:
        return []


def find_table(possible_names):

    tables = get_tables()

    for name in possible_names:

        for table in tables:

            if table.lower() == name.lower():
                return table

    return None


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN APP
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(37,99,235,0.10),
                transparent 35%
            ),
            #0b0f17;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #111827 0%,
                #172554 100%
            );
        border-right: 1px solid #263247;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 12px;
        border: 1px solid #334155;
        background: rgba(255,255,255,0.04);
        color: white;
        font-weight: 600;
        transition: 0.2s;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59,130,246,0.20);
        border-color: #3b82f6;
    }


    /* ======================================================
       BRAND
       ====================================================== */

    .brand-box {
        text-align: center;
        padding: 18px 5px;
    }

    .brand-icon {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .brand-title {
        font-size: 23px;
        font-weight: 800;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 5px;
    }


    /* ======================================================
       TOP HEADER
       ====================================================== */

    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 0 20px 0;
        border-bottom: 1px solid #263247;
        margin-bottom: 28px;
    }

    .top-title {
        font-size: 30px;
        font-weight: 800;
    }

    .top-subtitle {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 4px;
    }

    .online {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 30px;
        border: 1px solid #166534;
        background: rgba(22,101,52,0.15);
        color: #4ade80;
        font-size: 12px;
        font-weight: 700;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 65px 35px;
        border-radius: 24px;

        background:
            radial-gradient(
                circle at 80% 20%,
                rgba(59,130,246,0.25),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #172554,
                #1d4ed8,
                #312e81
            );

        border: 1px solid #3b82f6;
        box-shadow:
            0 20px 50px rgba(37,99,235,0.20);

        text-align: center;
        margin-bottom: 28px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 30px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.20);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 850;
        color: white;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #dbeafe;
        max-width: 700px;
        margin: auto;
    }


    /* ======================================================
       AI CARD
       ====================================================== */

    .ai-card {
        padding: 28px;
        border-radius: 20px;

        background:
            linear-gradient(
                135deg,
                #111827,
                #172033
            );

        border: 1px solid #334155;

        box-shadow:
            0 10px 30px rgba(0,0,0,0.20);

        margin-bottom: 20px;
    }

    .ai-title {
        font-size: 25px;
        font-weight: 800;
        color: #f8fafc;
    }

    .ai-subtitle {
        margin-top: 8px;
        color: #94a3b8;
        line-height: 1.7;
    }


    /* ======================================================
       SECTION TITLE
       ====================================================== */

    .section-title {
        font-size: 23px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 30px;
        margin-bottom: 15px;
    }


    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-card {
        padding: 23px;
        min-height: 145px;
        border-radius: 18px;

        background: #111827;

        border: 1px solid #263247;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.15);
    }

    .feature-icon {
        font-size: 30px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 750;
        margin-top: 9px;
        color: #f8fafc;
    }

    .feature-text {
        color: #94a3b8;
        font-size: 13px;
        margin-top: 7px;
        line-height: 1.5;
    }


    /* ======================================================
       PAGE HEADER
       ====================================================== */

    .page-header {
        padding: 25px 30px;
        border-radius: 18px;

        background: #111827;

        border: 1px solid #263247;

        margin-bottom: 25px;
    }

    .page-title {
        font-size: 30px;
        font-weight: 800;
        color: #f8fafc;
    }

    .page-subtitle {
        color: #94a3b8;
        margin-top: 6px;
    }


    /* ======================================================
       TIP
       ====================================================== */

    .home-tip {
        margin-top: 22px;
        padding: 15px 20px;
        border-radius: 14px;
        background: #111827;
        border: 1px solid #263247;
        color: #cbd5e1;
        text-align: center;
        font-size: 13px;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    div.stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 650;
        border: 1px solid #334155;
        background: #111827;
        color: #f8fafc;
    }

    div.stButton > button:hover {
        border-color: #3b82f6;
        color: white;
        background: #172033;
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="input"] {
        background: #111827;
        border-radius: 12px;
    }

    div[data-baseweb="select"] {
        border-radius: 12px;
    }

    textarea {
        background: #111827 !important;
        color: white !important;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #263247;
    }


    /* ======================================================
       AI RESPONSE
       ====================================================== */

    .ai-response {
        padding: 22px;
        margin-top: 20px;
        border-radius: 18px;

        background: #111827;

        border: 1px solid #334155;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.15);
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        color: #64748b;
        margin-top: 55px;
        padding: 20px;
        font-size: 12px;
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

if "ai_conversation" not in st.session_state:
    st.session_state.ai_conversation = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-box">
            <div class="brand-icon">🚆</div>
            <div class="brand-title">Railway Assistant</div>
            <div class="brand-subtitle">
                Indian Railway Information System
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 🧭 Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("🤖 AI Assistant", use_container_width=True):
        st.session_state.page = "AI Assistant"
        st.rerun()

    if st.button("🚆 Train Search", use_container_width=True):
        st.session_state.page = "Train Search"
        st.rerun()

    if st.button("🛤️ Route Search", use_container_width=True):
        st.session_state.page = "Route Search"
        st.rerun()

    if st.button("🕐 Train Schedule", use_container_width=True):
        st.session_state.page = "Train Schedule"
        st.rerun()

    if st.button("📍 Station Information", use_container_width=True):
        st.session_state.page = "Station Information"
        st.rerun()

    st.markdown("---")

    if check_database():

        st.markdown(
            """
            <div style="
                text-align:center;
                color:#4ade80;
                font-size:12px;
                padding:10px;
            ">
                🟢 Railway Database Online
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div style="
                text-align:center;
                color:#f87171;
                font-size:12px;
                padding:10px;
            ">
                🔴 Database Not Found
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# TOP HEADER
# ============================================================

st.markdown(
    """
    <div class="top-header">

        <div>
            <div class="top-title">
                🚆 Indian Railway Assistant
            </div>

            <div class="top-subtitle">
                Trains • Routes • Stations • Schedules
            </div>
        </div>

        <div class="online">
            🟢 Railway Database Online
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


def show_home():

    # ============================================================
    # HERO
    # ============================================================

    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">
                SMART RAILWAY SEARCH
            </div>

            <div class="hero-title">
                Where would you like to go? 🚉
            </div>

            <div class="hero-subtitle">
                Search trains, discover routes, check schedules and find stations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ============================================================
    # AI ASSISTANT CARD
    # ============================================================

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🤖 AI Railway Assistant
            </div>

            <div class="ai-subtitle">
                Ask your railway question in normal language.
                The assistant will understand your request automatically.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ============================================================
    # AI INPUT
    # ============================================================

    question = st.text_input(
        "Ask Railway Assistant",
        placeholder="Example: Find trains from Mumbai to Goa",
        key="home_ai_question"
    )

    if st.button("🤖 Ask Railway Assistant", use_container_width=True):

        if question.strip() == "":
            st.warning("Please enter your railway question.")

        else:
            with st.spinner("Railway Assistant is thinking..."):

                try:
                    result = ask_railway_ai(question)

                    st.markdown(
                        """
                        <div class="ai-response">
                            <div class="ai-title">
                                🤖 Railway Assistant
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(result)

                except Exception as e:
                    st.error(f"Unable to process your request: {e}")

    # ============================================================
    # QUICK SEARCH TITLE
    # ============================================================

    st.markdown(
        """
        <div class="quick-title">
            ⚡ Quick Search
        </div>
        """,
        unsafe_allow_html=True
    )

    # ============================================================
    # QUICK SEARCH BUTTONS
    # ============================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🚉 TRAIN SEARCH", use_container_width=True):
            st.session_state.page = "Train Search"
            st.rerun()

    with col2:
        if st.button("🛤️ ROUTE SEARCH", use_container_width=True):
            st.session_state.page = "Route Search"
            st.rerun()

    with col3:
        if st.button("📅 SCHEDULES", use_container_width=True):
            st.session_state.page = "Train Schedule"
            st.rerun()

    with col4:
        if st.button("📍 STATIONS", use_container_width=True):
            st.session_state.page = "Station Information"
            st.rerun()

    # ============================================================
    # TIP
    # ============================================================

    st.markdown(
        """
        <div class="home-tip">
            💡 <b>Tip:</b> Use Route Search to find trains between cities
            such as <b>Mumbai → Goa</b> or <b>Mumbai → Delhi</b>.
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# TRAIN SEARCH
# ============================================================

def show_train_search():

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">
                🚆 Train Search
            </div>

            <div class="page-subtitle">
                Search for a train using its train number or name.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    search = st.text_input(
        "🔎 Search Train",
        placeholder="Enter train number or train name"
    )

    if st.button(
        "🔍 Search Train",
        use_container_width=True
    ):

        if not search.strip():

            st.warning("Please enter a train number or train name.")

            return

        try:

            conn = get_connection()

            tables = get_tables()

            train_table = find_table(
                ["trains", "train", "train_data"]
            )

            if train_table is None:

                st.error(
                    "Train table was not found in the database."
                )

                conn.close()

                return

            columns = get_table_columns(train_table)

            number_col = None
            name_col = None

            for col in columns:

                low = col.lower()

                if low in ["number", "train_number", "train_no"]:
                    number_col = col

                if low in ["name", "train_name"]:
                    name_col = col

            conditions = []
            params = []

            if number_col:

                conditions.append(
                    f'CAST("{number_col}" AS TEXT) LIKE ?'
                )

                params.append(f"%{search}%")

            if name_col:

                conditions.append(
                    f'LOWER("{name_col}") LIKE LOWER(?)'
                )

                params.append(f"%{search}%")

            if not conditions:

                st.error(
                    "Could not find train number/name columns."
                )

                conn.close()

                return

            query = f'''
                SELECT *
                FROM "{train_table}"
                WHERE {" OR ".join(conditions)}
                LIMIT 50
            '''

            df = pd.read_sql_query(
                query,
                conn,
                params=params
            )

            conn.close()

            if df.empty:

                st.warning(
                    f"No train found for '{search}'."
                )

            else:

                st.success(
                    f"🚆 {len(df)} train(s) found."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:

            st.error(
                f"Database error: {e}"
            )


# ============================================================
# ROUTE SEARCH
# ============================================================

def show_route_search():

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">
                🛤️ Route Search
            </div>

            <div class="page-subtitle">
                Find trains travelling between two cities or stations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        source = st.text_input(
            "🟢 From",
            placeholder="Example: Mumbai"
        )

    with col2:

        destination = st.text_input(
            "🔴 To",
            placeholder="Example: Goa"
        )

    if st.button(
        "🔎 Find Trains",
        use_container_width=True
    ):

        if not source.strip() or not destination.strip():

            st.warning(
                "Please enter both source and destination."
            )

            return

        try:

            conn = get_connection()

            train_table = find_table(
                ["trains", "train", "train_data"]
            )

            if train_table is None:

                st.error(
                    "Train table was not found."
                )

                conn.close()

                return

            columns = get_table_columns(train_table)

            source_col = None
            destination_col = None

            for col in columns:

                low = col.lower()

                if low in [
                    "source_station",
                    "source",
                    "from_station",
                    "from"
                ]:
                    source_col = col

                if low in [
                    "destination_station",
                    "destination",
                    "to_station",
                    "to"
                ]:
                    destination_col = col

            if source_col is None or destination_col is None:

                st.error(
                    "The train table does not contain "
                    "source/destination columns."
                )

                conn.close()

                return

            query = f'''
                SELECT *
                FROM "{train_table}"
                WHERE
                    LOWER("{source_col}") LIKE LOWER(?)
                    AND
                    LOWER("{destination_col}") LIKE LOWER(?)
                LIMIT 100
            '''

            df = pd.read_sql_query(
                query,
                conn,
                params=[
                    f"%{source.strip()}%",
                    f"%{destination.strip()}%"
                ]
            )

            conn.close()

            if df.empty:

                st.warning(
                    f"No direct trains found from "
                    f"{source.title()} to {destination.title()}."
                )

            else:

                st.success(
                    f"🚆 {len(df)} train(s) found from "
                    f"{source.title()} to {destination.title()}."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:

            st.error(
                f"Route search error: {e}"
            )


# ============================================================
# TRAIN SCHEDULE
# ============================================================

def show_train_schedule():

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">
                🕐 Train Schedule
            </div>

            <div class="page-subtitle">
                Check the stations, arrival and departure times
                of a train.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    train_number = st.text_input(
        "🚆 Train Number",
        placeholder="Example: 10103"
    )

    if st.button(
        "🕐 Show Schedule",
        use_container_width=True
    ):

        if not train_number.strip():

            st.warning(
                "Please enter a train number."
            )

            return

        try:

            conn = get_connection()

            schedule_table = find_table(
                [
                    "schedules",
                    "schedule",
                    "train_schedule"
                ]
            )

            if schedule_table is None:

                st.error(
                    "Schedule table was not found."
                )

                conn.close()

                return

            columns = get_table_columns(schedule_table)

            train_col = None

            for col in columns:

                low = col.lower()

                if low in [
                    "train_number",
                    "train_no",
                    "number"
                ]:

                    train_col = col
                    break

            if train_col is None:

                st.error(
                    "Train number column was not found "
                    "in schedule table."
                )

                conn.close()

                return

            query = f'''
                SELECT *
                FROM "{schedule_table}"
                WHERE CAST("{train_col}" AS TEXT) = ?
            '''

            df = pd.read_sql_query(
                query,
                conn,
                params=[train_number.strip()]
            )

            conn.close()

            if df.empty:

                st.warning(
                    f"No schedule found for train "
                    f"{train_number}."
                )

            else:

                st.success(
                    f"🕐 Schedule found for train "
                    f"{train_number}."
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

        except Exception as e:

            st.error(
                f"Schedule error: {e}"
            )


# ============================================================
# STATION INFORMATION
# ============================================================

def show_station_information():

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">
                📍 Station Information
            </div>

            <div class="page-subtitle">
                Search for railway stations by name or station code.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    station = st.text_input(
        "📍 Station Search",
        placeholder="Example: Mumbai / Karmali / MAO"
    )

    if st.button(
        "🔎 Search Station",
        use_container_width=True
    ):

        if not station.strip():

            st.warning(
                "Please enter a station name or code."
            )

            return

        try:

            conn = get_connection()

            station_table = find_table(
                [
                    "stations",
                    "station",
                    "station_data"
                ]
            )

            if station_table is None:

                st.error(
                    "Station table was not found."
                )

                conn.close()

                return

            columns = get_table_columns(station_table)

            search_conditions = []
            params = []

            for col in columns:

                low = col.lower()

                if (
                    "name" in low
                    or "code" in low
                ):

                    search_conditions.append(
                        f'LOWER(CAST("{col}" AS TEXT)) LIKE LOWER(?)'
                    )

                    params.append(
                        f"%{station.strip()}%"
                    )

            if not search_conditions:

                st.error(
                    "No station name/code columns found."
                )

                conn.close()

                return

            query = f'''
                SELECT *
                FROM "{station_table}"
                WHERE {" OR ".join(search_conditions)}
                LIMIT 100
            '''

            df = pd.read_sql_query(
                query,
                conn,
                params=params
            )

            conn.close()

            if df.empty:

                st.warning(
                    f"No station found for '{station}'."
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

        except Exception as e:

            st.error(
                f"Station search error: {e}"
            )


# ============================================================
# AI ASSISTANT
# ============================================================

def show_ai_assistant():

    st.markdown(
        """
        <div class="page-header">

            <div class="page-title">
                🤖 AI Railway Assistant
            </div>

            <div class="page-subtitle">
                Ask railway questions in normal language.
                For example: "Find trains from Mumbai to Goa".
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if not AI_AVAILABLE:

        st.error(
            "AI Router could not be loaded. "
            "Check ai_router.py and its required packages."
        )

        return

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                💬 Ask me anything about Indian Railways
            </div>

            <div class="ai-subtitle">
                Try questions like:
                <br><br>
                🚆 Find trains from Mumbai to Goa
                <br>
                🚆 Tell me about train 10103
                <br>
                🕐 Show schedule of 10103
                <br>
                📍 What is Karmali station?
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_area(
        "Your railway question",
        placeholder="Example: Find trains from Mumbai to Goa",
        height=100
    )

    col1, col2 = st.columns([3, 1])

    with col1:

        ask_button = st.button(
            "🤖 Ask Railway Assistant",
            use_container_width=True
        )

    with col2:

        clear_button = st.button(
            "🗑️ Clear",
            use_container_width=True
        )

    if clear_button:

        st.session_state.ai_conversation = []

        st.rerun()

    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a railway question."
            )

            return

        with st.spinner(
            "🤖 Understanding your question..."
        ):

            try:

                result = ask_railway_ai(
                    question.strip()
                )

                st.session_state.ai_conversation.append(
                    {
                        "question": question.strip(),
                        "answer": result
                    }
                )

                st.markdown(
                    """
                    <div class="ai-response">
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(result)

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    f"AI Assistant Error: {e}"
                )

    # Previous conversations

    if st.session_state.ai_conversation:

        st.markdown(
            """
            <div class="section-title">
                💬 Previous Questions
            </div>
            """,
            unsafe_allow_html=True
        )

        for item in reversed(
            st.session_state.ai_conversation
        ):

            st.markdown(
                f"**👤 You:** {item['question']}"
            )

            st.markdown(
                f"**🤖 Assistant:**"
            )

            st.markdown(
                item["answer"]
            )

            st.markdown("---")


# ============================================================
# PAGE ROUTING
# ============================================================

if st.session_state.page == "Home":

    show_home()

elif st.session_state.page == "AI Assistant":

    show_ai_assistant()

elif st.session_state.page == "Train Search":

    show_train_search()

elif st.session_state.page == "Route Search":

    show_route_search()

elif st.session_state.page == "Train Schedule":

    show_train_schedule()

elif st.session_state.page == "Station Information":

    show_station_information()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🚆 Indian Railway Assistant
        <br>
        Powered by local railway database and AI
    </div>
    """,
    unsafe_allow_html=True
)