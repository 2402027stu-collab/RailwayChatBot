import streamlit as st

from ai_router import ask_railway_ai


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Railway AI",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# FUNCTIONS
# ============================================================

def start_new_chat():
    st.session_state.messages = []


def add_chat_to_history(question):
    title = question.strip()

    if len(title) > 38:
        title = title[:38] + "..."

    if title and title not in st.session_state.chat_history:
        st.session_state.chat_history.insert(0, title)

    st.session_state.chat_history = st.session_state.chat_history[:8]


def get_ai_response(question):

    conversation = []

    for message in st.session_state.messages:
        conversation.append({
            "role": message["role"],
            "content": message["content"]
        })

    try:

        response = ask_railway_ai(
            question,
            conversation=conversation
        )

        if response is None:
            return "Sorry, I could not generate a response."

        if isinstance(response, str):
            return response

        if isinstance(response, dict):

            if "answer" in response:
                return str(response["answer"])

            if "response" in response:
                return str(response["response"])

            if "content" in response:
                return str(response["content"])

            return str(response)

        return str(response)

    except Exception as e:

        return (
            "Sorry, something went wrong while processing "
            "your request.\n\n"
            f"Error: `{e}`"
        )


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   MAIN PAGE
   ========================================================== */

.stApp {
    background: #ffffff;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 6rem;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: #f7f7f8;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}


/* Sidebar branding */

.sidebar-brand {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 2px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 20px;
}


/* Sidebar section */

.sidebar-section-title {
    font-size: 11px;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-top: 22px;
    margin-bottom: 8px;
}


/* Sidebar buttons */

section[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 40px;

    border-radius: 9px;

    border: 1px solid #e5e7eb;

    background: #ffffff;

    color: #374151;

    font-size: 13px;

    text-align: left;

    transition: all 0.15s ease;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #eeeeef;
    border-color: #d1d5db;
}


/* New chat */

.new-chat-box button {
    background: #111827 !important;
    color: #ffffff !important;
    border-color: #111827 !important;
    font-weight: 600 !important;
    text-align: center !important;
}


/* Sidebar information */

.sidebar-info {
    margin-top: 24px;

    padding: 13px;

    border: 1px solid #e5e7eb;

    border-radius: 10px;

    background: #ffffff;

    font-size: 12px;

    color: #6b7280;

    line-height: 1.6;
}


/* ==========================================================
   HEADER
   ========================================================== */

.top-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    padding-bottom: 18px;

    border-bottom: 1px solid #e5e7eb;
}

.top-title {
    font-size: 25px;
    font-weight: 700;
    color: #111827;
}

.top-right {
    font-size: 12px;
    color: #9ca3af;
}


/* ==========================================================
   WELCOME
   ========================================================== */

.welcome-container {
    text-align: center;

    margin-top: 120px;
    margin-bottom: 30px;
}

.welcome-icon {
    font-size: 48px;
    margin-bottom: 12px;
}

.welcome-title {
    font-size: 29px;
    font-weight: 750;
    color: #111827;
    margin-bottom: 8px;
}

.welcome-subtitle {
    font-size: 14px;
    color: #6b7280;
    line-height: 1.7;
}


/* ==========================================================
   CHAT
   ========================================================== */

[data-testid="stChatMessage"] {
    border-radius: 14px;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {
    text-align: center;

    margin-top: 30px;

    color: #9ca3af;

    font-size: 11px;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # Branding
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-brand">🚆 Railway AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Indian Railway Assistant'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # New Chat
    # --------------------------------------------------------

    st.markdown(
        '<div class="new-chat-box">',
        unsafe_allow_html=True
    )

    if st.button(
        "＋  New chat",
        use_container_width=True,
        key="new_chat"
    ):
        start_new_chat()
        st.rerun()

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Recent Chats
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section-title">'
        'Recent chats'
        '</div>',
        unsafe_allow_html=True
    )

    if st.session_state.chat_history:

        for index, title in enumerate(
            st.session_state.chat_history
        ):

            if st.button(
                f"💬  {title}",
                key=f"recent_{index}",
                use_container_width=True
            ):
                pass

    else:

        st.caption("No recent chats yet.")


    # --------------------------------------------------------
    # Try Asking
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section-title">'
        'Try asking'
        '</div>',
        unsafe_allow_html=True
    )

    questions = [
        "Find trains from Madgaon to Pune",
        "Show train 04601 details",
        "What trains go to Goa?",
        "Give me the schedule of train 11098",
        "Find trains from Goa to Patna"
    ]

    for index, question in enumerate(questions):

        if st.button(
            question,
            key=f"question_{index}",
            use_container_width=True
        ):

            st.session_state.pending_question = question

            st.rerun()


    # --------------------------------------------------------
    # Information
    # --------------------------------------------------------

    st.markdown(
        """
<div class="sidebar-info">
<b>🚆 Railway AI</b><br>
Ask about trains, routes, stations
and schedules using natural language.
<br><br>
🟢 Railway database connected<br>
🤖 AI powered by Groq
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
    <div class="top-title">Railway AI</div>
    <div class="top-right">Indian Railways</div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# CHECK PENDING QUESTION
# ============================================================

question_to_process = None

if st.session_state.pending_question:

    question_to_process = st.session_state.pending_question

    st.session_state.pending_question = None


# ============================================================
# CHAT INPUT
# ============================================================

typed_question = st.chat_input(
    "Ask anything about Indian Railways..."
)

if typed_question:

    question_to_process = typed_question


# ============================================================
# PROCESS QUESTION
# ============================================================

if question_to_process:

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": question_to_process
    })

    add_chat_to_history(question_to_process)


    # AI response
    with st.spinner("Railway AI is thinking..."):

        answer = get_ai_response(
            question_to_process
        )


    # Assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# ============================================================
# WELCOME SCREEN
# ============================================================

if not st.session_state.messages:

    st.markdown(
        "<div style='text-align:center; margin-top:100px;'>"
        "<div style='font-size:48px;'>🚆</div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h1 style='text-align:center; color:#111827;'>"
        "How can I help you today?"
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:#6b7280; font-size:14px;'>"
        "Ask me about Indian Railways.<br>"
        "Find trains, routes, stations and schedules using natural language."
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # Suggestion buttons
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🚆  Find trains between two cities",
            use_container_width=True,
            key="welcome_find_trains"
        ):
            st.session_state.pending_question = (
                "Find trains between two cities"
            )
            st.rerun()

        if st.button(
            "📍  Search railway station",
            use_container_width=True,
            key="welcome_station"
        ):
            st.session_state.pending_question = (
                "Search for a railway station"
            )
            st.rerun()

    with col2:

        if st.button(
            "🕐  Get a train schedule",
            use_container_width=True,
            key="welcome_schedule"
        ):
            st.session_state.pending_question = (
                "Give me a train schedule"
            )
            st.rerun()

        if st.button(
            "🔎  Search for a train",
            use_container_width=True,
            key="welcome_search"
        ):
            st.session_state.pending_question = (
                "Search for a train"
            )
            st.rerun()

# ============================================================
# DISPLAY CHAT
# ============================================================

else:

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
Railway database • AI powered by Groq
</div>
""",
    unsafe_allow_html=True
)