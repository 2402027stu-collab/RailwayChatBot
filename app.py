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

st.set_page_config(
    page_title="Indian Railway AI Chatbot",
    page_icon="🚆",
    layout="wide"
)

st.title("🚆 Indian Railway AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user = st.chat_input("Ask me anything about Indian Railways...")

if user:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user}
    )

    with st.chat_message("user"):
        st.markdown(user)

    # ==========================================
    # NLP
    # ==========================================

    intent = detect_intent(user)
    train_number = extract_train_number(user)
    station_code = extract_station_code(user)
    source, destination = extract_source_destination(user)

    # ==========================================
    # TRAIN DETAILS
    # ==========================================

    if intent == "train":

        train = get_train_by_number(train_number)

        if len(train) > 0:
            reply = generate_train_response(train.iloc[0])
        else:
            reply = "❌ Train not found."

    # ==========================================
    # STATION DETAILS
    # ==========================================

    elif intent == "station":

        if station_code:

            if isinstance(station_code, list):
                code = station_code[0]
            else:
                code = station_code

            station = get_station(code)

            if len(station) > 0:
                reply = generate_station_response(station.iloc[0])
            else:
                reply = "❌ Station not found."

        else:
            reply = "❌ Please enter a valid station code."

    # ==========================================
    # TRAIN SCHEDULE
    # ==========================================

    elif intent == "schedule":

        if train_number:

            schedule = get_schedule(train_number)

            if len(schedule) > 0:
                reply = generate_schedule_response(schedule)
            else:
                reply = "❌ Schedule not found."

        else:
            reply = "❌ Please enter a valid train number."

    # ==========================================
    # TRAINS BETWEEN TWO CITIES
    # ==========================================

    elif intent == "between":

        if source and destination:

            source_df = get_station_codes(source)

            if len(source_df) > 0:
                source_codes = source_df["code"].tolist()
            else:
                source_codes = [source.upper()]

            destination_df = get_station_codes(destination)

            if len(destination_df) > 0:
                destination_codes = destination_df["code"].tolist()
            else:
                destination_codes = [destination.upper()]

            trains = get_trains_between_route(
                source_codes,
                destination_codes
            )

            trains = trains.drop_duplicates(subset=["number"])

            if len(trains) == 0:

                reply = "❌ No trains found."

            else:

                reply = f"✅ Found {len(trains)} train(s)."

                st.dataframe(trains)

        else:

            reply = "❌ Please enter both source and destination."

    # ==========================================
    # UNKNOWN
    # ==========================================

    else:

        reply = "❌ Sorry, I didn't understand your question."

    # ==========================================
    # DISPLAY REPLY
    # ==========================================

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )