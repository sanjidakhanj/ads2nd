import pandas as pd
import networkx as nx
import openpyxl
from itertools import combinations
import matplotlib.pyplot as plt


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
num_stops_data = []
longest_path = []
max_stops = 0
for start, end in combinations(stations, 2):
    try:
        shortest_path = nx.shortest_path(graph, start, end)
        num_stops = len(shortest_path) - 1

        num_stops_data.append(num_stops)

        if num_stops > max_stops:
            max_stops = num_stops
            longest_path = shortest_path

    except nx.NetworkXNoPath:
        continue

plt.hist(num_stops_data, bins=range(1, max(num_stops_data) + 2), edgecolor='black')
plt.title('Histogram of Journey Durations by Number of Stops')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')
plt.show()
print(f"The longest journey by number of stops is from {longest_path[0]} to {longest_path[-1]}")
print(f"Number of stops in longest journey: {max_stops}")
print(f"Path: {longest_path}")