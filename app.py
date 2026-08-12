import streamlit as st

from search import (
    get_train_by_number,
    get_schedule,
    get_station,
    get_station_codes,
    get_trains_between_route
)

from response_generator import generate_train_response
from schedule_response import generate_schedule_response
from station_response import generate_station_response

from nlp import (
    detect_intent,
    extract_train_number,
    extract_station_code,
    extract_source_destination
)


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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background: #0b0e14;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}


/* =========================
   SIDEBAR
   ========================= */

[data-testid="stSidebar"] {
    background: #0f131b;
    border-right: 1px solid #242a35;
}

.sidebar-title {
    font-size: 25px;
    font-weight: 800;
    color: white;
    margin-bottom: 4px;
}

.sidebar-subtitle {
    color: #8d96a8;
    font-size: 12px;
    margin-bottom: 25px;
}

.side-card {
    background: #151a24;
    border: 1px solid #272e3b;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    transition: 0.2s;
}

.side-card:hover {
    border-color: #ff3b30;
}

.side-card-title {
    color: #ffffff;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 7px;
}

.side-card-text {
    color: #8f98aa;
    font-size: 12px;
    line-height: 1.5;
}


/* =========================
   HEADER
   ========================= */

.railway-header {
    background: linear-gradient(
        135deg,
        #171c27,
        #10141d
    );

    border: 1px solid #272e3b;
    border-radius: 20px;

    padding: 22px 26px;

    margin-bottom: 22px;

    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo-row {
    display: flex;
    align-items: center;
    gap: 15px;
}

.logo {
    width: 55px;
    height: 55px;

    border-radius: 15px;

    background: #ff3b30;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 30px;
}

.header-title {
    color: white;
    font-size: 28px;
    font-weight: 800;
}

.header-subtitle {
    color: #8f98aa;
    font-size: 13px;
    margin-top: 4px;
}

.status {
    color: #b8c0ce;
    font-size: 12px;

    background: #151a24;

    border: 1px solid #29303d;

    border-radius: 20px;

    padding: 9px 14px;
}

.status-dot {
    display: inline-block;

    width: 8px;
    height: 8px;

    background: #27d17f;

    border-radius: 50%;

    margin-right: 7px;
}


/* =========================
   SEARCH HERO
   ========================= */

.search-hero {
    background:
        radial-gradient(
            circle at 80% 20%,
            rgba(255, 59, 48, 0.15),
            transparent 35%
        ),
        #141923;

    border: 1px solid #282f3d;

    border-radius: 20px;

    padding: 35px;

    text-align: center;

    margin-bottom: 22px;
}

.search-title {
    color: white;

    font-size: 26px;

    font-weight: 800;

    margin-bottom: 8px;
}

.search-subtitle {
    color: #929bad;

    font-size: 14px;
}


/* =========================
   QUICK ACTIONS
   ========================= */

.quick-title {
    color: #a9b1c1;

    font-size: 12px;

    font-weight: 700;

    letter-spacing: 1px;

    margin: 15px 0 10px 2px;
}

.metric-card {
    background: #141923;

    border: 1px solid #292f3c;

    border-radius: 16px;

    padding: 20px;

    text-align: center;

    min-height: 105px;
}

.metric-icon {
    font-size: 28px;

    margin-bottom: 7px;
}

.metric-label {
    color: #8d96a8;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 0.7px;
}


/* =========================
   TRAIN CARD
   ========================= */

.train-card {
    background: linear-gradient(
        135deg,
        #171c27,
        #121620
    );

    border: 1px solid #2b3240;

    border-radius: 18px;

    padding: 22px;

    margin: 12px 0;
}

.train-number {
    color: #ff5148;

    font-size: 13px;

    font-weight: 800;

    letter-spacing: 1px;
}

.train-name {
    color: white;

    font-size: 21px;

    font-weight: 800;

    margin-top: 5px;

    margin-bottom: 18px;
}

.route {
    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 20px;
}

.station {
    flex: 1;
}

.station-code {
    color: white;

    font-size: 23px;

    font-weight: 800;
}

.station-name {
    color: #8e97a8;

    font-size: 12px;

    margin-top: 4px;
}

.route-line {
    flex: 1;

    text-align: center;

    color: #ff5148;

    font-size: 20px;
}

.info-row {
    display: flex;

    gap: 10px;

    margin-top: 20px;

    flex-wrap: wrap;
}

.info-pill {
    background: #1b202b;

    border: 1px solid #2b3240;

    border-radius: 10px;

    padding: 8px 12px;

    color: #aab2c0;

    font-size: 12px;
}


/* =========================
   CHAT INPUT
   ========================= */

[data-testid="stChatInput"] {
    border-color: #303746;
}


/* =========================
   DATAFRAME
   ========================= */

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div class="sidebar-title">
        🚆 Railway Assistant
    </div>

    <div class="sidebar-subtitle">
        Indian Railway Information System
    </div>

    <div class="side-card">
        <div class="side-card-title">
            🔎 Train Search
        </div>
        <div class="side-card-text">
            Find trains using train number or name.
        </div>
    </div>

    <div class="side-card">
        <div class="side-card-title">
            🛤️ Route Search
        </div>
        <div class="side-card-text">
            Find trains travelling between two cities.
        </div>
    </div>

    <div class="side-card">
        <div class="side-card-title">
            📅 Train Schedule
        </div>
        <div class="side-card-text">
            View complete station schedules.
        </div>
    </div>

    <div class="side-card">
        <div class="side-card-title">
            📍 Station Information
        </div>
        <div class="side-card-text">
            Search railway stations using station codes.
        </div>
    </div>

    <br>

    <div style="
        color:#697386;
        font-size:11px;
        text-align:center;
        line-height:1.5;
    ">
        Railway Assistant<br>
        Powered by local railway database
    </div>
    """)


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="railway-header">

    <div class="logo-row">

        <div class="logo">
            🚆
        </div>

        <div>

            <div class="header-title">
                Indian Railway Assistant
            </div>

            <div class="header-subtitle">
                Trains • Routes • Stations • Schedules
            </div>

        </div>

    </div>

    <div class="status">
        <span class="status-dot"></span>
        Railway Database Online
    </div>

</div>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="search-hero">

    <div class="search-title">
        Where would you like to go?
    </div>

    <div class="search-subtitle">
        Ask about trains, stations, routes or schedules
    </div>

</div>
""")


