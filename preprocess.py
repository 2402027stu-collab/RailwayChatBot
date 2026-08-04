import pandas as pd

# Load JSON files
trains = pd.read_json("Data/trains.json")
stations = pd.read_json("Data/stations.json")
schedules = pd.read_json("Data/schedules.json")

# -----------------------------
# Extract train properties
# -----------------------------
train_data = []

for feature in trains["features"]:
    train_data.append(feature["properties"])

train_df = pd.DataFrame(train_data)

# -----------------------------
# Extract station properties
# -----------------------------
station_data = []

for feature in stations["features"]:
    station_data.append(feature["properties"])

station_df = pd.DataFrame(station_data)

# -----------------------------
# Show information
# -----------------------------
print("========== TRAIN DATA ==========")
print(train_df.head())

print("\n========== TRAIN COLUMNS ==========")
print(train_df.columns)

print("\n========== STATION DATA ==========")
print(station_df.head())

print("\n========== STATION COLUMNS ==========")
print(station_df.columns)

# -----------------------------
# Save cleaned CSV files
# -----------------------------
train_df.to_csv("Data/clean_trains.csv", index=False)
station_df.to_csv("Data/clean_stations.csv", index=False)
schedules.to_csv("Data/clean_schedules.csv", index=False)

print("\n✅ Cleaned CSV files created successfully!")