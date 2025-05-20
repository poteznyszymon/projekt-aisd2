from collections import deque
import copy

class Edge:
    def __init__(self, to: int, capacity: int, cost: int):
        self.to = to              # numer wierzcholka docelowego
        self.capacity = capacity  # przepustowosc
        self.flow = 0             # przepływ
        self.cost = cost          # koszt naprawy drogi
        self.rev = None           # wskaznik na krawedz odwrotna (do pozniejszego obliczania przeplywu)

class Graph:
    def __init__(self):
        self.graph = {}  # slownik: wierzcholek -> lista krawedzi
        self.edges = []
        self.paid_edges = []  # tu zapisujemy tylko płatne krawędzie
        self.breweries_dict = {}
        self.breweries_dict_rev = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
    
    def add_edge(self, start, end, capacity, cost=0):
        forward = Edge(end, capacity, cost)
        backward = Edge(start, capacity, cost)  # krawedz odwrotna: 0 capacity i przeciwny koszt
        forward.rev = backward
        backward.rev = forward
        self.graph[start].append(forward)
        self.graph[end].append(backward)

        self.edges.append(forward)
        if cost > 0:
            self.paid_edges.append(forward)

    def edmonds_karp(self, source, sink, tryb):
        max_flow = 0
        while True:
            # BFS do znalezienia najkrótszej ścieżki rozszerzającej
            parent = {}
            queue = deque([source])
            parent[source] = None
            found = False

            while queue and not found:
                u = queue.popleft()
                for edge in self.graph.get(u, []):
                    if tryb == 1:
                        if edge.capacity > 0 and edge.cost>=0 and edge.to not in parent:
                            parent[edge.to] = (u, edge)  # Zapisz węzeł rodzica i krawędź
                            queue.append(edge.to)

                            if edge.to == sink:
                                found = True
                                break
                    else:
                        if edge.capacity > 0 and edge.cost == 0 and edge.to not in parent:
                            parent[edge.to] = (u, edge)  # Zapisz węzeł rodzica i krawędź
                            queue.append(edge.to)

                            if edge.to == sink:
                                found = True
                                break
                #print(deque(parent))
            #print(deque(parent))
            if not found:
                break

            # Oblicz maksymalny przepływ na znalezionej ścieżce
            path_flow = float('inf')
            v = sink
            while v != source:
                u, edge = parent[v]
                path_flow = min(path_flow, edge.capacity)
                v = u
                #print(f"{u} -> {edge.to} => cost: {edge.cost}, capacity: {edge.capacity}, max flow: {path_flow}")

            # Aktualizuj przepływy
            v = sink
            while v != source:
                u, edge = parent[v]
                edge.capacity -= path_flow
                edge.rev.capacity += path_flow
                edge.flow += path_flow
                edge.rev.flow -= path_flow
                v = u

            max_flow += path_flow
        return max_flow
        
    def add_bidirectional_edge(self, node1, node2, capacity, cost=0):
        self.add_edge(node1, node2, capacity, cost)
        self.add_edge(node2, node1, capacity, cost)
        
    def print_graph(self):
        for node, edges in self.graph.items():
            print(f"Wierzcholek {node}:")
            visited_edges = set()  # Set do sledzenia odwiedzonych krawedzi
            
            for edge in edges:
                # Sprawdzamy czy krawedz odwrotna zostala juz wydrukowana
                #if (edge.to, edge.rev.to) not in visited_edges and (edge.rev.to, edge.to) not in visited_edges:
                print(f"  -> {edge.to} | capacity: {edge.capacity} | flow: {edge.flow} | cost: {edge.cost}")
                  #  visited_edges.add((node, edge.to))  # Dodajemy krawedz
                    #visited_edges.add((edge.to, node))  # Dodajemy krawedz odwrotna
            print()

