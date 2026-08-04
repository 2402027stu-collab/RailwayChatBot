import search

print("Imported search.py from:")
print(search.__file__)

from search import (
    get_train_by_number,
    get_schedule,
    get_station,
    get_station_codes,
    get_trains_between_route
)

from response_generator import generate_train_response
from schedule_response import generate_schedule_response
from station_response import generate_station_response

from nlp import (
    extract_train_number,
    extract_station_code,
    extract_source_destination,
    detect_intent
)

print("=" * 50)
print("🚆 Indian Railway AI Chatbot")
print("Type 'exit' to quit")
print("=" * 50)

while True:

    user = input("\nYou : ")

    if user.lower() == "exit":
        print("\nBot : Thank you for using Indian Railway AI Chatbot.")
        break

    # =====================================
    # NLP
    # =====================================

    intent = detect_intent(user)

    train_number = extract_train_number(user)

    station_code = extract_station_code(user)

    source, destination = extract_source_destination(user)

    print("\n========== NLP ==========")
    print("Intent :", intent)
    print("Source :", source)
    print("Destination :", destination)
    print("=========================\n")

    # =====================================
    # TRAINS BETWEEN TWO CITIES / STATIONS
    # =====================================

    if intent == "between":

        if source and destination:

            # Automatically find all station codes
            source_df = get_station_codes(source)

            if len(source_df) > 0:
                source_stations = source_df["code"].tolist()
            else:
                source_stations = [source.upper()]

            destination_df = get_station_codes(destination)

            if len(destination_df) > 0:
                destination_stations = destination_df["code"].tolist()
            else:
                destination_stations = [destination.upper()]

            print("\n========== DEBUG ==========")
            print("Source City :", source)
            print("Destination City :", destination)
            print("Source Stations :", source_stations)
            print("Destination Stations :", destination_stations)
            print("===========================\n")

            trains = get_trains_between_route(
                source_stations,
                destination_stations
            )

            print("\nReturned rows:", len(trains))
            print(trains)

            if len(trains) > 0:

                print("\n===================================================")
                print(f"🚆 Found {len(trains)} Train(s)")
                print("===================================================")

                trains = trains.sort_values(by="number")
                trains = trains.drop_duplicates(subset=["number"])

                for i, (_, row) in enumerate(trains.iterrows(), start=1):
                    print(f"\nTrain {i}")
                    print("---------------------------------------------------")
                    print(f"Train Number : {row['number']}")
                    print(f"Train Name   : {row['name']}")
                    print(f"From         : {row['source_station']}")
                    print(f"To           : {row['destination_station']}")
                    print(f"Type         : {row['type']}")
                    print(f"Distance     : {row['distance']} km")
            else:

                print("\nBot : No trains found.")

        else:

            print("\nBot : Please enter source and destination.")

    # =====================================
    # STATION INFORMATION
    # =====================================

    elif intent == "station":

        if station_code:

            station = get_station(station_code)

            if len(station) > 0:

                print("\nBot :")
                print(generate_station_response(station.iloc[0]))

            else:

                print("\nBot : Station not found.")

        else:

            print("\nBot : Please enter a valid station code.")

    # =====================================
    # TRAIN DETAILS
    # =====================================

    elif intent == "train" and train_number:

        train = get_train_by_number(train_number)

        if len(train) > 0:

            print("\nBot :")
            print(generate_train_response(train.iloc[0]))

        else:

            print("\nBot : Train not found.")

    # =====================================
    # TRAIN SCHEDULE
    # =====================================

    elif intent == "schedule" and train_number:

        schedule = get_schedule(train_number)

        if len(schedule) > 0:

            print("\nBot :")
            print(generate_schedule_response(schedule))

        else:

            print("\nBot : Schedule not found.")

    # =====================================
    # UNKNOWN
    # =====================================

    else:

        print("\nBot : Sorry, I didn't understand your question.")