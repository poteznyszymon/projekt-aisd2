from collections import deque
from itertools import combinations
import math

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

def bruteforce(city):
    # Szukanie najtańszego zbioru dróg do naprawy (bruteforce)

    # Tworzenie listy punktów (pola, browary, karczmy)
    physical = []
    for f in city.fields:
        physical.append((f.x, f.y, f.id, 'field'))
    for b in city.breweries:
        physical.append((b.x, b.y, b.id, 'brewery'))
    for inn in city.inns:
        physical.append((inn.x, inn.y, inn.id, 'inn'))

    P = len(physical)
    source = 0
    barley_start = 1
    beer_start = barley_start + P
    sink = beer_start + P
    N = sink + 1

    barley_nodes = {}
    beer_nodes = {}
    for idx, (x, y, _id, _type) in enumerate(physical):
        barley_nodes[(x, y)] = barley_start + idx
        beer_nodes[(x, y)] = beer_start + idx

    roads = city.roads
    paid_ids = [r.id for r in roads if r.repair_cost > 0]
    zero_set = {r.id for r in roads if r.repair_cost == 0}
    cost_map = {r.id: r.repair_cost for r in roads}

    total_supply = sum(f.sector_yield for f in city.fields)
    max_flow, min_cost, used_roads = -1, math.inf, set()

    for rcount in range(len(paid_ids) + 1):
        for combo in combinations(paid_ids, rcount):
            repaired = zero_set.union(combo)
            cost_combo = sum(cost_map[rid] for rid in combo)
            if max_flow == total_supply and cost_combo >= min_cost:
                continue
            g = GraphEK(N)
            # Dodanie krawędzi ze źródła do pól (jęczmień)
            for f in city.fields:
                g.add_edge(source, barley_nodes[(f.x, f.y)], f.sector_yield)
            # Dodanie krawędzi pomiędzy punktami (jęczmień)
            for r in roads:
                if r.id in repaired:
                    u0, v0 = tuple(r.start), tuple(r.end)
                    if u0 in barley_nodes and v0 in barley_nodes:
                        u, v = barley_nodes[u0], barley_nodes[v0]
                        g.add_edge(u, v, r.capacity)
                        g.add_edge(v, u, r.capacity)
            # Przetworzenie jęczmienia na piwo w browarach
            for b in city.breweries:
                u = barley_nodes[(b.x, b.y)]
                v = beer_nodes[(b.x, b.y)]
                g.add_edge(u, v, b.capacity)
            # Dodanie krawędzi pomiędzy punktami (piwo)
            for r in roads:
                if r.id in repaired:
                    u0, v0 = tuple(r.start), tuple(r.end)
                    if u0 in beer_nodes and v0 in beer_nodes:
                        u, v = beer_nodes[u0], beer_nodes[v0]
                        g.add_edge(u, v, r.capacity)
                        g.add_edge(v, u, r.capacity)
            # Dodanie krawędzi z karczm do ujścia
            for inn in city.inns:
                u = beer_nodes[(inn.x, inn.y)]
                g.add_edge(u, sink, inn.demand)
            flow = g.max_flow(source, sink)
            if flow > max_flow or (flow == max_flow and cost_combo < min_cost):
                max_flow, min_cost, used_roads = flow, cost_combo, repaired
        if max_flow == total_supply:
            break

    return max_flow, min_cost, used_roads