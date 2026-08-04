import pandas as pd

# Load JSON files
trains = pd.read_json("Data/trains.json")
stations = pd.read_json("Data/stations.json")
schedules = pd.read_json("Data/schedules.json")

print("===== TRAINS COLUMNS =====")
print(trains.columns)

print("\n===== STATIONS COLUMNS =====")
print(stations.columns)

print("\n===== SCHEDULES COLUMNS =====")
print(schedules.columns)

print("\n===== FIRST TRAIN FEATURE =====")
print(trains["features"][0])

print("\n===== FIRST STATION FEATURE =====")
print(stations["features"][0])