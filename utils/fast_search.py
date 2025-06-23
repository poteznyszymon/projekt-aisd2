import json
import time
import os
import math
from models.city import City
from utils.algo import GraphEK
from itertools import combinations
import utils.plotter as plotter
from utils.data_generator import Generator
from utils.coding_encoding import huffman_code
from utils.coding_encoding import decode_huffman


def fast_search(city, max_flow):
    start_time = time.time()
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

    roads = sorted(city.roads, key=lambda r: r.repair_cost)
    paid_ids = [r.id for r in roads if r.repair_cost > 0]
    total_supply = sum(f.sector_yield for f in city.fields)
    zero_set = {r.id for r in roads if r.repair_cost == 0}
    cost_map = {r.id: r.repair_cost for r in roads}

    best_flow, best_cost, best_subset = -1, math.inf, set()

    combo = []
    if max_flow == -1:
        for paid_id in paid_ids:
            combo.append(paid_id)

    for rcount in range(len(paid_ids) + 1):
        repaired = zero_set.union(combo)

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

        if flow > best_flow:
            best_flow = flow

        if best_flow == total_supply or rcount == len(paid_ids) or max_flow == flow or max_flow == -1:
            end_time = time.time()
            best_cost = sum(cost_map[rid] for rid in combo)
            repaired = zero_set.union(combo)
            return best_flow, best_cost, repaired, end_time - start_time

        if rcount > 0:
            combo.append(paid_ids[rcount - 1])

    end_time = time.time()
    best_cost = sum(cost_map[rid] for rid in combo)
    repaired = zero_set.union(combo)
    return best_flow, best_cost, repaired, end_time - start_time
