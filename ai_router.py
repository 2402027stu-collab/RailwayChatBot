import os
import json
import re

from dotenv import load_dotenv
from groq import Groq

from railway_tools import (
    search_train,
    search_route,
    search_schedule,
    search_station,
    search_train_stations,
    search_trains_from_station,
    search_trains_to_station,
    database_status
)


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "Please add GROQ_API_KEY=your_key to .env"
    )


client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# AI INTENT PROMPT
# ============================================================

INTENT_PROMPT = """
You are the intent detection system for an Indian Railway
AI Assistant.

Your job is ONLY to understand what the user wants.

Return ONLY valid JSON.
Do not return markdown.
Do not return explanations.

Available intents:

1. train
   Use when the user asks about a particular train.

2. route
   Use when the user asks for trains between a source
   and destination.

3. schedule
   Use when the user asks about the timetable or schedule
   of a particular train.

4. train_stations
   Use when the user asks where a train stops or which
   stations a train visits.

5. station
   Use when the user asks about a railway station.

6. trains_from
   Use when the user asks which trains start from a station.

7. trains_to
   Use when the user asks which trains go to or arrive at
   a station.

8. database
   Use ONLY if the user explicitly asks about the database,
   such as number of train records or station records.

9. general
   Use for greetings, help, capabilities, or general
   railway-related conversation.

10. unknown
   Use when the request is unrelated to railway information
   or cannot be understood.

JSON FORMAT:

{
    "intent": "route",
    "source": "Mumbai",
    "destination": "Goa",
    "train_number": "",
    "station": "",
    "search_text": ""
}

RULES:

- For "Mumbai to Goa":
  intent = route
  source = Mumbai
  destination = Goa

- For "Which trains go to Goa?":
  intent = trains_to
  station = Goa

- For "What trains go to Mumbai?":
  intent = trains_to
  station = Mumbai

- For "What trains start from Mumbai?":
  intent = trains_from
  station = Mumbai

- For "Tell me about train 10103":
  intent = train
  train_number = 10103

- For "What is train 10103?":
  intent = train
  train_number = 10103

- For "Show schedule of 10103":
  intent = schedule
  train_number = 10103

- For "When does 10103 arrive?":
  intent = schedule
  train_number = 10103

- For "Where does 10103 stop?":
  intent = train_stations
  train_number = 10103

- For "Which stations does 10103 visit?":
  intent = train_stations
  train_number = 10103

- For "What is Karmali station?":
  intent = station
  station = Karmali

- For "Tell me about Madgaon":
  intent = station
  station = Madgaon

- For "How many trains are in your database?":
  intent = database

- For "Hello":
  intent = general

- For "What can you do?":
  intent = general

Never invent train numbers or station names.
"""


# ============================================================
# GET AI INTENT
# ============================================================

def get_intent(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": INTENT_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0,
        max_tokens=300
    )

    text = response.choices[0].message.content.strip()

    # --------------------------------------------------------
    # Remove markdown JSON fences if model adds them
    # --------------------------------------------------------

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:

        data = json.loads(text)

    except json.JSONDecodeError:

        # Try to find JSON inside the response
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if match:

            try:
                data = json.loads(match.group(0))

            except json.JSONDecodeError:

                return {
                    "intent": "unknown",
                    "source": "",
                    "destination": "",
                    "train_number": "",
                    "station": "",
                    "search_text": ""
                }

        else:

            return {
                "intent": "unknown",
                "source": "",
                "destination": "",
                "train_number": "",
                "station": "",
                "search_text": ""
            }

    # --------------------------------------------------------
    # Make sure all expected fields exist
    # --------------------------------------------------------

    fields = [
        "intent",
        "source",
        "destination",
        "train_number",
        "station",
        "search_text"
    ]

    for field in fields:

        if field not in data:
            data[field] = ""

    return data


# ============================================================
# EXECUTE RAILWAY SEARCH
# ============================================================

