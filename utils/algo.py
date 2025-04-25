from collections import deque
import math


class RoadTracker:
    def __init__(self):
        # Zbior uzywanych drog
        self.used_roads = set()
        # Slownik przechowujacy przeplywy przez poszczegolne drogi
        self.road_flows = {}

    def mark_used(self, road_id, flow=1):
        # Dodaje droge do zbioru uzywanych drog
        # i aktualizuje sume przeplywow przez te droge
        self.used_roads.add(road_id)
        if road_id not in self.road_flows:
            self.road_flows[road_id] = 0
        self.road_flows[road_id] += flow

    def get_total_cost(self, city):
        # Zwraca sume kosztow napraw uzywanych drog
        return sum(road.repair_cost for road in city.roads if road.id in self.used_roads)

    def get_roads_with_flows(self):
        # Zwraca slownik z przeplywami przez poszczegolne drogi
        return self.road_flows


class Edge:
    def __init__(self, to, rev, capacity, cost, road_id=None):
        # Krawedz skierowana w grafie
        self.to = to        # Wezel docelowy
        self.rev = rev      # Indeks krawedzi przeciwnej
        self.capacity = capacity  # Maksymalna przepustowosć
        self.flow = 0       # Aktualny przeplyw
        self.cost = cost    # Koszt uzycia krawedzi
        self.road_id = road_id  # ID drogi (jesli dotyczy)


class Graph:
    def __init__(self):
        # Inicjalizacja grafu
        self.nodes = []      # Lista wezlow
        self.node_map = {}   # Mapowanie nazw wezlow na indeksy
        self.node_id_counter = 0  # Licznik ID wezlow
        self.edge_list = []  # Lista krawedzi (do debugowania)

    def add_node(self, name):
        # Dodaje wezel do grafu jesli nie istnieje
        # i zwraca jego indeks
        if name not in self.node_map:
            self.node_map[name] = self.node_id_counter
            self.node_id_counter += 1
            self.nodes.append([])
        return self.node_map[name]

    def add_edge(self, fr_name, to_name, capacity, cost, road_id=None):
        # Dodaje krawedz do grafu wraz z krawedzia przeciwna
        fr = self.add_node(fr_name)
        to = self.add_node(to_name)

        forward_rev = len(self.nodes[to])
        forward_edge = Edge(to, forward_rev, capacity, cost, road_id)

        backward_rev = len(self.nodes[fr])
        backward_edge = Edge(fr, backward_rev, 0, -cost, road_id)

        self.nodes[fr].append(forward_edge)
        self.nodes[to].append(backward_edge)

        # Dla celow debugowania
        self.edge_list.append((fr_name, to_name, capacity, cost, road_id))

        return forward_edge, backward_edge

    def get_node_id(self, name):
        # Zwraca ID wezla o podanej nazwie
        return self.node_map.get(name)


