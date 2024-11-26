import time
import random
import networkx as nx
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph

# Define fixed node positions for visualization
fixed_positions = {
    0: (0, 0), 1: (1, 1), 2: (3, 1), 3: (5, 1.5), 4: (1, -1)
}
index_to_label = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
label_to_index = {v: k for k, v in index_to_label.items()}

def convert_path_to_labels(path):
    """Convert a list of node indices to labels, generating 'Node_<index>' for unknown nodes."""
    return [index_to_label.get(node, f"Node_{node}") for node in path]

# Task 2a: Create Journey Time-Based and Stop-Based Networks
def create_journey_time_network():
    num_stations = 5
    graph = AdjacencyListGraph(num_stations, weighted=True)
    graph.insert_edge(0, 1, 5)  # A -> B: 5 minutes
    graph.insert_edge(1, 2, 7)  # B -> C: 7 minutes
    graph.insert_edge(2, 3, 3)  # C -> D: 3 minutes
    graph.insert_edge(3, 4, 2)  # D -> E: 2 minutes
    graph.insert_edge(0, 2, 10) # A -> C: 10 minutes
    graph.insert_edge(1, 3, 8)  # B -> D: 8 minutes
    return graph

def create_stop_based_network():
    num_stations = 5
    graph = AdjacencyListGraph(num_stations, weighted=False)
    graph.insert_edge(0, 1)  # A -> B: 1 stop
    graph.insert_edge(1, 2)  # B -> C: 1 stop
    graph.insert_edge(2, 3)  # C -> D: 1 stop
    graph.insert_edge(3, 4)  # D -> E: 1 stop
    graph.insert_edge(0, 2)  # A -> C: 1 stop
    graph.insert_edge(1, 3)  # B -> D: 1 stop
    return graph

def add_default_weights_for_stops(graph):
    for u in range(graph.get_card_V()):
        for edge in graph.get_adj_list(u):
            edge.weight = 1  # Set weight attribute to 1 for stops

# Function to calculate shortest path based on journey time
def calculate_shortest_path_journey_time(graph, start_station, destination_station):
    start_time = time.time()
    distances, predecessors = dijkstra(graph, start_station)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

    path = []
    current = destination_station
    while current is not None:
        path.append(current)
        current = predecessors[current] if predecessors[current] != -1 else None
    path.reverse()
    journey_time = distances[destination_station]
    labeled_path = convert_path_to_labels(path)
    print("**Journey Time Path Calculation:**")
    print(f"- Path: {labeled_path}")
    print(f"- Total Cost: {journey_time} minutes")
    print(f"- Execution Time: {execution_time:.2f} ms\n")
    return path, journey_time, execution_time

# Function to calculate shortest path based on stops
def calculate_shortest_path_stops(graph, start_station, destination_station):
    start_time = time.time()
    distances, predecessors = dijkstra(graph, start_station)
    end_time = time.time()
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

    path = []
    current = destination_station
    while current is not None:
        path.append(current)
        current = predecessors[current] if predecessors[current] != -1 else None
    path.reverse()
    stops = distances[destination_station]
    labeled_path = convert_path_to_labels(path)
    print("**Stop-Based Path Calculation:**")
    print(f"- Path: {labeled_path}")
    print(f"- Total Cost: {stops} stops")
    print(f"- Execution Time: {execution_time:.2f} ms\n")
    return path, stops, execution_time

# Compare paths based on journey time and stops
def compare_journey_time_and_stops():
    journey_time_graph = create_journey_time_network()
    stop_based_graph = create_stop_based_network()
    add_default_weights_for_stops(stop_based_graph)

    start_station, destination_station = 0, 4

    journey_time_path, journey_time_cost, journey_time_exec = calculate_shortest_path_journey_time(
        journey_time_graph, start_station, destination_station)
    stops_path, stops_cost, stops_exec = calculate_shortest_path_stops(
        stop_based_graph, start_station, destination_station)

    # Visualizing the graphs (optional)
    journey_edges = [(journey_time_path[i], journey_time_path[i+1]) for i in range(len(journey_time_path) - 1)]
    stop_edges = [(stops_path[i], stops_path[i+1]) for i in range(len(stops_path) - 1)]

    visualize_graph(journey_time_graph, "Journey Time-Based Network with Shortest Path", shortest_path_edges=journey_edges)
    visualize_graph(stop_based_graph, "Stop-Based Network with Shortest Path", shortest_path_edges=stop_edges)

# Visualize the graph with highlighted paths
def visualize_graph(graph, title, shortest_path_edges=None):
    plt.figure(figsize=(10, 6))
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from(fixed_positions.keys())
    for u in range(graph.get_card_V()):
        for edge in graph.get_adj_list(u):
            nx_graph.add_edge(u, edge.v, weight=edge.weight)
    
    nx.draw(nx_graph, fixed_positions, with_labels=True, labels=index_to_label, node_size=500, node_color="skyblue", 
            font_weight="bold", edge_color="gray", width=2)
    if shortest_path_edges:
        nx.draw_networkx_edges(nx_graph, fixed_positions, edgelist=shortest_path_edges, edge_color="red", width=3)
    edge_labels = nx.get_edge_attributes(nx_graph, 'weight')
    nx.draw_networkx_edge_labels(nx_graph, fixed_positions, edge_labels=edge_labels, font_size=10)
    plt.title(title)
    plt.axis('off')
    plt.show()
    plt.close()  # Clear the plot to avoid overlapping issues

# Task 2b: Measure execution time for various network sizes
def measure_execution_time_stops():
    network_sizes = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
    execution_times_stops = []
    for size in network_sizes:
        graph = AdjacencyListGraph(size, weighted=False)
        for i in range(size):
            for j in range(i + 1, size):
                if random.random() < 0.05:
                    graph.insert_edge(i, j)
        add_default_weights_for_stops(graph)

        start_station = random.randint(0, size - 1)
        destination_station = random.randint(0, size - 1)

        exec_time_sum = 0
        trials = 5
        for _ in range(trials):
            _, _, exec_time = calculate_shortest_path_stops(graph, start_station, destination_station)
            exec_time_sum += exec_time

        avg_exec_time = exec_time_sum / trials
        execution_times_stops.append(avg_exec_time)
        print(f"**Network Size: {size}**")
        print(f"- Average Execution Time: {avg_exec_time:.2f} ms\n")

    plt.plot(network_sizes, execution_times_stops, label='Stop-Based Execution Time', marker='o')
    plt.xlabel('Network Size (n)')
    plt.ylabel('Average Execution Time (ms)')
    plt.title('Execution Time vs. Network Size (Stop-Based)')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.close()  # Clear the plot to avoid overlapping issues

# Execute Task 2a
print("=== Task 2a: Code-Based Execution ===")
compare_journey_time_and_stops()

# Execute Task 2b
measure_execution_time_stops()
