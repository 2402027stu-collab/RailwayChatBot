import streamlit as st
import sqlite3
import pandas as pd

# AI Router
from ai_router import ask_railway_ai


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Railway Assistant",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GENERAL ---------- */

    .stApp {
        background: #f7f9fc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #0f172a 0%,
            #172554 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }


    /* ---------- HERO ---------- */

    .hero {
        padding: 55px 35px;
        border-radius: 25px;
        background: linear-gradient(
            135deg,
            #1d4ed8,
            #2563eb,
            #3b82f6
        );
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.92;
    }


    /* ---------- AI CARD ---------- */

    .ai-card {
        padding: 28px;
        margin-top: 30px;
        margin-bottom: 18px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #eef6ff,
            #ffffff
        );
        border: 1px solid #dbeafe;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.07);
    }

    .ai-title {
        font-size: 27px;
        font-weight: 750;
        color: #1e3a8a;
    }

    .ai-subtitle {
        margin-top: 7px;
        font-size: 15px;
        color: #64748b;
    }


    /* ---------- SECTION TITLE ---------- */

    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: #0f172a;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ---------- FEATURE CARDS ---------- */

    .feature-card {
        padding: 25px;
        min-height: 150px;
        border-radius: 18px;
        background: white;
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.06);
        margin-bottom: 15px;
    }

    .feature-icon {
        font-size: 32px;
    }

    .feature-title {
        font-size: 20px;
        font-weight: 700;
        margin-top: 8px;
        color: #0f172a;
    }

    .feature-text {
        color: #64748b;
        font-size: 14px;
        margin-top: 5px;
    }


    /* ---------- PAGE HEADERS ---------- */

    .page-header {
        padding: 25px 30px;
        background: white;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 18px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    }

    .page-title {
        font-size: 32px;
        font-weight: 800;
        color: #0f172a;
    }

    .page-subtitle {
        color: #64748b;
        margin-top: 5px;
    }


    /* ---------- BUTTONS ---------- */

    div.stButton > button {
        border-radius: 12px;
        font-weight: 650;
        min-height: 45px;
    }


    /* ---------- AI RESPONSE ---------- */

    .ai-response {
        padding: 22px;
        margin-top: 20px;
        border-radius: 18px;
        background: white;
        border: 1px solid #dbeafe;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 50px;
        padding: 20px;
        font-size: 13px;
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
# DATABASE CONNECTION
# ============================================================

DB_PATH = "Database/railway.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:20px 5px;">
            <div style="font-size:45px;">🚆</div>
            <div style="font-size:25px; font-weight:800;">
                Railway Assistant
            </div>
            <div style="font-size:13px; opacity:0.8;">
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

    st.markdown(
        """
        <div style="
            text-align:center;
            font-size:13px;
            opacity:0.75;
            padding:10px;
        ">
            🤖 AI Powered Railway Assistant
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HOME PAGE
# ============================================================

def show_home():

    # ==========================================
    # HERO SECTION
    # ==========================================

    st.markdown(
        """
        <div class="hero">

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


    # ==========================================
    # AI ASSISTANT SECTION
    # ==========================================

    st.markdown(
        """
        <div class="ai-card">

            <div class="ai-title">
                🤖 AI Railway Assistant
            </div>

            <div class="ai-subtitle">
                Ask your railway question in normal language.<br>
                The assistant will understand your request automatically.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # EXAMPLE
    # ==========================================

    st.info(
        "💡 Example: Find trains from Mumbai to Goa"
    )


    # ==========================================
    # AI BUTTON
    # ==========================================

    if st.button(
        "🤖 Ask Railway Assistant",
        use_container_width=False
    ):
        st.session_state["page"] = "AI Assistant"
        st.rerun()


    # ==========================================
    # QUICK SEARCH TITLE
    # ==========================================

    st.markdown(
        """
        <div class="quick-title">
            ⚡ Quick Search
        </div>
        """,
        unsafe_allow_html=True
    )


    # ==========================================
    # QUICK SEARCH BUTTONS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        if st.button(
            "🚉 TRAIN SEARCH",
            use_container_width=True
        ):
            st.session_state["page"] = "Train Search"
            st.rerun()


    with col2:

        if st.button(
            "🛤️ ROUTE SEARCH",
            use_container_width=True
        ):
            st.session_state["page"] = "Route Search"
            st.rerun()


    with col3:

        if st.button(
            "📅 SCHEDULES",
            use_container_width=True
        ):
            st.session_state["page"] = "Train Schedule"
            st.rerun()


    with col4:

        if st.button(
            "📍 STATIONS",
            use_container_width=True
        ):
            st.session_state["page"] = "Station Information"
            st.rerun()


    # ==========================================
    # TIP
    # ==========================================

    st.markdown(
        """
        <div class="home-tip">
            💡 <b>Tip:</b> Use Route Search to find trains between cities
            such as <b>Mumbai → Goa</b> or <b>Mumbai → Delhi</b>.
        </div>
        """,
        unsafe_allow_html=True
    )