from models.field import Field
from models.inn import Inn
from models.breweries import Breweries
from models.road import Road

class Edge:
    def __init__(self, to: int, capacity: int, cost: int):
        self.to = to              # numer wierzchołka docelowego
        self.capacity = capacity  # przepustowość
        self.cost = cost          # koszt naprawy drogi
        self.rev = None           # wskaźnik na krawędź odwrotną (do pozniejszego obliczania przeplywu)

class Graph:
    def __init__(self):
        self.graph = {}  # słownik: wierzchołek -> lista krawędzi
    
    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
    
    def add_edge(self, start, end, capacity, cost=0):
        forward = Edge(end, capacity, cost)
        backward = Edge(start, 0, -cost)  # krawędź odwrotna: 0 capacity i przeciwny koszt
        forward.rev = backward
        backward.rev = forward
        self.graph[start].append(forward)
        self.graph[end].append(backward)
        
    def print_graph(self):
        for node, edges in self.graph.items():
            print(f"Wierzchołek {node}:")
            visited_edges = set()  # Set do sledzenia odwiedzonych kraeędzi
            
            for edge in edges:
                # Sprawdzamy czy krawedz odwrotna zostala juz wydrukowana
                if (edge.to, edge.rev.to) not in visited_edges and (edge.rev.to, edge.to) not in visited_edges:
                    print(f"  -> {edge.to} | capacity: {edge.capacity} | cost: {edge.cost}")
                    visited_edges.add((node, edge.to))  # Dodajemy krawedz
                    visited_edges.add((edge.to, node))  # Dodajemy krawedz odwrotna
            print()


def build_flow_graph(fields: list[Field], breweries: list[Breweries], inns: list[Inn], roads: list[Road]) -> Graph:
    graph = Graph()
    
    node_id = 0
    point_to_node = {}

    # 1. Dodajemy source (sztuczny poczatkowy wiercholek dla sieci przeplywowej)
    source = node_id
    graph.add_node(source)
    node_id += 1

    # 2. Pola
    for field in fields:
        point = (field.x, field.y)
        point_to_node[point] = node_id
        graph.add_node(node_id)
        node_id += 1

    # 3. Browary
    for brewery in breweries:
        point = (brewery.x, brewery.y)
        point_to_node[point] = node_id
        graph.add_node(node_id)
        node_id += 1

    # 4. Karczmy
    for inn in inns:
        point = (inn.x, inn.y)
        point_to_node[point] = node_id
        graph.add_node(node_id)
        node_id += 1

    # 5. Dodajemy sink (sztuczny ostatni wiercholek dla sieci przeplywowej)
    sink = node_id
    graph.add_node(sink)
    node_id += 1

    # 6. Krawędzie Source -> Pola
    for field in fields:
        field_node = point_to_node[(field.x, field.y)]
        graph.add_edge(source, field_node, field.sector_yield, cost=0)

    # 7. Krawędzie na podstawie dróg (między polami, browarami, karczmami)
    for road in roads:
        from_point = tuple(road.start)
        to_point = tuple(road.end)

        if from_point in point_to_node and to_point in point_to_node:
            from_node = point_to_node[from_point]
            to_node = point_to_node[to_point]
            graph.add_edge(from_node, to_node, road.capacity, cost=road.repair_cost)
            # Dodajemy tez w druga strone bo drogi sa dwukierunkowe
            graph.add_edge(to_node, from_node, road.capacity, cost=road.repair_cost)

    # 8. Krawędzie Karczmy -> Sink
    for inn in inns:
        inn_node = point_to_node[(inn.x, inn.y)]
        graph.add_edge(inn_node, sink, inn.demand, cost=0)

    return graph
