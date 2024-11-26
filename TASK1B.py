import time
import random
from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph
from generate_random_graph import generate_random_graph

# Function to generate an artificial tube network (graph) with n stations
def generate_tube_network(num_stations, edge_density=0.08):
    # edge_density controls how many edges there will be in the network
    return generate_random_graph(num_stations, edge_density, True, True, True, 1, 10)  # Edge weights between 1 and 10

# Function to measure execution time for Dijkstra's algorithm
def measure_execution_time(graph, start_station):
    start_time = time.time()  # Record start time
    dijkstra(graph, start_station)  # Run Dijkstra's algorithm from the start station
    end_time = time.time()  # Record end time
    return (end_time - start_time) * 1000  # Return time in milliseconds

# Main code for Task 1b: Measure execution times for varying network sizes
network_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
execution_times = []

for size in network_sizes:
    # Generate a network with 'size' stations
    graph = generate_tube_network(size)

    avg_time = 0
    for _ in range(20):  # Measure time for 20 station pairs to get average execution time
        start_station = random.randint(0, size - 1)  # Randomly select a start station
        avg_time += measure_execution_time(graph, start_station)

    avg_time /= 20  # Calculate average execution time for this network size
    execution_times.append(avg_time)
    print(f"Network Size: {size}, Average Execution Time: {avg_time:.2f} ms")

# Output the final results as a table for plotting the graph later
for size, time in zip(network_sizes, execution_times):
    print(f"Network Size: {size}, Average Execution Time: {time:.2f} ms")


print(graph)