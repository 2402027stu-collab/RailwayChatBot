def generate_schedule_response(schedule):

    reply = "### 🚆 Train Schedule\n\n"

    for _, row in schedule.iterrows():
        reply += (
            f"- {row['station_name']} ({row['station_code']}) | "
            f"Arrival: {row['arrival']} | "
            f"Departure: {row['departure']}\n"
        )

    return reply