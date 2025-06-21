import os
import math
import pytest
from models.city import City
from utils.algo import GraphEK
from itertools import combinations

def run_flow_solver(DATA_DIR):
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR, 'fields.json'))
    city.load_breweries_from_json(os.path.join(DATA_DIR, 'breweries.json'))
    city.load_inns_from_json(os.path.join(DATA_DIR, 'inns.json'))
    city.load_roads_from_json(os.path.join(DATA_DIR, 'roads.json'))
    city.load_sectors_from_json(os.path.join(DATA_DIR, 'sectors.json'))
    city.assign_sector_yeild_to_fields()

    # Tworzenie listy węzłów (pola, browary, karczmy)
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
    best_flow, best_cost, best_subset = -1, math.inf, set()

    # Szukanie najtańszego zbioru dróg do naprawy (bruteforce)
    for rcount in range(len(paid_ids) + 1):
        for combo in combinations(paid_ids, rcount):
            repaired = zero_set.union(combo)
            cost_combo = sum(cost_map[rid] for rid in combo)
            if best_flow == total_supply and cost_combo >= best_cost:
                continue
            g = GraphEK(N)
            # Dodanie krawędzi za źródla do pól (jęczmień)
            for f in city.fields:
                g.add_edge(source, barley_nodes[(f.x, f.y)], f.sector_yield)
            # Dodanie krawędzi pomiędzy polami
            for r in roads:
                if r.id in repaired:
                    u0, v0 = tuple(r.start), tuple(r.end)
                    if u0 in barley_nodes and v0 in barley_nodes:
                        u, v = barley_nodes[u0], barley_nodes[v0]
                        g.add_edge(u, v, r.capacity)
                        g.add_edge(v, u, r.capacity)
            # Przejście ziarna na piwo w browarach
            for b in city.breweries:
                u = barley_nodes[(b.x, b.y)]
                v = beer_nodes[(b.x, b.y)]
                g.add_edge(u, v, b.capacity)
            # Dodanie krawędzi pomiędzy browarami (piwo)
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
            if flow > best_flow or (flow == best_flow and cost_combo < best_cost):
                best_flow, best_cost, best_subset = flow, cost_combo, repaired
        if best_flow == total_supply:
            break

    return best_flow, best_cost


@pytest.mark.parametrize("example_num, expected_flow, expected_cost", [
    (1, 320, 0),
    (2, 70, 0),
    (3, 70, 0),
    (4, 450, 300),
    ("4_1", 300, 0),
    (5, 200, 0),
    (6, 150, 14),
    ("6_1", 150, 1),
    ("6_2", 200, 23),
    (7, 800, 51),
])
def test_flow_solver(example_num, expected_flow, expected_cost):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, '../data', f'example_{example_num}')

    print(f"Testing example_{example_num} -> data_dir: {data_dir}")

    assert os.path.exists(data_dir), f"Brak katalogu danych: {data_dir}"
    assert os.path.exists(os.path.join(data_dir, 'fields.json')), "Brak pliku fields.json"

    flow, cost = run_flow_solver(data_dir)
    assert flow == expected_flow, f"Flow mismatch in example {example_num}"
    assert cost == expected_cost, f"Cost mismatch in example {example_num}"