# ============================================================
# QUICK ACTIONS
# ============================================================

st.html("""
<div class="quick-title">
    QUICK SEARCH
</div>
""")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.html("""
    <div class="metric-card">
        <div class="metric-icon">🚆</div>
        <div class="metric-label">TRAIN SEARCH</div>
    </div>
    """)

with col2:
    st.html("""
    <div class="metric-card">
        <div class="metric-icon">🛤️</div>
        <div class="metric-label">ROUTE SEARCH</div>
    </div>
    """)

with col3:
    st.html("""
    <div class="metric-card">
        <div class="metric-icon">📅</div>
        <div class="metric-label">SCHEDULES</div>
    </div>
    """)

with col4:
    st.html("""
    <div class="metric-card">
        <div class="metric-icon">📍</div>
        <div class="metric-label">STATIONS</div>
    </div>
    """)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SHOW PREVIOUS CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message.get("type") == "train":

            train = message["data"]

            st.html(f"""
            <div class="train-card">

                <div class="train-number">
                    TRAIN {train['number']}
                </div>

                <div class="train-name">
                    {train['name']}
                </div>

                <div class="route">

                    <div class="station">

                        <div class="station-code">
                            {train['from_code']}
                        </div>

                        <div class="station-name">
                            {train['from_name']}
                        </div>

                    </div>

                    <div class="route-line">
                        ━━━━━ 🚆 ━━━━━
                    </div>

                    <div class="station">

                        <div class="station-code">
                            {train['to_code']}
                        </div>

                        <div class="station-name">
                            {train['to_name']}
                        </div>

                    </div>

                </div>

                <div class="info-row">

                    <div class="info-pill">
                        🕐 Departure: {train['departure']}
                    </div>

                    <div class="info-pill">
                        🕐 Arrival: {train['arrival']}
                    </div>

                    <div class="info-pill">
                        📏 {train['distance']} km
                    </div>

                    <div class="info-pill">
                        🚄 {train['type']}
                    </div>

                    <div class="info-pill">
                        🌐 Zone: {train['zone']}
                    </div>

                </div>

            </div>
            """)

        else:

            st.markdown(message["content"])


# ============================================================
# CHAT INPUT
# ============================================================

user = st.chat_input(
    "Ask me anything about Indian Railways..."
)


# ============================================================
# PROCESS USER QUESTION
# ============================================================

