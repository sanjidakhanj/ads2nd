from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from bfs import bfs
import matplotlib.pyplot as plt


# To read CSV file for creating a graph
def read_csv(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()[1:]  # To skip the header line from the CSV file
        data = [line.strip().split(',') for line in lines]
    return data


# To create a graph with station names to unique indices
def create_and_process_graph(london_underground_data):
    station_to_indices = {}
    index_counter = 0
    for row in london_underground_data:
        for station in row[:2]:  # Only takes data from the first two columns as station names
            if station not in station_to_indices:
                station_to_indices[station] = index_counter
                index_counter += 1

    num_stations = len(station_to_indices)
    data_graph = AdjacencyListGraph(num_stations, directed=False,
                                    weighted=True)  # To initialize graph with the number of stations

    # Add edges to the graph
    for row in london_underground_data:
        u = station_to_indices[row[0]]
        v = station_to_indices[row[1]]
        weight = int(row[2].strip().strip('"'))
        if not data_graph.has_edge(u, v):
            data_graph.insert_edge(u, v, weight)

    return data_graph, station_to_indices


# To find shortest path durations for all pairs of nodes in the graph
def compute_all_pairs_durations(graph):
    durations = []
    for start_node in range(graph.card_V):
        distances, _ = bfs(graph, start_node)  # Or use Dijkstra's algorithm
        durations.extend([dist for dist in distances if dist < float('inf')])
    return durations


# To find the longest shortest path (diameter) in the graph
def find_longest_path(graph):
    max_path_duration = 0
    for start_node in range(graph.card_V):
        distances, _ = bfs(graph, start_node)
        max_path_duration = max(max_path_duration, max(distances))
    return max_path_duration


# To plot a histogram of journey durations
def plot_histogram(durations, title):
    plt.hist(durations, bins=20, color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel("Journey Duration (minutes)")
    plt.ylabel("Frequency")
    plt.show()


# To compare histograms of journey durations before and after closures
def compare_histograms(durations_before, durations_after):
    plt.hist(durations_before, bins=20, color='skyblue', alpha=0.7, label='Before Closures', edgecolor='black')
    plt.hist(durations_after, bins=20, color='orange', alpha=0.7, label='After Closures', edgecolor='black')
    plt.title("Comparison of Journey Durations")
    plt.xlabel("Journey Duration (minutes)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()




if __name__ == "__main__":
    csv_data = read_csv("london_underground_graph.csv")

    if csv_data:
        full_graph, station_to_index = create_and_process_graph(csv_data)


        durations_before = compute_all_pairs_durations(full_graph)
        longest_path_before = find_longest_path(full_graph)
        plot_histogram(durations_before, "Journey Durations Before Closures")


        mst = kruskal(full_graph)
        edges_to_shut = [edge for edge in full_graph.get_edge_list() if edge not in mst.get_edge_list()]
        for u, v in edges_to_shut:
            full_graph.delete_edge(u, v)


        durations_after = compute_all_pairs_durations(full_graph)
        longest_path_after = find_longest_path(full_graph)
        plot_histogram(durations_after, "Journey Durations After Closures")


        compare_histograms(durations_before, durations_after)
        print(f"Longest Path Duration Before Closures: {longest_path_before} minutes")
        print(f"Longest Path Duration After Closures: {longest_path_after} minutes")
