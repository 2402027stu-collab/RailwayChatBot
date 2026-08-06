def generate_station_response(station):
    return f"""
### 🚉 Station Details

**Code:** {station['code']}
**Name:** {station['name']}
**State:** {station['state']}
**Address:** {station['address']}
"""