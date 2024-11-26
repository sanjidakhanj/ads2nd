import dijkstra as d
import min_heap_priority_queue
from adjacency_list_graph import AdjacencyListGraph
from bellman_ford import bellman_ford
from generate_random_graph import generate_random_graph
from single_source_shortest_paths import initialize_single_source, relax

london_underground_names = ['A', 'B', 'C', 'D', 'E']
london_underground_edges = [('A', 'B', 5), ('A', 'C', 5), ('B', 'D', 6),
                           ('B', 'E', 2), ('C', 'D', 1), ('C', 'E', 3),
                           ('D', 'E', 1), ('D', 'A', 15), ('E', 'B', 4,), ('E', 'C', 7)]

# Creating the graph
graph1 = AdjacencyListGraph(len(london_underground_names), True, True)

# Inserting the edges(distance/time taken) for each vertex into the graph
for edge in london_underground_edges:
    graph1.insert_edge(london_underground_names.index(edge[0]), london_underground_names.index(edge[1]), edge[2])

start = input("What station are you starting at?").upper()
end = input("Where will you like to go").upper()

# Verifies input before running Dijkstra's algorithm

if start not in london_underground_names or end not in london_underground_names:
    print("Invalid Station Names")
else:
    d, pi = d.dijkstra(graph1, london_underground_names.index(start))

    print(f"Shortest distant from {start} to {end}: {d[london_underground_names.index(end)]}")

    # Creating the shortest path from start to end
    path = []
    current_vertex = london_underground_names.index(end)
    while current_vertex is not None:
        path.insert(0, london_underground_names[current_vertex])
        current_vertex = pi[current_vertex]

    print(f"shortest path: {' to '.join(path)}")