if user:

    # --------------------------------------------------------
    # Save user message
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": user
    })

    with st.chat_message("user"):
        st.markdown(user)


    # --------------------------------------------------------
    # NLP
    # --------------------------------------------------------

    intent = detect_intent(user)

    train_number = extract_train_number(user)

    station_code = extract_station_code(user)

    source, destination = extract_source_destination(user)


    # --------------------------------------------------------
    # TRAIN DETAILS
    # --------------------------------------------------------

    if intent == "train":

        if not train_number:

            reply = "❌ Please enter a valid train number."

            with st.chat_message("assistant"):
                st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        else:

            train = get_train_by_number(train_number)

            if len(train) == 0:

                reply = f"❌ Train **{train_number}** was not found."

                with st.chat_message("assistant"):
                    st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            else:

                row = train.iloc[0]

                # Get station codes
                from_code = row.get(
                    "from_station_code",
                    ""
                )

                to_code = row.get(
                    "to_station_code",
                    ""
                )

                from_name = row.get(
                    "from_station_name",
                    ""
                )

                to_name = row.get(
                    "to_station_name",
                    ""
                )

                train_data = {
                    "number": row.get("number", train_number),
                    "name": row.get("name", "Unknown Train"),
                    "from_code": from_code,
                    "to_code": to_code,
                    "from_name": from_name,
                    "to_name": to_name,
                    "departure": row.get("departure", ""),
                    "arrival": row.get("arrival", ""),
                    "distance": row.get("distance", ""),
                    "type": row.get("type", ""),
                    "zone": row.get("zone", "")
                }

                with st.chat_message("assistant"):

                    st.html(f"""
                    <div class="train-card">

                        <div class="train-number">
                            TRAIN {train_data['number']}
                        </div>

                        <div class="train-name">
                            {train_data['name']}
                        </div>

                        <div class="route">

                            <div class="station">

                                <div class="station-code">
                                    {train_data['from_code']}
                                </div>

                                <div class="station-name">
                                    {train_data['from_name']}
                                </div>

                            </div>

                            <div class="route-line">
                                ━━━━━ 🚆 ━━━━━
                            </div>

                            <div class="station">

                                <div class="station-code">
                                    {train_data['to_code']}
                                </div>

                                <div class="station-name">
                                    {train_data['to_name']}
                                </div>

                            </div>

                        </div>

                        <div class="info-row">

                            <div class="info-pill">
                                🕐 Departure: {train_data['departure']}
                            </div>

                            <div class="info-pill">
                                🕐 Arrival: {train_data['arrival']}
                            </div>

                            <div class="info-pill">
                                📏 {train_data['distance']} km
                            </div>

                            <div class="info-pill">
                                🚄 {train_data['type']}
                            </div>

                            <div class="info-pill">
                                🌐 Zone: {train_data['zone']}
                            </div>

                        </div>

                    </div>
                    """)

                st.session_state.messages.append({
                    "role": "assistant",
                    "type": "train",
                    "data": train_data
                })


    # --------------------------------------------------------
    # STATION DETAILS
    # --------------------------------------------------------

    elif intent == "station":

        if station_code:

            if isinstance(station_code, list):
                code = station_code[0]
            else:
                code = station_code

            station = get_station(code)

            if len(station) > 0:

                reply = generate_station_response(
                    station.iloc[0]
                )

            else:

                reply = f"❌ Station **{code}** was not found."

        else:

            reply = "❌ Please enter a valid station code."


        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })


    # --------------------------------------------------------
    # TRAIN SCHEDULE
    # --------------------------------------------------------

    elif intent == "schedule":

        if train_number:

            schedule = get_schedule(train_number)

            if len(schedule) > 0:

                reply = generate_schedule_response(
                    schedule
                )

                with st.chat_message("assistant"):

                    st.markdown(
                        f"### 📅 Train {train_number} Schedule"
                    )

                    st.dataframe(
                        schedule,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.caption(
                        f"Complete schedule for train {train_number}"
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            else:

                reply = (
                    f"❌ Schedule for train "
                    f"**{train_number}** was not found."
                )

                with st.chat_message("assistant"):
                    st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

        else:

            reply = "❌ Please enter a valid train number."

            with st.chat_message("assistant"):
                st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })


    # --------------------------------------------------------
    # TRAINS BETWEEN TWO CITIES
    # --------------------------------------------------------

    elif intent == "between":

        if source and destination:

            source_df = get_station_codes(source)

            if len(source_df) > 0:

                source_codes = (
                    source_df["code"]
                    .dropna()
                    .unique()
                    .tolist()
                )

            else:

                source_codes = [source.upper()]


            destination_df = get_station_codes(destination)

            if len(destination_df) > 0:

                destination_codes = (
                    destination_df["code"]
                    .dropna()
                    .unique()
                    .tolist()
                )

            else:

                destination_codes = [
                    destination.upper()
                ]

            trains = get_trains_between_route(
                source_codes,
                destination_codes
            )

            if trains.empty:

                reply = (
                    f"❌ No trains found from "
                    f"**{source.title()}** to "
                    f"**{destination.title()}**."
                )

                with st.chat_message("assistant"):
                    st.markdown(reply)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

            else:

                # Remove duplicate trains
                trains = trains.drop_duplicates(
                    subset=["number"]
                )

                reply = (
                    f"🚆 **{len(trains)} train(s) found** "
                    f"from **{source.title()}** "
                    f"to **{destination.title()}**."
                )

                with st.chat_message("assistant"):
                    st.markdown(reply)

                    st.dataframe(
                        trains,
                        use_container_width=True,
                        hide_index=True
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    else:

        reply = """
❌ I didn't understand that.

Try something like:

- **Tell me about train 10103**
- **Schedule of train 10103**
- **Station MAO**
- **Trains from Mumbai to Goa**
"""

        with st.chat_message("assistant"):
            st.markdown(reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })