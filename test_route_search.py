from search import get_trains_between_route, get_station_codes

source_df = get_station_codes("Mumbai")
destination_df = get_station_codes("Delhi")

source_codes = source_df["code"].dropna().unique().tolist()
destination_codes = destination_df["code"].dropna().unique().tolist()

print("Mumbai codes:")
print(source_codes)

print("\nDelhi codes:")
print(destination_codes)

trains = get_trains_between_route(
    source_codes,
    destination_codes
)

print("\n========== TRAINS ==========")
print(trains.to_string(index=False))