def build_flow_network(city):
    # Buduje sieć przeplywowa dla problemu dystrybucji jeczmienia i piwa
    graph = Graph()

    # Wezly zrodla i ujscia
    super_source = "super_source"
    super_sink = "super_sink"
    source_id = graph.add_node(super_source)
    sink_id = graph.add_node(super_sink)

    # Dodanie pol (zrodel jeczmienia)
    for field in city.fields:
        field_node = f"field_{field.id}"
        field_coord = f"coord_{field.x}_{field.y}"

        graph.add_node(field_node)
        graph.add_node(field_coord)

        # Polaczenie zrodla z polem
        graph.add_edge(super_source, field_node, field.sector_yield, 0)

        # Polaczenie pola z jego wspolrzednymi
        graph.add_edge(field_node, field_coord, math.inf, 0)

    # Dodanie browarow (przetwarzanie jeczmienia na piwo)
    for brewery in city.breweries:
        brewery_in = f"brewery_{brewery.id}_in"
        brewery_out = f"brewery_{brewery.id}_out"
        brewery_coord = f"coord_{brewery.x}_{brewery.y}"

        graph.add_node(brewery_in)
        graph.add_node(brewery_out)
        graph.add_node(brewery_coord)

        # Polaczenie wspolrzednych z wejsciem browaru
        graph.add_edge(brewery_coord, brewery_in, math.inf, 0)

        # Ograniczenie przepustowosci browaru
        graph.add_edge(brewery_in, brewery_out, brewery.capacity, 0)

        # Polaczenie wyjscia browaru z powrotem do sieci
        graph.add_edge(brewery_out, brewery_coord, math.inf, 0)

    # Dodanie karczm (odbiorcow piwa)
    for inn in city.inns:
        inn_node = f"inn_{inn.id}"
        inn_coord = f"coord_{inn.x}_{inn.y}"

        graph.add_node(inn_node)
        graph.add_node(inn_coord)

        # Polaczenie wspolrzednych z karczma
        graph.add_edge(inn_coord, inn_node, math.inf, 0)

        # Polaczenie karczmy z ujsciem
        graph.add_edge(inn_node, super_sink, inn.demand, 0)

    # Dodanie drog (polaczen miedzy lokalizacjami)
    for road in city.roads:
        from_x, from_y = road.start
        to_x, to_y = road.end

        from_coord = f"coord_{from_x}_{from_y}"
        to_coord = f"coord_{to_x}_{to_y}"

        # Dodanie drogi w obu kierunkach
        graph.add_edge(from_coord, to_coord, road.capacity, road.repair_cost, road.id)
        graph.add_edge(to_coord, from_coord, road.capacity, road.repair_cost, road.id)

    return graph, source_id, sink_id


def min_cost_flow(graph, source, sink, city):
    # Oblicza maksymalny przeplyw o minimalnym koszcie
    n = len(graph.nodes)
    max_flow = 0
    road_tracker = RoadTracker()

    # Inicjalizacja potencjalow
    potential = [0] * n

    # Glowna petla algorytmu
    while True:
        # Inicjalizacja odleglosci
        dist = [math.inf] * n
        prev = [None] * n
        prev_edge = [None] * n
        dist[source] = 0

        # Kolejka dla algorytmu
        queue = deque([source])
        in_queue = [False] * n
        in_queue[source] = True

        # Znajdowanie najkrotszej sciezki
        while queue:
            node = queue.popleft()
            in_queue[node] = False

            for i, edge in enumerate(graph.nodes[node]):
                if edge.capacity > 0:
                    next_node = edge.to
                    reduced_cost = edge.cost + potential[node] - potential[next_node]
                    new_dist = dist[node] + reduced_cost

                    if new_dist < dist[next_node]:
                        dist[next_node] = new_dist
                        prev[next_node] = node
                        prev_edge[next_node] = i

                        if not in_queue[next_node]:
                            queue.append(next_node)
                            in_queue[next_node] = True

        # Jesli nie ma sciezki do ujscia, konczymy
        if dist[sink] == math.inf:
            break

        # Aktualizacja potencjalow
        for i in range(n):
            if dist[i] < math.inf:
                potential[i] += dist[i]

        # Obliczenie minimalnej przepustowosci na sciezce
        min_capacity = math.inf
        node = sink
        while node != source:
            p = prev[node]
            edge = graph.nodes[p][prev_edge[node]]
            min_capacity = min(min_capacity, edge.capacity)
            node = p

        # Aktualizacja przeplywow
        node = sink
        while node != source:
            p = prev[node]
            edge_idx = prev_edge[node]
            edge = graph.nodes[p][edge_idx]

            if edge.road_id is not None and edge.cost > 0:
                road_tracker.mark_used(edge.road_id, min_capacity)

            edge.capacity -= min_capacity
            edge.flow += min_capacity
            reverse_edge = graph.nodes[edge.to][edge.rev]
            reverse_edge.capacity += min_capacity

            node = p

        max_flow += min_capacity

    # Obliczenie kosztu
    total_cost = road_tracker.get_total_cost(city)

    # Wyswietlenie informacji o drogach
    print("\n--- Road Usage Details ---")
    road_flows = road_tracker.get_roads_with_flows()
    for road_id, flow in sorted(road_flows.items()):
        road = next((r for r in city.roads if r.id == road_id), None)
        if road:
            print(f"Road {road_id}: {road.start} to {road.end}, Flow: {flow}, Cost: {road.repair_cost}")

    return max_flow, total_cost