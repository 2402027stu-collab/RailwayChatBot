from search import get_trains_between_route

source = ["NDLS", "NZM", "DLI", "DEE"]
destination = ["MAS", "MS"]

df = get_trains_between_route(source, destination)

print(df)