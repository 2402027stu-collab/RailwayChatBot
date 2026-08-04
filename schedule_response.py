from ai_engine import ask_ai

def generate_schedule_response(schedule_df):

    schedule_text = ""

    for _, row in schedule_df.iterrows():
        schedule_text += (
            f"Station: {row['station_name']}, "
            f"Arrival: {row['arrival']}, "
            f"Departure: {row['departure']}, "
            f"Day: {row['day']}\n"
        )

    prompt = f"""
Explain the following railway schedule in a clean and readable format.

{schedule_text}
"""

    return ask_ai(prompt)