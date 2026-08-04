from ai_engine import ask_ai

def generate_station_response(station):

    prompt = f"""
You are an Indian Railway Assistant.

Explain the following station information in a friendly and readable format.

Station Name : {station['name']}
Station Code : {station['code']}
State        : {station['state']}
Zone         : {station['zone']}
Address      : {station['address']}

Do not invent information.
"""

    return ask_ai(prompt)