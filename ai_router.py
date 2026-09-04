# ============================================================
# RailwayChatBot - AI Router
# Smart Natural Language + Travel Recommendations
# ============================================================

import os
import json
from dotenv import load_dotenv
from groq import Groq

from railway_tools import (
    train_search,
    train_search_by_name,
    route_search,
    schedule_search,
    station_search,
    search_trains_from_station,
    search_trains_to_station,
    search_trains_passing_station,
    search_trains_terminating_at,
    database_status,
)


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY not found.\n"
        "Please add GROQ_API_KEY to your .env file."
    )

client = Groq(api_key=API_KEY)

MODEL = "openai/gpt-oss-20b"


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are RailwayAI, a professional Indian railway assistant.

You help users find trains, stations, routes and schedules using
the railway database connected to you.

Your most important rule:

DATABASE INFORMATION IS THE SOURCE OF TRUTH.

Never invent railway-specific information.

============================================================
1. NATURAL LANGUAGE
============================================================

Understand different ways users may ask the same question.

Examples:

"Tell me about 12779"
"What is train 12779?"
"Give details of 12779"

These all mean:
Search for train 12779.

Examples:

"Madgaon to Pune"
"Trains from Madgaon to Pune"
"I want to go from Madgaon to Pune"
"How can I travel from Madgaon to Pune?"

These mean:
Search the route between Madgaon and Pune.

============================================================
2. TRAIN INFORMATION
============================================================

For train numbers use train_search.

For train names use train_search_by_name.

For schedules use schedule_search.

For stations use station_search.

============================================================
3. ROUTE SEARCH
============================================================

When the user gives:

SOURCE -> DESTINATION

use route_search.

Examples:

"Goa to Pune"
"Madgaon to Pune"
"Thivim to Bangalore"
"Goa to Maharashtra"

============================================================
4. SMART RECOMMENDATION
============================================================

When the user asks:

"Which train is best?"
"Which one should I take?"
"Best train?"
"Recommend a train"
"Which is faster?"
"Which is better?"

first obtain the actual route results from the database.

Then compare the available results using ONLY the information
returned by the database.

Possible comparison factors:

- departure time
- arrival time
- journey progression shown by the database
- train name
- train number
- availability of route
- user's stated preference

Do NOT invent travel duration if it is not available.

If the user says:

"earliest"

prefer the train with the earliest available departure.

If the user says:

"reach early"

prefer the train with the earliest available destination arrival.

If the user says:

"fastest"

compare available timing information only.

If the database does not provide enough information to determine
which train is objectively fastest, say so and provide the available
options instead.

============================================================
5. MULTIPLE OPTIONS
============================================================

When multiple trains are available, present them clearly.

Example:

1. 12779 — Goa Express
   Madgaon: 15:50
   Pune: 04:00

2. 11098 — Poorna Express
   Madgaon: 15:20
   Pune: 05:05

Then provide a short recommendation based on the user's request.

============================================================
6. FOLLOW-UP QUESTIONS
============================================================

Remember recent conversation.

Example:

User:
Tell me about train 12779.

Assistant:
[train information]

User:
Where does it go?

Understand "it" as train 12779.

User:
What time does it reach Pune?

Continue using train 12779.

User:
What about 11098?

Now switch to train 11098.

============================================================
7. STATIONS
============================================================

Understand common aliases.

Examples:

Madgaon = Margao

Mumbai = Bombay

Bangalore = Bengaluru

Chennai = Madras

Kolkata = Calcutta

Kochi = Cochin

Trivandrum = Thiruvananthapuram

Mysore = Mysuru

Visakhapatnam = Vizag

Vadodara = Baroda

Varanasi = Banaras

Delhi = New Delhi

============================================================
8. GENERAL RAILWAY QUESTIONS
============================================================

Questions such as:

"What is a superfast train?"
"What is a sleeper coach?"
"What is an express train?"

can be answered using general railway knowledge.

Do not present general knowledge as live database information.

============================================================
9. LIVE INFORMATION
============================================================

The current database does not provide reliable live:

- running status
- delays
- PNR status
- seat availability
- current fares
- platform numbers

If asked for these, clearly say that live information is not
available through the current database.

Never pretend database information is live.

============================================================
10. DATABASE LIMITATIONS
============================================================

If no train is found:

"I couldn't find a matching train in the railway database."

If a station is not found:

"I couldn't find that station in the railway database."

Do not fabricate alternatives.

============================================================
11. ANSWER STYLE
============================================================

Be:

- natural
- professional
- concise
- helpful
- friendly

Do not sound like a database.

Do not mention internal Python functions.

Do not mention tool names.

Do not expose implementation details unless the user asks.

Use simple formatting.

