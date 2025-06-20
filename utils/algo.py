from collections import deque

class GraphEK:
    def __init__(self, N):
        self.N = N
        self.capacity = [[0]*N for _ in range(N)]
        self.adj = [[] for _ in range(N)]

    def add_edge(self, u, v, cap):
        if v not in self.adj[u]: self.adj[u].append(v)
        if u not in self.adj[v]: self.adj[v].append(u)
        self.capacity[u][v] += cap

    def max_flow(self, source, sink):
        flow = 0
        parent = [-1]*self.N
        while True:
            for i in range(self.N): parent[i] = -1
            parent[source] = source
            q = deque([source])
            while q and parent[sink] == -1:
                u = q.popleft()
                for v in self.adj[u]:
                    if self.capacity[u][v] > 0 and parent[v] == -1:
                        parent[v] = u; q.append(v)
                        if v == sink: break
            if parent[sink] == -1: break
            bottleneck = float('inf'); v = sink
            while v != source:
                u = parent[v]
                bottleneck = min(bottleneck, self.capacity[u][v])
                v = u
            v = sink
            while v != source:
                u = parent[v]
                self.capacity[u][v] -= bottleneck
                self.capacity[v][u] += bottleneck
                v = u
            flow += bottleneck
        return flow