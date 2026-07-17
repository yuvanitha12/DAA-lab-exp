import heapq
import matplotlib.pyplot as plt


def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap
    Time: O((V + E) log V), Space: O(V)
    graph: dict {u: [(v, weight), ...]}, 0-indexed
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev


def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path[0] == source:
        return path
    return []


# --- Graph Definition (Adjacency List) ---
graph = {
    0: [(1, 4), (2, 1)],
    1: [(3, 1)],
    2: [(1, 2), (3, 5)],
    3: [(4, 3)],
    4: [(5, 2)],
    5: []
}

source = 0
dist, prev = dijkstra(graph, source)

print(f'Shortest paths from vertex {source}:')
print(f'{"Vertex":>8} {"Distance":>10} {"Path":>30}')
print('-' * 55)
for v in range(len(graph)):
    path = reconstruct_path(prev, source, v)
    path_str = ' -> '.join(map(str, path)) if path else 'No path'
    d = dist[v] if dist[v] != float('inf') else 'INF'
    print(f'{v:>8} {str(d):>10} {path_str:>30}')

# ---------------- TIME & SPACE COMPLEXITY ----------------
print("\nComplexity Summary")
print("-" * 55)
print(f"{'Metric':<20}{'Complexity':<20}")
print(f"{'Time':<20}{'O((V + E) log V)':<20}")
print(f"{'Space':<20}{'O(V)':<20}")

# ---------------- GRAPH 1: Distance Bar Chart ----------------
vertices = list(range(len(graph)))
distances = [dist[v] if dist[v] != float('inf') else 0 for v in vertices]

plt.figure(figsize=(7, 5))
bars = plt.bar(vertices, distances, color='steelblue')
plt.xlabel("Vertex")
plt.ylabel("Shortest Distance from Source")
plt.title(f"Dijkstra's Algorithm - Shortest Distances from Vertex {source}")
plt.xticks(vertices)
plt.grid(axis='y')
for bar, d in zip(bars, distances):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
              str(d), ha='center')
plt.savefig("dijkstra_distances.png")
plt.show()

# ---------------- GRAPH 2: Network Visualization ----------------
try:
    import networkx as nx

    G = nx.DiGraph()
    for u in graph:
        for v, w in graph[u]:
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(7, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=800, arrowsize=20, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Graph Structure (Edge Weights Shown)")
    plt.savefig("dijkstra_graph_structure.png")
    plt.show()
except ImportError:
    print("\n(networkx not installed - skipping graph structure visualization)")
    print("Run: py -m pip install networkx  to enable it")