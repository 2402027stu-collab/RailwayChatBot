# ============================================================
# RAILWAY AI ROUTER - PROFESSIONAL TERMINAL ASSISTANT
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
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY was not found.\n"
        "Please add GROQ_API_KEY to your .env file."
    )

client = Groq(api_key=GROQ_API_KEY)

MODEL = "openai/gpt-oss-20b"


# ============================================================
# HELPERS
# ============================================================

def compact_result(result, max_chars=6000):
    """
    Keep database results small enough for the AI model.
    """

    if result is None:
        return "[]"

    if isinstance(result, str):
        text = result
    else:
        try:
            text = json.dumps(result, default=str)
        except Exception:
            text = str(result)

    if len(text) > max_chars:
        text = text[:max_chars] + "\n...[results shortened]"

    return text


def safe_json_arguments(arguments):
    """
    Safely convert Groq tool arguments into a dictionary.
    """

    try:
        if isinstance(arguments, dict):
            return arguments

        return json.loads(arguments)

    except Exception:
        return {}


# ============================================================
# TOOL EXECUTOR
# ============================================================

def execute_tool(tool_name, arguments):

    try:

        if tool_name == "train_search":

            return train_search(
                arguments.get("train_number", "")
            )


        elif tool_name == "train_search_by_name":

            return train_search_by_name(
                arguments.get("train_name", "")
            )


        elif tool_name == "route_search":

            return route_search(
                arguments.get("source", ""),
                arguments.get("destination", "")
            )


        elif tool_name == "schedule_search":

            return schedule_search(
                arguments.get("train_number", "")
            )


        elif tool_name == "station_search":

            return station_search(
                arguments.get("station", "")
            )


        elif tool_name == "search_trains_from_station":

            return search_trains_from_station(
                arguments.get("place", "")
            )


        elif tool_name == "search_trains_to_station":

            return search_trains_to_station(
                arguments.get("place", "")
            )


        elif tool_name == "search_trains_passing_station":

            return search_trains_passing_station(
                arguments.get("place", "")
            )


        elif tool_name == "search_trains_terminating_at":

            return search_trains_terminating_at(
                arguments.get("place", "")
            )


        elif tool_name == "database_status":

            return database_status()


        return json.dumps({
            "error": "Unknown railway tool."
        })


    except Exception as e:

        return json.dumps({
            "error": str(e)
        })


# ============================================================
# GROQ TOOL DEFINITIONS
# ============================================================

TOOLS = [

    # --------------------------------------------------------
    # TRAIN NUMBER
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "train_search",

            "description": (
                "Find detailed information about a specific "
                "Indian Railway train using its train number."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "train_number": {

                        "type": "string",

                        "description": (
                            "Indian Railway train number, "
                            "for example 10103 or 12779."
                        )
                    }
                },

                "required": ["train_number"]
            }
        }
    },


    # --------------------------------------------------------
    # TRAIN NAME
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "train_search_by_name",

            "description": (
                "Find trains using a train name or part of "
                "a train name."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "train_name": {

                        "type": "string",

                        "description": (
                            "Train name or part of a train name."
                        )
                    }
                },

                "required": ["train_name"]
            }
        }
    },


    # --------------------------------------------------------
    # ROUTE SEARCH
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "route_search",

            "description": (
                "Find trains travelling between a source "
                "city, state, or railway station and a "
                "destination city, state, or railway station."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "source": {

                        "type": "string",

                        "description": (
                            "Starting city, state, or station."
                        )
                    },

                    "destination": {

                        "type": "string",

                        "description": (
                            "Destination city, state, or station."
                        )
                    }
                },

                "required": [
                    "source",
                    "destination"
                ]
            }
        }
    },


    # --------------------------------------------------------
    # SCHEDULE
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "schedule_search",

            "description": (
                "Find the complete station-by-station "
                "schedule of a train."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "train_number": {

                        "type": "string",

                        "description": (
                            "Train number."
                        )
                    }
                },

                "required": ["train_number"]
            }
        }
    },


    # --------------------------------------------------------
    # STATION
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "station_search",

            "description": (
                "Find information about a railway station "
                "using its name or station code."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "station": {

                        "type": "string",

                        "description": (
                            "Station name or station code."
                        )
                    }
                },

                "required": ["station"]
            }
        }
    },


    # --------------------------------------------------------
    # TRAINS FROM PLACE
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "search_trains_from_station",

            "description": (
                "Find trains stopping at stations in a "
                "specified city, state, or railway station."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "place": {

                        "type": "string",

                        "description": (
                            "City, state, or railway station."
                        )
                    }
                },

                "required": ["place"]
            }
        }
    },


    # --------------------------------------------------------
    # TRAINS TO PLACE
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "search_trains_to_station",

            "description": (
                "Find trains associated with or stopping at "
                "a specified destination city, state, or station."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "place": {

                        "type": "string",

                        "description": (
                            "Destination city, state, "
                            "or railway station."
                        )
                    }
                },

                "required": ["place"]
            }
        }
    },


    # --------------------------------------------------------
    # PASSING STATION
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "search_trains_passing_station",

            "description": (
                "Find trains that stop at or pass through "
                "a specified city, state, or station."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "place": {

                        "type": "string",

                        "description": (
                            "City, state, or station."
                        )
                    }
                },

                "required": ["place"]
            }
        }
    },


    # --------------------------------------------------------
    # TERMINATING TRAINS
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "search_trains_terminating_at",

            "description": (
                "Find trains whose final destination is "
                "a specified city, state, or station."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "place": {

                        "type": "string",

                        "description": (
                            "Final destination city, "
                            "state, or station."
                        )
                    }
                },

                "required": ["place"]
            }
        }
    },


    # --------------------------------------------------------
    # DATABASE STATUS
    # --------------------------------------------------------

    {
        "type": "function",

        "function": {

            "name": "database_status",

            "description": (
                "Check whether the railway database is "
                "available and return basic database statistics."
            ),

            "parameters": {

                "type": "object",

                "properties": {}
            }
        }
    }

]


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are Railway AI, a professional and friendly Indian Railway
assistant.

