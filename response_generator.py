from ai_engine import ask_ai

def generate_train_response(train):

    prompt = f"""
Explain this train information in a friendly way.

Train Number : {train['number']}
Train Name : {train['name']}
From : {train['from_station_name']}
To : {train['to_station_name']}
Departure : {train['departure']}
Arrival : {train['arrival']}
Distance : {train['distance']} km
Zone : {train['zone']}
Train Type : {train['type']}
"""

    return ask_ai(prompt)