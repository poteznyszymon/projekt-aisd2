from collections import deque
import math

class RoadTracker:
    def __init__(self):
        self.used_roads = set()

    def mark_used(self, road_id):
        self.used_roads.add(road_id)

    def get_total_cost(self, city):
        return sum(road.repair_cost for road in city.roads if road.id in self.used_roads)

class Edge:
    def __init__(self, to, rev, capacity, cost):
        self.to = to
        self.rev = rev
        self.capacity = capacity
        self.cost = cost


class Graph:
    def __init__(self):
        self.nodes = []
        self.node_map = {}
        self.node_id_counter = 0

    def add_node(self, name):
        if name not in self.node_map:
            self.node_map[name] = self.node_id_counter
            self.node_id_counter += 1
            self.nodes.append([])
        return self.node_map[name]

    def add_edge(self, fr_name, to_name, capacity, cost):
        fr = self.add_node(fr_name)
        to = self.add_node(to_name)

        forward_rev = len(self.nodes[to])
        forward_edge = Edge(to, forward_rev, capacity, cost)

        backward_rev = len(self.nodes[fr])
        backward_edge = Edge(fr, backward_rev, 0, -cost)

        self.nodes[fr].append(forward_edge)
        self.nodes[to].append(backward_edge)


def build_flow_network(city):
    graph = Graph()

    super_source_name = "super_source"
    super_sink_name = "super_sink"
    graph.add_node(super_source_name)
    graph.add_node(super_sink_name)

    for field in city.fields:
        field_node_name = f"field_{field.id}"
        graph.add_edge(super_source_name, field_node_name, field.sector_yield, 0)

    breweries_in = {}
    breweries_out = {}
    for brewery in city.breweries:
        in_node_name = f"brewery_{brewery.id}_in"
        out_node_name = f"brewery_{brewery.id}_out"
        graph.add_edge(in_node_name, out_node_name, brewery.capacity, 0)
        breweries_in[brewery.id] = in_node_name
        breweries_out[brewery.id] = out_node_name

    for inn in city.inns:
        inn_node_name = f"inn_{inn.id}"
        graph.add_edge(inn_node_name, super_sink_name, inn.demand, 0)

    for road in city.roads:
        from_node_name = tuple(road.start)
        to_node_name = tuple(road.end)
        graph.add_edge(from_node_name, to_node_name, road.capacity, road.repair_cost)
        graph.add_edge(to_node_name, from_node_name, road.capacity, road.repair_cost)

    for field in city.fields:
        field_coord = (field.x, field.y)
        field_node_name = f"field_{field.id}"
        road_node_name = tuple(field_coord)
        if road_node_name in graph.node_map:
            graph.add_edge(field_node_name, road_node_name, math.inf, 0)

    for brewery in city.breweries:
        coord = (brewery.x, brewery.y)
        road_node_name = tuple(coord)
        if road_node_name in graph.node_map:
            brewery_in_name = breweries_in[brewery.id]
            graph.add_edge(road_node_name, brewery_in_name, math.inf, 0)

    for brewery in city.breweries:
        coord = (brewery.x, brewery.y)
        road_node_name = tuple(coord)
        if road_node_name in graph.node_map:
            brewery_out_name = breweries_out[brewery.id]
            graph.add_edge(brewery_out_name, road_node_name, math.inf, 0)

    for inn in city.inns:
        coord = (inn.x, inn.y)
        road_node_name = tuple(coord)
        if road_node_name in graph.node_map:
            inn_node_name = f"inn_{inn.id}"
            graph.add_edge(road_node_name, inn_node_name, math.inf, 0)

    return graph, graph.node_map[super_source_name], graph.node_map[super_sink_name]


def min_cost_flow(graph, source, sink, city):
    n = len(graph.nodes)
    flow = 0
    cost = 0
    prev = [None] * n
    potential = [0] * n
    road_tracker = RoadTracker()

    while True:
        dist = [math.inf] * n
        inqueue = [False] * n
        dist[source] = 0
        q = deque([source])

        while q:
            u = q.popleft()
            inqueue[u] = False
            for i, e in enumerate(graph.nodes[u]):
                if e.capacity > 0 and dist[e.to] > dist[u] + e.cost + potential[u] - potential[e.to]:
                    dist[e.to] = dist[u] + e.cost + potential[u] - potential[e.to]
                    prev[e.to] = (u, i)
                    if not inqueue[e.to]:
                        q.append(e.to)
                        inqueue[e.to] = True

        if dist[sink] == math.inf:
            break

        for i in range(n):
            potential[i] += dist[i] if dist[i] < math.inf else 0

        delta = math.inf
        v = sink
        path_edges = []
        while v != source:
            u, i = prev[v]
            e = graph.nodes[u][i]
            path_edges.append(e)
            delta = min(delta, e.capacity)
            v = u

        for e in path_edges:
            for road in city.roads:
                if (e.cost == road.repair_cost and road.repair_cost > 0):
                    road_tracker.mark_used(road.id)

        v = sink
        while v != source:
            u, i = prev[v]
            e = graph.nodes[u][i]
            e.capacity -= delta
            graph.nodes[e.to][e.rev].capacity += delta
            v = u

        flow += delta

    total_cost = road_tracker.get_total_cost(city)
    return flow, total_cost