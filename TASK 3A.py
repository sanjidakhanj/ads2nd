import pandas as pd
import networkx as nx
import openpyxl
from itertools import combinations


file_path = 'C:/Users/nmali/Desktop/ADVANCED ADS CW/London Underground data.xlsx'
data = pd.read_excel(file_path, header=None, engine='openpyxl')

data.columns = ["Tube Line", "Tube Station", "End Destination", "Duration in Minutes"]
data = data.drop_duplicates(subset=["Tube Station", "End Destination", "Duration in Minutes"])

graph = nx.Graph()

for index, row in data.iterrows():
    line = row["Tube Line"]
    start_station = row["Tube Station"]
    end_station = row["End Destination"]
    duration = row["Duration in Minutes"]

    graph.add_edge(start_station, end_station, weight=duration, line=line)


stations = list(graph.nodes)
station_pairs = list(combinations(stations, 2))

results = []

for start, end in station_pairs:
    try:
        shortest_path = nx.dijkstra_path(graph, start, end, weight="weight")
        path_duration = nx.dijkstra_path_length(graph, start, end, weight='weight')
        results.append((start, end, path_duration, shortest_path))
    except nx.NetworkXNoPath:
        results.append((start, end, float('inf'),[]))

for start, end, duration, path in results:
    print(f"Shortest path from {start} to {end}: Duration = {duration} minutes, Path = {path}")


for start, end, duration, path in results:
    print(f"Shortest path from {start} to {end}: Duration = {duration} minutes, Path = {path}")

#Amount of journeys
valid_journey_count = sum(1 for _, _, duration, _ in results if duration != float('inf'))
print(f"Total number of journeys calculated: {valid_journey_count}")

#Calculating shortest path

longest_path = []
longest_duration = 0

stations = list(graph.nodes)
for start, end in combinations(stations, 2):
    try:
        path_duration = nx.dijkstra_path_length(graph, start, end, weight='weight')

        if path_duration > longest_duration:
            longest_duration = path_duration
            longest_path = nx.dijkstra_path(graph, start, end, weight='weight')

    except nx.NetworkXNoPath:
        continue


print(f"The longest path (shortest paths) is from {longest_path[0]} to {longest_path[-1]}")
print(f"Duration of longest path: {longest_duration} minutes")
print(f"Path: {longest_path}")