def execute_search(intent):

    try:

        # ----------------------------------------------------
        # TRAIN
        # ----------------------------------------------------

        if intent["intent"] == "train":

            train_number = intent.get(
                "train_number",
                ""
            )

            search_text = intent.get(
                "search_text",
                ""
            )

            value = train_number or search_text

            if not value:

                return {
                    "error": "Please provide a train number or name."
                }

            return search_train(value)

        # ----------------------------------------------------
        # ROUTE
        # ----------------------------------------------------

        elif intent["intent"] == "route":

            source = intent.get(
                "source",
                ""
            )

            destination = intent.get(
                "destination",
                ""
            )

            if not source or not destination:

                return {
                    "error": (
                        "Please provide both source "
                        "and destination."
                    )
                }

            return search_route(
                source,
                destination
            )

        # ----------------------------------------------------
        # SCHEDULE
        # ----------------------------------------------------

        elif intent["intent"] == "schedule":

            train_number = intent.get(
                "train_number",
                ""
            )

            if not train_number:

                return {
                    "error": "Please provide a train number."
                }

            return search_schedule(
                train_number
            )

        # ----------------------------------------------------
        # TRAIN STATIONS
        # ----------------------------------------------------

        elif intent["intent"] == "train_stations":

            train_number = intent.get(
                "train_number",
                ""
            )

            if not train_number:

                return {
                    "error": "Please provide a train number."
                }

            return search_train_stations(
                train_number
            )

        # ----------------------------------------------------
        # STATION
        # ----------------------------------------------------

        elif intent["intent"] == "station":

            station = intent.get(
                "station",
                ""
            )

            search_text = intent.get(
                "search_text",
                ""
            )

            value = station or search_text

            if not value:

                return {
                    "error": "Please provide a station name."
                }

            return search_station(value)

        # ----------------------------------------------------
        # TRAINS FROM
        # ----------------------------------------------------

        elif intent["intent"] == "trains_from":

            station = intent.get(
                "station",
                ""
            )

            if not station:

                return {
                    "error": "Please provide a station."
                }

            return search_trains_from_station(
                station
            )

        # ----------------------------------------------------
        # TRAINS TO
        # ----------------------------------------------------

        elif intent["intent"] == "trains_to":

            station = intent.get(
                "station",
                ""
            )

            if not station:

                return {
                    "error": "Please provide a station."
                }

            return search_trains_to_station(
                station
            )

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        elif intent["intent"] == "database":

            return database_status()

        # ----------------------------------------------------
        # GENERAL
        # ----------------------------------------------------

        elif intent["intent"] == "general":

            return None

        # ----------------------------------------------------
        # UNKNOWN
        # ----------------------------------------------------

        return None

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# FINAL AI RESPONSE
# ============================================================

def generate_answer(
    question,
    intent,
    database_result,
    conversation=None
):

    if conversation is None:
        conversation = []

    # --------------------------------------------------------
    # GENERAL QUESTIONS
    # --------------------------------------------------------

    if database_result is None:

        prompt = f"""
You are Railway Assistant.

User question:
{question}

Answer naturally and professionally.

You can help with:
- Train information
- Train routes
- Train schedules
- Train stops
- Railway stations
- Trains from a station
- Trains going to a station
- Railway database information

If the user is greeting you, greet them.

If the user asks what you can do, explain your capabilities.

If the user wants to travel but did not provide enough
information, ask for the source and destination.

If the question is unrelated to Indian Railways, politely
explain that you are a Railway Assistant.

Do not invent railway facts.
"""

    else:

        # Convert database result to JSON
        result_text = json.dumps(
            database_result,
            ensure_ascii=False,
            default=str
        )

        prompt = f"""
You are a professional Indian Railway Assistant.

User question:
{question}

Detected intent:
{intent.get("intent")}

Verified railway database result:
{result_text}

IMPORTANT:

The database result is the source of truth.

NEVER invent railway information.

Use ONLY information present in the database result.

If the database result says no information was found,
clearly tell the user that no matching information was found.

Give the answer in a clear and readable format.

For multiple trains, use a clean numbered list or table.

For a schedule, clearly show:
- Station
- Arrival
- Departure
- Day

For train information, clearly show relevant details.

For route searches, show:
- Train number
- Train name
- Source
- Destination
- Type
- Distance

Do not mention internal Python functions,
database implementation, AI routing,
or technical details.

Do not say that you used a tool.

Answer the user's actual question directly.
"""

    messages = [
        {
            "role": "system",
            "content": prompt
        }
    ]

    # --------------------------------------------------------
    # ADD SHORT CONVERSATION HISTORY
    # --------------------------------------------------------

    for message in conversation[-6:]:

        if (
            isinstance(message, dict)
            and "role" in message
            and "content" in message
        ):

            messages.append({
                "role": message["role"],
                "content": str(message["content"])
            })

    # --------------------------------------------------------
    # CURRENT QUESTION
    # --------------------------------------------------------

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=2000
    )

    return response.choices[0].message.content


# ============================================================
# MAIN FUNCTION
# ============================================================

def ask_railway_ai(
    question,
    conversation=None
):

    if not question or not question.strip():

        return "Please enter a railway question."

    question = question.strip()

    # --------------------------------------------------------
    # STEP 1: UNDERSTAND USER
    # --------------------------------------------------------

    intent = get_intent(question)

    # --------------------------------------------------------
    # STEP 2: GET DATABASE INFORMATION
    # --------------------------------------------------------

    database_result = execute_search(
        intent
    )

    # --------------------------------------------------------
    # STEP 3: GENERATE NATURAL RESPONSE
    # --------------------------------------------------------

    answer = generate_answer(
        question,
        intent,
        database_result,
        conversation
    )

    return answer


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 65)
    print("🚆 RAILWAY AI ROUTER TEST")
    print("=" * 65)

    while True:

        question = input(
            "\nAsk Railway Assistant: "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "bye"
        }:
            print("\n👋 Goodbye!")
            break

        if not question:
            continue

        print()
        print("🤖 AI:")
        print()

        try:

            answer = ask_railway_ai(
                question
            )

            print(answer)

        except Exception as e:

            print("❌ Error:")
            print(e)