============================================================
"""


# ============================================================
# TOOL DEFINITIONS
# ============================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "train_search",
            "description": (
                "Search for a train using its train number."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "train_number": {
                        "type": "string",
                        "description": "Train number."
                    }
                },
                "required": ["train_number"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "train_search_by_name",
            "description": (
                "Search for trains by train name or part of a train name."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Train name."
                    }
                },
                "required": ["name"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "route_search",
            "description": (
                "Find trains between a source and destination. "
                "Use this for travel route questions and recommendations."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Source station, city or state."
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination station, city or state."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of trains.",
                        "default": 20
                    }
                },
                "required": [
                    "source",
                    "destination"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "schedule_search",
            "description": (
                "Get the complete schedule of a train."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "train_number": {
                        "type": "string",
                        "description": "Train number."
                    }
                },
                "required": ["train_number"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "station_search",
            "description": (
                "Find a railway station using station name, "
                "station code, city or state."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Station search query."
                    }
                },
                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_trains_from_station",
            "description": (
                "Find trains stopping at a specified station, city or state."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "place": {
                        "type": "string",
                        "description": "Station, city or state."
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20
                    }
                },
                "required": ["place"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_trains_to_station",
            "description": (
                "Find trains reaching or stopping at a specified place."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "place": {
                        "type": "string",
                        "description": "Destination station, city or state."
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20
                    }
                },
                "required": ["place"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_trains_passing_station",
            "description": (
                "Find trains passing through or stopping at a station."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "place": {
                        "type": "string",
                        "description": "Station, city or station code."
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20
                    }
                },
                "required": ["place"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_trains_terminating_at",
            "description": (
                "Find trains whose final destination is a specified place."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "place": {
                        "type": "string",
                        "description": "Final destination."
                    },
                    "limit": {
                        "type": "integer",
                        "default": 20
                    }
                },
                "required": ["place"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "database_status",
            "description": (
                "Check railway database status and table counts."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(name, arguments):

    try:

        if name == "train_search":

            return train_search(
                arguments.get("train_number", "")
            )

        elif name == "train_search_by_name":

            return train_search_by_name(
                arguments.get("name", "")
            )

        elif name == "route_search":

            return route_search(
                arguments.get("source", ""),
                arguments.get("destination", ""),
                arguments.get("limit", 20)
            )

        elif name == "schedule_search":

            return schedule_search(
                arguments.get("train_number", "")
            )

        elif name == "station_search":

            return station_search(
                arguments.get("query", "")
            )

        elif name == "search_trains_from_station":

            return search_trains_from_station(
                arguments.get("place", ""),
                arguments.get("limit", 20)
            )

        elif name == "search_trains_to_station":

            return search_trains_to_station(
                arguments.get("place", ""),
                arguments.get("limit", 20)
            )

        elif name == "search_trains_passing_station":

            return search_trains_passing_station(
                arguments.get("place", ""),
                arguments.get("limit", 20)
            )

        elif name == "search_trains_terminating_at":

            return search_trains_terminating_at(
                arguments.get("place", ""),
                arguments.get("limit", 20)
            )

        elif name == "database_status":

            return database_status()

        return {
            "error": f"Unknown tool: {name}"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# SAFE JSON
# ============================================================

def safe_json_arguments(raw_arguments):

    if not raw_arguments:
        return {}

    try:
        return json.loads(raw_arguments)

    except Exception:
        return {}


# ============================================================
# COMPACT TOOL RESULT
# ============================================================

def compact_result(result, max_chars=6000):

    try:

        if isinstance(result, str):

            text = result

        else:

            text = json.dumps(
                result,
                ensure_ascii=False,
                default=str
            )

    except Exception:

        text = str(result)

    if len(text) > max_chars:

        text = (
            text[:max_chars]
            + "\n...[additional database results omitted]"
        )

    return text


# ============================================================
# SMART RECOMMENDATION CONTEXT
# ============================================================

def recommendation_hint(user_message):

    """
    Detect the user's recommendation preference.

    This does not make the recommendation itself.
    It only tells the AI what the user appears to prefer.
    """

    text = user_message.lower()

    if any(word in text for word in [
        "earliest",
        "first train",
        "leave early",
        "early departure"
    ]):

        return (
            "\nUSER PREFERENCE DETECTED: "
            "Prefer the earliest available departure."
        )

    if any(word in text for word in [
        "reach early",
        "arrive early",
        "earliest arrival",
        "get there early"
    ]):

        return (
            "\nUSER PREFERENCE DETECTED: "
            "Prefer the earliest available destination arrival."
        )

    if any(word in text for word in [
        "fastest",
        "quickest",
        "fast train"
    ]):

        return (
            "\nUSER PREFERENCE DETECTED: "
            "Prefer the fastest option only when the database "
            "provides enough timing information to support it."
        )

    if any(word in text for word in [
        "best",
        "recommend",
        "recommended",
        "which should",
        "which one should",
        "good option"
    ]):

        return (
            "\nUSER PREFERENCE DETECTED: "
            "Recommend the most suitable option using only "
            "database information and the user's stated preference."
        )

    return ""


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def ask_railway_ai(user_message, conversation=None):

    if conversation is None:
        conversation = []

    history = conversation[-8:]

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": (
                user_message
                + recommendation_hint(user_message)
            )
        }
    )

    # ========================================================
    # FIRST AI CALL
    # ========================================================

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
            max_tokens=900
        )

    except Exception as e:

        return (
            "I couldn't connect to the Railway AI service.\n"
            f"Error: {e}"
        )

    assistant_message = response.choices[0].message

    # ========================================================
    # NO TOOL REQUIRED
    # ========================================================

    if not assistant_message.tool_calls:

        return assistant_message.content or (
            "I couldn't generate a response."
        )

    # ========================================================
    # SAVE ASSISTANT TOOL CALL
    # ========================================================

    assistant_tool_message = {
        "role": "assistant",
        "content": assistant_message.content or "",
        "tool_calls": []
    }

    for tool_call in assistant_message.tool_calls:

        assistant_tool_message["tool_calls"].append(
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            }
        )

    messages.append(assistant_tool_message)

    # ========================================================
    # EXECUTE TOOLS
    # ========================================================

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = safe_json_arguments(
            tool_call.function.arguments
        )

        result = execute_tool(
            tool_name,
            arguments
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": compact_result(result)
            }
        )

    # ========================================================
    # FINAL AI CALL
    # ========================================================

    try:

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=1100
        )

        answer = final_response.choices[0].message.content

        if answer:

            return answer

        return "I couldn't generate a final answer."

    except Exception as e:

        return (
            "I found the railway information, but I couldn't "
            "generate the final response.\n"
            f"Error: {e}"
        )


# ============================================================
# HELP
# ============================================================

def show_help():

    print("""