You help users ask natural questions about Indian Railways.

You can answer questions about:

- trains
- train numbers
- train names
- routes
- cities
- states
- railway stations
- station codes
- train schedules
- arrival times
- departure times
- train type
- distance
- trains stopping at stations
- trains passing through stations
- final destinations
- railway terminology and general railway knowledge

============================================================
IMPORTANT DATABASE RULE
============================================================

The railway database is the source of truth for database-based
railway information.

NEVER invent:

- train numbers
- train names
- station names
- station codes
- arrival times
- departure times
- schedules
- distances
- routes
- railway database facts

If database information is required, use the appropriate tool.

============================================================
UNDERSTAND NATURAL LANGUAGE
============================================================

Users do NOT have to use exact commands.

Examples:

"Can I go from Mumbai to Goa?"

Use route search.

"Any trains from Madgaon to Pune?"

Use route search.

"What trains stop at Thivim?"

Use station/train search.

"Tell me about 12779."

Use train search.

"Give me information about train number 10103."

Use train search.

"What is the schedule of 10103?"

Use schedule search.

"When does 10103 reach Madgaon?"

Use schedule search and answer from the schedule.

"What is MAO?"

Use station search.

"Tell me about Madgaon station."

Use station search.

"Which trains pass through Karmali?"

Use passing-station search.

"Which trains terminate at Goa?"

Use terminating search when appropriate.

"What trains are available in Goa?"

Use station/place train search.

============================================================
FOLLOW-UP QUESTIONS
============================================================

Understand conversational follow-up questions.

Example:

User:
"Tell me about train 12779."

Assistant:
[train information]

User:
"Where does it go?"

Understand that "it" refers to train 12779.

User:
"What time does it reach Pune?"

Use the previous train context and schedule information.

============================================================
AMBIGUOUS QUESTIONS
============================================================

If the user says:

"I want to travel."

Ask:

"Sure! Where are you travelling from and where do you
want to go?"

If only one place is given:

"I want to travel from Goa."

Ask for the destination.

============================================================
LIVE INFORMATION
============================================================

The local database does NOT provide reliable live:

- running status
- current delays
- live location
- PNR status
- current seat availability
- current ticket price

Do not pretend that it does.

If asked for live information, clearly explain that the
current local railway database does not provide live data.

============================================================
GENERAL RAILWAY QUESTIONS
============================================================

For general educational railway questions that do not require
database information, answer naturally using your knowledge.

Examples:

"What is a superfast train?"

"What does AC 2 Tier mean?"

"What is a railway station code?"

"What is the difference between Express and Superfast?"

Keep such answers simple and useful.

============================================================
ANSWER STYLE
============================================================

Be natural and conversational.

Do not mention:

- tool names
- function names
- SQL
- SQLite
- internal code
- database implementation

Do not say:

"I used route_search."

Instead say:

"I found 3 trains between Mumbai and Goa."

Use clean formatting.

For train results, prefer:

🚆 Train Number – Train Name
📍 From → To
🕐 Departure → Arrival
🚄 Type
📏 Distance

Do not invent fields that are missing from the database.

If there are many results, show the most useful results first
and mention that additional results are available.

If no matching database result exists, say so honestly.

============================================================
INDIAN RAILWAY CONTEXT
============================================================

Understand common alternative names.

Examples:

Bombay = Mumbai
Bengaluru = Bangalore
Madgaon = Margao
MAO = Madgaon
Cochin = Kochi
Trivandrum = Thiruvananthapuram

The database tools handle place matching.

============================================================
FINAL RULE
============================================================

