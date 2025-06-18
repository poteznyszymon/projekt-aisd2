import json
import os
from models.city import City
import utils.algo as algo
import utils.plotter as plotter
from utils.data_generator import Generator
from utils.coding_encoding import huffman_code
from utils.coding_encoding import decode_huffman
import time

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data/example_6_2")

def main():
    start = time.time()
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR_PATH, "fields.json"))
    city.load_inns_from_json(os.path.join(DATA_DIR_PATH, "inns.json"))
    city.load_breweries_from_json(os.path.join(DATA_DIR_PATH, "breweries.json"))
    city.load_roads_from_json(os.path.join(DATA_DIR_PATH, "roads.json"))
    city.load_sectors_from_json(os.path.join(DATA_DIR_PATH, "sectors.json"))
    city.assign_sector_yeild_to_fields()

    # maks 3400 do kazdego po rowno tyle sie miesci na mapie 10 na 10 jezeli sa odddalone o 0.1
    random_city = Generator(5,3,3,5).city
    random_city.assign_sector_yeild_to_fields()

    #Buduję graf pola -> browary
    graph_1, sink = algo.build_flow_graph(random_city.fields, random_city.breweries, random_city.inns, random_city.roads)

    # Buduję graf browary -> karczmy
    graph_2, sink = algo.build_flow_graph(random_city.breweries, random_city.inns, random_city.fields, random_city.roads)

    #liczę max_flow z pola -> browary
    max_flow = graph_1.edmonds_karp(0, sink, 1)
    print(f"Maksymalny przepływ z pól do browarów: {max_flow}, sink: {sink}")

    for edge in graph_2.graph[0]:
        for edge_1 in graph_1.graph[graph_1.breweries_dict_rev[graph_2.breweries_dict[edge.to]]]:
            if edge_1.to == sink:
                edge.capacity = edge_1.flow
                edge.rev.capacity = edge_1.flow

    # liczę max_flow z browary -> karczmy
    max_flow = graph_2.edmonds_karp(0, sink, 1)
    print(f"Maksymalny przepływ z browarów do karczm: {max_flow}, sink: {sink}")

    # liczę max_flow całego miasta
    print(f"Maksymalny przepływ: {max_flow}, sink: {sink}")

    # Tworze graf dla pola -> browary, browary -> karczmy
    graph_1, sink = algo.build_flow_graph(random_city.fields, random_city.breweries, random_city.inns, random_city.roads)

    graph_2, sink = algo.build_flow_graph(random_city.breweries, random_city.inns, random_city.fields, random_city.roads)

    # Wywołuje funkcje szukającą
    min_cost = [float('inf')]
    repair_list = []
    min_cost, graph_1_1, graph_2_1 = algo.test(graph_1, graph_2, 0, sink,  max_flow, min_cost, repair_list, -1)
    print(f"Maksymalny przepływ: {max_flow}, minimalny koszt: {min_cost}, sink: {sink}")

    encoded, codes = huffman_code(random_city, max_flow, min_cost)
    decoded_text = decode_huffman(encoded, codes)

    decoded_data = json.loads(decoded_text)

    print(decoded_data)

    end = time.time()
    print(f"Czas wykonania: {end - start:.4f} sekund")

    plotter.plot_city(random_city, show_capacity=False, max_flow=max_flow, min_cost=min_cost)



if __name__ == "__main__":
    main()

