import csv
import time
import statistics
import sys
import os
import math
from itertools import combinations

# to musi byc zeby dalo sie korzystac z utils tutaj
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.data_generator import Generator
from utils.algo import GraphEK


def run_test_case(total_objects, damaged_roads, iterations, writer):
    fields_amount = total_objects // 3
    breweries_amount = total_objects // 3
    inns_amount = total_objects - fields_amount - breweries_amount

    flow_list = []
    cost_list = []
    time_list = []

    for i in range(iterations):
        print(f"iteration {i+1}: total_objects={total_objects}, damaged_roads={damaged_roads}")

        start = time.time()
        city = Generator(fields_amount, breweries_amount, inns_amount, damaged_roads).city
        city.assign_sector_yeild_to_fields()

        physical = [(x.x, x.y, x.id, x.__class__.__name__.lower()) for x in (city.fields + city.breweries + city.inns)]
        P = len(physical)
        source = 0
        barley_start = 1
        beer_start = barley_start + P
        sink = beer_start + P
        N = sink + 1

        barley_nodes = {(x, y): barley_start + idx for idx, (x, y, *_rest) in enumerate(physical)}
        beer_nodes = {(x, y): beer_start + idx for idx, (x, y, *_rest) in enumerate(physical)}

        roads = city.roads
        paid_ids = [r.id for r in roads if r.repair_cost > 0]
        zero_set = {r.id for r in roads if r.repair_cost == 0}
        cost_map = {r.id: r.repair_cost for r in roads}

        total_supply = sum(f.sector_yield for f in city.fields)
        best_flow, best_cost = -1, math.inf

        for rcount in range(len(paid_ids) + 1):
            for combo in combinations(paid_ids, rcount):
                repaired = zero_set.union(combo)
                cost_combo = sum(cost_map[rid] for rid in combo)
                if best_flow == total_supply and cost_combo >= best_cost:
                    continue

                g = GraphEK(N)
                for f in city.fields:
                    g.add_edge(source, barley_nodes[(f.x, f.y)], f.sector_yield)
                for r in roads:
                    if r.id in repaired:
                        u0, v0 = tuple(r.start), tuple(r.end)
                        if u0 in barley_nodes and v0 in barley_nodes:
                            g.add_edge(barley_nodes[u0], barley_nodes[v0], r.capacity)
                            g.add_edge(barley_nodes[v0], barley_nodes[u0], r.capacity)
                for b in city.breweries:
                    g.add_edge(barley_nodes[(b.x, b.y)], beer_nodes[(b.x, b.y)], b.capacity)
                for r in roads:
                    if r.id in repaired:
                        u0, v0 = tuple(r.start), tuple(r.end)
                        if u0 in beer_nodes and v0 in beer_nodes:
                            g.add_edge(beer_nodes[u0], beer_nodes[v0], r.capacity)
                            g.add_edge(beer_nodes[v0], beer_nodes[u0], r.capacity)
                for inn in city.inns:
                    g.add_edge(beer_nodes[(inn.x, inn.y)], sink, inn.demand)

                flow = g.max_flow(source, sink)
                if flow > best_flow or (flow == best_flow and cost_combo < best_cost):
                    best_flow, best_cost = flow, cost_combo
            if best_flow == total_supply:
                break

        end = time.time()
        flow_list.append(best_flow)
        cost_list.append(best_cost)
        time_list.append(end - start)

    avg_flow = round(statistics.mean(flow_list), 2)
    avg_cost = round(statistics.mean(cost_list), 2)
    avg_time = round(statistics.mean(time_list), 4)

    writer.writerow([
        total_objects, fields_amount, breweries_amount, inns_amount, damaged_roads,
        avg_flow, avg_cost, avg_time
    ])


def test_no_damaged_roads(iterations=10):
    output_file = "./performance_tests_no_damaged.csv"
    total_objects_amount = [10, 20, 40, 80, 120, 200, 300, 500, 1000, 1500]

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "TotalObjects", "Fields", "Breweries", "Inns", "DamagedRoads",
            "AvgBestFlow", "AvgBestCost", "AvgTime"
        ])

        for total_objects in total_objects_amount:
            run_test_case(total_objects, damaged_roads=0, iterations=iterations, writer=writer)
            

def test_with_damaged_roads(iterations=10):
    output_file = "./performance_tests_damaged.csv"
    total_objects_amount = [40]
    damaged_values = [2, 4, 6, 8, 10, 12, 15, 20]

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "TotalObjects", "Fields", "Breweries", "Inns", "DamagedRoads",
            "AvgBestFlow", "AvgBestCost", "AvgTime"
        ])

        for damaged_roads in damaged_values:
            for total_objects in total_objects_amount:
                run_test_case(total_objects, damaged_roads, iterations, writer)


if __name__ == "__main__":
    #test_no_damaged_roads()
    test_with_damaged_roads()
