import heapq
import random
import time
import matplotlib.pyplot as plt

# ---------------- Union-Find for Kruskal ----------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        rx = self.find(x)
        ry = self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True

# ---------------- Kruskal ----------------
def kruskal(n, edges):
    edges.sort()
    uf = UnionFind(n)
    mst = []
    cost = 0
    for w, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            if len(mst) == n - 1:
                break
    return mst, cost

# ---------------- Prim ----------------
def prim(n, adj, start=0):
    INF = float("inf")
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0
    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost

# ---------------- Sample Graph ----------------
n = 15
edges = [
    (7, 2, 1),
    (3, 0, 3),
    (8, 1, 2),
    (9, 1, 7),
    (7, 5, 4),
    (5, 3, 4),
    (15, 3, 4),
    (6, 3, 5),
    (10, 4, 5),
    (9, 4, 14),
    (11, 5, 6)
]

adj = {}
for w, u, v in edges:
    adj.setdefault(u, []).append((v, w))
    adj.setdefault(v, []).append((u, w))

k_mst, k_cost = kruskal(n, edges[:])
p_mst, p_cost = prim(n, adj)

print("===== Kruskal's MST =====")
for u, v, w in k_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total MST Cost =", k_cost)
print()
print("===== Prim's MST =====")
for u, v, w in p_mst:
    print(f"Edge ({u} - {v})  Weight = {w}")
print("Total MST Cost =", p_cost)

# ---------------- Performance Analysis ----------------
sizes = [50, 100, 200, 400, 800]
kruskal_time = []
prim_time = []

for n in sizes:
    edges = []
    for i in range(n - 1):
        edges.append((random.randint(1, 100), i, i + 1))
    for _ in range(n):
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u != v:
            edges.append((random.randint(1, 100), u, v))

    adj = {}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))

    start = time.perf_counter()
    kruskal(n, edges[:])
    kruskal_time.append((time.perf_counter() - start) * 1000)

    start = time.perf_counter()
    prim(n, adj)
    prim_time.append((time.perf_counter() - start) * 1000)

# ---------------- Graph ----------------
plt.figure(figsize=(8, 5))
plt.plot(sizes, kruskal_time, marker='o', label="Kruskal's Algorithm")
plt.plot(sizes, prim_time, marker='s', label="Prim's Algorithm")
plt.xlabel("Number of Vertices (n)")
plt.ylabel("Time (ms)")
plt.title("Kruskal vs Prim - Time Complexity Comparison")
plt.legend()
plt.grid(True)
plt.savefig("mst_performance_graph.png")
plt.show()