def test(graph_1, graph_2, source, sink, max_flow, current_flow, min_cost, repair_list, napraw):
    if napraw == -1:
        print(f"TEST 0")
        graph_1_copy = copy.deepcopy(graph_1)
        graph_2_copy = copy.deepcopy(graph_2)
        current_cost = 0
        max_flow_1 = graph_1_copy.edmonds_karp(source, sink, 2)
        """print("Z Browarów do sink")
        for edge in graph_1_copy.graph[sink]:
            # Sprawdź krawędzie odwrotne, czyli takie, które prowadzą *do* sinka
            if edge.rev:
                print(f"[Node_id: {edge.to}, ID_czegos: {graph_1_copy.breweries_dict[edge.to]}, {edge.rev.flow} / {edge.rev.capacity}]")"""

        # print("Z source do Browarów 1")
        for edge in graph_2_copy.graph[source]:
            # Sprawdź krawędzie odwrotne, czyli takie, które prowadzą *do* sinka

            if edge.rev:
                # print(f"[Node_id: {edge.to}, ID_czegos: {graph_2_copy.breweries_dict[edge.to]}, {edge.flow} / {edge.capacity}]")
                # print(f"   {graph_1_copy.breweries_dict_rev[graph_2_copy.breweries_dict[edge.to]]}")
                for edge_1 in graph_1_copy.graph[graph_1_copy.breweries_dict_rev[graph_2_copy.breweries_dict[edge.to]]]:
                    if edge_1.to == sink:
                        # print(f"      edge {edge_1.to}, flow: {edge_1.flow} / {edge_1.rev.capacity}, EDGE: {edge.capacity}")
                        edge.capacity = -edge_1.rev.flow
                        edge.rev.capacity = -edge_1.rev.flow

        max_flow_2 = graph_2_copy.edmonds_karp(source, sink, 2)
        current_flow = min(max_flow_1, max_flow_2)
        print(f"Koszt: {current_cost}, przepływ: {current_flow}, naprawiono: {0} / {len(graph_1_copy.paid_edges)}, {max_flow_1}, {max_flow_2}")

        if current_flow >= max_flow:
            min_cost[0] = current_cost
            print(f"Nowy minimalny koszt znaleziony: {min_cost[0]}, dla napraw: 0")
            return min_cost[0], graph_1_copy, graph_2_copy
        print("GRAF_1")
        graph_1_copy.print_graph()
        print("GRAF_2")
        graph_2_copy.print_graph()

    print("NOWA REKURENCJA")
    graph_1_copy = copy.deepcopy(graph_1)
    graph_2_copy = copy.deepcopy(graph_2)

    # W kolejnych rekurencjach kopiujemy listę napraw i modyfikujemy grafy
    local_repair_list = repair_list.copy()

    if napraw >= 0:
        local_repair_list.append(napraw)

    current_cost = 0
    for i in local_repair_list:
        print(f"Repairing {i} za {graph_1_copy.paid_edges[i].cost}")
        current_cost += graph_1_copy.paid_edges[i].cost
        graph_1_copy.paid_edges[i].cost = 0
        graph_1_copy.paid_edges[i].rev.cost = 0
        graph_2_copy.paid_edges[i].cost = 0
        graph_2_copy.paid_edges[i].rev.cost = 0
    print(f"Current cost: {current_cost}")

    max_flow_1 = graph_1_copy.edmonds_karp(source, sink, 2)
    """print("Z Browarów do sink")
    for edge in graph_1_copy.graph[sink]:
        # Sprawdź krawędzie odwrotne, czyli takie, które prowadzą *do* sinka
        if edge.rev:
            print(f"[Node_id: {edge.to}, ID_czegos: {graph_1_copy.breweries_dict[edge.to]}, {edge.rev.flow} / {edge.rev.capacity}]")"""

    #print("Z source do Browarów 1")
    for edge in graph_2_copy.graph[source]:
        # Sprawdź krawędzie odwrotne, czyli takie, które prowadzą *do* sinka
        
        if edge.rev:
            #print(f"[Node_id: {edge.to}, ID_czegos: {graph_2_copy.breweries_dict[edge.to]}, {edge.flow} / {edge.capacity}]")
            #print(f"   {graph_1_copy.breweries_dict_rev[graph_2_copy.breweries_dict[edge.to]]}")
            for edge_1 in graph_1_copy.graph[graph_1_copy.breweries_dict_rev[graph_2_copy.breweries_dict[edge.to]]]:
                if edge_1.to == sink:
                    #print(f"      edge {edge_1.to}, flow: {edge_1.flow} / {edge_1.rev.capacity}, EDGE: {edge.capacity}")
                    edge.capacity = -edge_1.rev.flow
                    edge.rev.capacity = -edge_1.rev.flow

    max_flow_2 = graph_2_copy.edmonds_karp(source, sink, 2)
    """print("Z source do Browarów 2")
    for edge in graph_2_copy.graph[source]:
        # Sprawdź krawędzie odwrotne, czyli takie, które prowadzą *do* sinka
        if edge.rev:
            print(f"[Node_id: {edge.to}, ID_czegos: {graph_2_copy.breweries_dict[edge.to]}, {edge.flow} / {edge.capacity}]")

    print("Z karczm do sink")
    for edge in graph_2_copy.graph[sink]:
        if edge.rev:
            print(f"[Node_id: {edge.to}, {edge.rev.flow} / {edge.rev.capacity}]")"""

    current_flow = min(max_flow_1, max_flow_2)
    #print()
    #print()
    #print("GRAF_1")
    #graph_1_copy.print_graph()
    #print("GRAF_2")
    #graph_2_copy.print_graph()

    print(f"Koszt: {current_cost}, przepływ: {current_flow}, naprawiono: {len(local_repair_list)} / {len(graph_1_copy.paid_edges)}, {max_flow_1}, {max_flow_2}")
    for i in local_repair_list:
        print(f"[{i}]")

    #print(f"Browarów: {len(graph_1.breweries_dict)}")
    #print(graph_1_copy.breweries_dict)

    # Sprawdzenie czy osiągnięto wymagany przepływ
    if current_flow >= max_flow:
        if current_cost < min_cost[0]:
            min_cost[0] = current_cost
            print(f"Nowy minimalny koszt znaleziony: {min_cost[0]}, dla napraw: {local_repair_list}")
        return min_cost[0], graph_1_copy, graph_2_copy

    # Próba naprawienia kolejnych krawędzi
    if len(local_repair_list) < len(graph_1_copy.paid_edges):
        start = max(local_repair_list, default=-1) + 1
        for i in range(start, len(graph_1_copy.paid_edges)):
            if graph_1_copy.paid_edges[i].cost > 0:
                test(
                    graph_1,
                    graph_2,
                    source,
                    sink,
                    max_flow,
                    current_flow,
                    min_cost,
                    local_repair_list,
                    i
                )

    return min_cost[0], graph_1_copy, graph_2_copy