============================================================
                 🚆 RAILWAY AI HELP
============================================================

You can ask questions naturally.

TRAIN QUESTIONS
----------------

Tell me about train 12779

What is train 12779?

Give me details of 11098


ROUTE QUESTIONS
---------------

What trains go from Madgaon to Pune?

I want to travel from Goa to Pune

Show trains between Madgaon and Pune


SMART RECOMMENDATIONS
---------------------

Which is the best train from Madgaon to Pune?

Which train should I take from Goa to Pune?

Which one is faster?

Show me the best options.

Which train leaves Madgaon first?

Which train reaches Pune earliest?


STATION QUESTIONS
-----------------

Tell me about Karmali station

What is the station code for Madgaon?

What trains stop at Thivim?


SCHEDULE QUESTIONS
-----------------

Show the schedule of train 12779

What time does train 12779 reach Pune?


GENERAL QUESTIONS
-----------------

What is a superfast train?

What is a sleeper coach?


COMMANDS
--------

/help       Show this help
/status     Check database
/clear      Clear conversation
/quit       Exit chatbot

============================================================
""")


# ============================================================
# TERMINAL APPLICATION
# ============================================================

def main():

    print("""
============================================================
              🚆 RAILWAY AI ASSISTANT
============================================================

Welcome to RailwayAI.

I can help you with:

  🚆 Trains
  📍 Stations
  🛤️ Routes
  🕐 Schedules
  ⭐ Smart recommendations
  💬 Natural conversations

Ask your question naturally.

Type /help for examples.
Type /quit to exit.

============================================================
""")

    conversation = []

    while True:

        try:

            user_input = input("\nYou: ").strip()

        except (KeyboardInterrupt, EOFError):

            print("\n\nRailway AI: Goodbye! 👋")
            break

        if not user_input:

            continue

        # ====================================================
        # COMMANDS
        # ====================================================

        if user_input.lower() == "/quit":

            print("\nRailway AI: Goodbye! 🚆")
            break

        if user_input.lower() == "/help":

            show_help()
            continue

        if user_input.lower() == "/clear":

            conversation = []

            print(
                "\nRailway AI: Conversation memory cleared."
            )

            continue

        if user_input.lower() == "/status":

            try:

                status = database_status()

                print("\nRailway AI:")
                print(
                    compact_result(
                        status,
                        max_chars=3000
                    )
                )

            except Exception as e:

                print(
                    f"\nRailway AI: Database error: {e}"
                )

            continue

        # ====================================================
        # AI
        # ====================================================

        print("\nRailway AI: ", end="", flush=True)

        answer = ask_railway_ai(
            user_input,
            conversation
        )

        print(answer)

        # ====================================================
        # MEMORY
        # ====================================================

        conversation.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        conversation.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        conversation = conversation[-8:]


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()