Your job is to understand what the user means, select the
correct railway operation, obtain reliable information, and
give the user a natural answer.
"""


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def ask_railway_ai(user_message, conversation=None):

    if conversation is None:
        conversation = []


    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


    # Keep conversation small to avoid token-limit problems
    for message in conversation[-6:]:

        if message.get("role") in ["user", "assistant"]:

            content = message.get("content")

            if content:

                messages.append({
                    "role": message["role"],
                    "content": content
                })


    messages.append({
        "role": "user",
        "content": user_message
    })


    # ========================================================
    # FIRST AI REQUEST
    # ========================================================

    try:

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOLS,

            tool_choice="auto",

            temperature=0.2,

            max_tokens=800
        )

    except Exception as e:

        return {
            "text": (
                "Sorry, I couldn't connect to the Railway AI "
                f"service right now.\n\nError: {e}"
            ),
            "data": None
        }


    assistant_message = response.choices[0].message


    # ========================================================
    # NO TOOL REQUIRED
    # ========================================================

    if not assistant_message.tool_calls:

        return {
            "text": assistant_message.content or
                    "I'm ready to help with Indian Railways.",
            "data": None
        }


    # ========================================================
    # ADD ASSISTANT TOOL CALL MESSAGE
    # ========================================================

    assistant_dict = {
        "role": "assistant",
        "content": assistant_message.content or "",
        "tool_calls": []
    }


    for tool_call in assistant_message.tool_calls:

        assistant_dict["tool_calls"].append({

            "id": tool_call.id,

            "type": "function",

            "function": {

                "name": tool_call.function.name,

                "arguments": tool_call.function.arguments
            }
        })


    messages.append(assistant_dict)


    # ========================================================
    # EXECUTE TOOLS
    # ========================================================

    tool_results = []


    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = safe_json_arguments(
            tool_call.function.arguments
        )


        result = execute_tool(
            tool_name,
            arguments
        )


        result = compact_result(
            result,
            max_chars=5000
        )


        tool_results.append({

            "tool_name": tool_name,

            "result": result
        })


        messages.append({

            "role": "tool",

            "tool_call_id": tool_call.id,

            "name": tool_name,

            "content": result
        })


    # ========================================================
    # SECOND AI REQUEST
    # ========================================================

    try:

        final_response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            temperature=0.2,

            max_tokens=900
        )


        final_text = (
            final_response
            .choices[0]
            .message
            .content
        )


    except Exception as e:

        return {

            "text": (
                "I found the railway information, but I "
                "couldn't format the final response.\n\n"
                f"Error: {e}"
            ),

            "data": tool_results
        }


    return {

        "text": final_text,

        "data": tool_results
    }


# ============================================================
# TERMINAL CHAT
# ============================================================

def main():

    print()
    print("=" * 62)
    print("🚆  INDIAN RAILWAY AI ASSISTANT")
    print("=" * 62)
    print("Ask me anything about Indian Railways.")
    print()
    print("Commands:")
    print("  /help    Show commands")
    print("  /status  Check railway database")
    print("  /clear   Clear conversation")
    print("  /quit    Exit")
    print("=" * 62)


    conversation = []


    while True:

        try:

            user_message = input("\nYou: ").strip()


        except KeyboardInterrupt:

            print("\n\nGoodbye! 🚆")

            break


        except EOFError:

            print("\nGoodbye! 🚆")

            break


        if not user_message:

            continue


        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        if user_message.lower() in [
            "/quit",
            "/exit",
            "quit",
            "exit"
        ]:

            print("\nRailway AI: Goodbye! Have a safe journey. 🚆")

            break


        # ----------------------------------------------------
        # HELP
        # ----------------------------------------------------

        if user_message.lower() == "/help":

            print()
            print("Railway AI can answer questions like:")
            print()
            print("  • Trains from Mumbai to Goa")
            print("  • Trains from Madgaon to Pune")
            print("  • Tell me about train 12779")
            print("  • Schedule of train 10103")
            print("  • What trains stop at Thivim?")
            print("  • Tell me about Karmali station")
            print("  • What is MAO?")
            print("  • What is a Superfast train?")
            print()
            print("Commands:")
            print("  /help")
            print("  /status")
            print("  /clear")
            print("  /quit")

            continue


        # ----------------------------------------------------
        # CLEAR
        # ----------------------------------------------------

        if user_message.lower() == "/clear":

            conversation = []

            print("\nRailway AI: Conversation cleared. 👍")

            continue


        # ----------------------------------------------------
        # DATABASE STATUS
        # ----------------------------------------------------

        if user_message.lower() == "/status":

            result = execute_tool(
                "database_status",
                {}
            )

            print("\nDatabase Status:")

            print(compact_result(result, 3000))

            continue


        # ----------------------------------------------------
        # ASK AI
        # ----------------------------------------------------

        result = ask_railway_ai(
            user_message,
            conversation
        )


        answer = result.get(
            "text",
            "Sorry, I couldn't generate an answer."
        )


        print()
        print("🤖 Railway AI:")
        print(answer)


        # ----------------------------------------------------
        # SAVE CONVERSATION
        # ----------------------------------------------------

        conversation.append({

            "role": "user",

            "content": user_message
        })


        conversation.append({

            "role": "assistant",

            "content": answer
        })


        # Keep memory small
        conversation = conversation[-6:]


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()