def build_flow_graph(sources, targets, others, roads):
    graph = Graph()

    node_id = 0
    point_to_node = {}

    # 1. Dodajemy source (sztuczny poczatkowy wierzcholek dla sieci przeplywowej)
    graph.add_node(node_id)
    node_id += 1

    # 2. Pola / Browary
    for source in sources:
        if hasattr(source, 'capacity'):
            graph.breweries_dict[node_id] = source.id
            graph.breweries_dict_rev[source.id] = node_id
        point = (source.x, source.y)
        point_to_node[point] = node_id
        graph.add_node(node_id)
        node_id += 1

    # 3. Browary / Karczmy
    for target in targets:
        if hasattr(target, 'capacity'):
            graph.breweries_dict[node_id] = target.id
            graph.breweries_dict_rev[target.id] = node_id
        point = (target.x, target.y)
        point_to_node[point] = node_id
        graph.add_node(node_id)
        node_id += 1

    # 4. Karczmy / Pola
    for other in others:
        point = (other.x, other.y)
        point_to_node[point] = node_id
        graph.add_node(node_id)
        node_id += 1

    # 5. Dodajemy sink (sztuczny ostatni wierzcholek dla sieci przeplywowej)
    sink = node_id
    graph.add_node(sink)

    # 6. Krawedzie Source -> Pola / Browary
    for source in sources:
        if hasattr(source, 'sector_yield'):
            capacity = source.sector_yield
        else:
            capacity = source.capacity
        source_node = point_to_node[(source.x, source.y)]
        graph.add_edge(0, source_node, capacity, cost=0)

    # 7. Krawędzie na podstawie dróg (między polami, browarami, karczmami)
    repair_list = []
    for road in roads:
        from_point = tuple(road.start)
        to_point = tuple(road.end)

        if from_point in point_to_node and to_point in point_to_node:
            from_node = point_to_node[from_point]
            to_node = point_to_node[to_point]

            graph.add_edge(from_node, to_node, road.capacity, cost=road.repair_cost)
            # Dodajemy tez w druga strone bo drogi sa dwukierunkowe
            #graph.add_edge(to_node, from_node, road.capacity, cost=road.repair_cost)

    # 8. Krawedzie Browary -> Sink
    for target in targets:
        target_node = point_to_node[(target.x, target.y)]
        graph.add_edge(target_node, sink, float('inf'), cost=0)


    return graph, sink