# ============================================================
# AI ROUTER - INDIAN RAILWAY ASSISTANT
# ============================================================

import os
import json
import pandas as pd

from dotenv import load_dotenv
from groq import Groq

from city_mapping import get_station_codes


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY was not found. "
        "Please add it to your .env file."
    )


client = Groq(api_key=GROQ_API_KEY)


# ============================================================
# IMPORT YOUR DATABASE FUNCTIONS
# ============================================================

from search import (
    get_train_by_number,
    get_schedule,
    get_station,
    get_trains_between_route
)


# ============================================================
# HELPER
# ============================================================

def dataframe_to_json(df):

    if df is None:
        return "[]"

    if isinstance(df, pd.DataFrame):

        if df.empty:
            return "[]"

        return json.dumps(
            df.fillna("").to_dict(orient="records"),
            default=str
        )

    return json.dumps(df, default=str)


# ============================================================
# TOOL 1 - TRAIN SEARCH
# ============================================================

def train_search(train_number):

    try:

        result = get_train_by_number(str(train_number))

        return dataframe_to_json(result)

    except Exception as e:

        return json.dumps({
            "error": str(e)
        })


# ============================================================
# TOOL 2 - TRAIN SCHEDULE
# ============================================================

def schedule_search(train_number):

    try:

        result = get_schedule(str(train_number))

        return dataframe_to_json(result)

    except Exception as e:

        return json.dumps({
            "error": str(e)
        })


# ============================================================
# TOOL 3 - STATION SEARCH
# ============================================================

def station_search(station):

    try:

        station_text = str(station).strip()

        # First try city/station mapping
        codes = get_station_codes(station_text)

        # If mapping returns station codes,
        # search each station code
        if codes:

            results = []

            for code in codes:

                result = get_station(code)

                if result is not None:

                    results.append(result)

            if results:

                combined = pd.concat(
                    results,
                    ignore_index=True
                )

                combined = combined.drop_duplicates()

                return dataframe_to_json(combined)

        # Otherwise search the provided value directly
        result = get_station(station_text.upper())

        return dataframe_to_json(result)

    except Exception as e:

        return json.dumps({
            "error": str(e)
        })


# ============================================================
# TOOL 4 - ROUTE SEARCH
# ============================================================

def route_search(source, destination):

    try:

        source = str(source).strip()
        destination = str(destination).strip()

        source_codes = get_station_codes(source)
        destination_codes = get_station_codes(destination)

        # If source is already a station code
        if not source_codes:
            source_codes = [source.upper()]

        # If destination is already a station code
        if not destination_codes:
            destination_codes = [destination.upper()]

        result = get_trains_between_route(
            source_codes,
            destination_codes
        )

        return dataframe_to_json(result)

    except Exception as e:

        return json.dumps({
            "error": str(e)
        })


# ============================================================
# GROQ TOOL DEFINITIONS
# ============================================================

TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "train_search",

            "description": (
                "Search for information about a specific train "
                "using its train number."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "train_number": {
                        "type": "string",
                        "description": (
                            "The 5 digit Indian railway train number."
                        )
                    }

                },

                "required": ["train_number"]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "route_search",

            "description": (
                "Find trains travelling from a source city or station "
                "to a destination city or station."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "source": {
                        "type": "string",
                        "description": (
                            "Starting city or railway station."
                        )
                    },

                    "destination": {
                        "type": "string",
                        "description": (
                            "Destination city or railway station."
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

    {
        "type": "function",

        "function": {

            "name": "schedule_search",

            "description": (
                "Find the complete station-by-station schedule "
                "for a train."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "train_number": {
                        "type": "string",
                        "description": (
                            "The train number."
                        )
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
                "Find information about a railway station using "
                "its name or station code."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "station": {
                        "type": "string",
                        "description": (
                            "Railway station name or station code."
                        )
                    }

                },

                "required": ["station"]
            }
        }
    }
]


# ============================================================
# TOOL EXECUTOR
# ============================================================

def execute_tool(tool_name, arguments):

    if tool_name == "train_search":

        return train_search(
            arguments["train_number"]
        )

    elif tool_name == "route_search":

        return route_search(
            arguments["source"],
            arguments["destination"]
        )

    elif tool_name == "schedule_search":

        return schedule_search(
            arguments["train_number"]
        )

    elif tool_name == "station_search":

        return station_search(
            arguments["station"]
        )

    return json.dumps({
        "error": "Unknown tool"
    })


# ============================================================
# MAIN AI FUNCTION
# ============================================================

def ask_railway_ai(user_message, conversation=None):
    if conversation is None:
        conversation = []

    system_message = """
    You are Railway Assistant, an intelligent Indian Railway chatbot.

    Your job is to help users with:

    1. Train information
    2. Trains between cities or stations
    3. Train schedules
    4. Railway station information

    IMPORTANT RULES:

    - Use the provided tools to obtain railway information.
    - NEVER invent train numbers, train names, stations, schedules,
      distances or railway information.
    - The railway database is the source of truth.
    - If the user asks for trains between two places,
      use route_search.
    - If the user gives a train number and asks for information,
      use train_search.
    - If the user asks for a schedule,
      use schedule_search.
    - If the user asks about a station,
      use station_search.
    - If required information is missing, politely ask the user
      for the missing information.
    - If the request is not related to Indian Railways, politely
      explain that you are a railway assistant.
    - Keep answers clear and easy to understand.
    - Only offer information that can be obtained using the available tools.
    - Do not claim that fare, seat availability, live train status, booking,
      or other information is available unless a tool provides it.
    - If the user asks for information that the tools cannot provide,
      clearly say that the information is not currently available.
    - Do not guess or make up missing railway information.
    - When showing route results, use the actual source and destination
      stations returned by the railway database.
    - Do not expose tool names or internal database details to the user.

    Examples:

    User: "Mumbai to Goa"
    Action: route_search

    User: "Find trains from Mumbai to Delhi"
    Action: route_search

    User: "Tell me about train 10103"
    Action: train_search

    User: "Show schedule of 10103"
    Action: schedule_search

    User: "What is Karmali station?"
    Action: station_search

    User: "I want to travel"
    Response: Ask for source and destination.
    """

    messages = [

        {
            "role": "system",
            "content": system_message
        }

    ]

    # Add previous conversation
    for message in conversation[-10:]:

        messages.append({
            "role": message["role"],
            "content": message["content"]
        })

    # Add current user message
    messages.append({
        "role": "user",
        "content": user_message
    })


    # ========================================================
    # FIRST GROQ REQUEST
    # ========================================================

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=messages,

        tools=TOOLS,

        tool_choice="auto",

        temperature=0.2,

        max_tokens=1000
    )


    assistant_message = response.choices[0].message


    # ========================================================
    # NO TOOL REQUIRED
    # ========================================================

    if not assistant_message.tool_calls:

        return {
            "text": assistant_message.content,
            "data": None
        }


    # ========================================================
    # ADD ASSISTANT TOOL CALL
    # ========================================================

    messages.append(
        assistant_message
    )


    tool_results = []


    # ========================================================
    # EXECUTE TOOLS
    # ========================================================

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        result = execute_tool(
            tool_name,
            arguments
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
    # SECOND GROQ REQUEST
    # ========================================================

    final_response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=messages,

        temperature=0.2,

        max_tokens=1500
    )


    final_text = final_response.choices[0].message.content


    return {

        "text": final_text,

        "data": tool_results
    }
if __name__ == "__main__":

    question = input(
        "Ask Railway Assistant: "
    )

    result = ask_railway_ai(question)

    print()
    print("AI:")
    print(result["text"])