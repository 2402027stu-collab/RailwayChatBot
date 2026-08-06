def generate_train_response(train):
    return f"""
### 🚆 Train Details

**Train Number:** {train['number']}
**Train Name:** {train['name']}
**From:** {train['from_station_name']}
**To:** {train['to_station_name']}
**Departure:** {train['departure']}
**Arrival:** {train['arrival']}
**Distance:** {train['distance']} km
**Type:** {train['type']}
**Zone:** {train['zone']}
"""