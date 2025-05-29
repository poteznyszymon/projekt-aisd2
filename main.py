import os
from models.city import City
import utils.algo as algo
import utils.plotter as plotter
from utils.data_generator import Generator

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data/example_6_2")

def main():
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR_PATH, "fields.json"))
    city.load_inns_from_json(os.path.join(DATA_DIR_PATH, "inns.json"))
    city.load_breweries_from_json(os.path.join(DATA_DIR_PATH, "breweries.json"))
    city.load_roads_from_json(os.path.join(DATA_DIR_PATH, "roads.json"))
    city.load_sectors_from_json(os.path.join(DATA_DIR_PATH, "sectors.json"))
    city.assign_sector_yeild_to_fields()

    for field in city.fields:
        print(f"Field ID: {field.id}, X: {field.x}, Y: {field.y}, sector_yield: {field.sector_yield}")
    for brewerie in city.breweries:
        print(f"Brewerie ID: {brewerie.id}, X: {brewerie.x}, Y: {brewerie.y}, Capacity: {brewerie.capacity}")
    for inn in city.inns:
        print(f"Inn ID: {inn.id}, X: {inn.x}, Y: {inn.y}")
    for road in city.roads:
        print(f"Road ID: {road.id}, Start: {road.start}, End: {road.end}, Capacity: {road.capacity}, Repair Cost: {road.repair_cost}")
    for sector in city.sectors:
        print(f"Sector ID: {sector.id}, Polygon: {sector.polygon}, Yield: {sector.sector_yield}")
    

    #Buduję graf pola -> browary
    graph_1, sink = algo.build_flow_graph(city.fields, city.breweries, city.inns, city.roads)

    # Buduję graf browary -> karczmy
    graph_2, sink = algo.build_flow_graph(city.breweries, city.inns, city.fields, city.roads)

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
    graph_1, sink = algo.build_flow_graph(city.fields, city.breweries, city.inns, city.roads)

    graph_2, sink = algo.build_flow_graph(city.breweries, city.inns, city.fields, city.roads)


    # Wywołuje funkcje szukającą
    min_cost = [float('inf')]
    repair_list = []
    min_cost, graph_1_1, graph_2_1 = algo.test(graph_1, graph_2, 0, sink,  max_flow, min_cost, repair_list, -1)
    graph_1_1.print_graph()
    graph_2_1.print_graph()
    print(f"Maksymalny przepływ: {max_flow}, minimalny koszt: {min_cost}, sink: {sink}")


    plotter.plot_city(city, show_capacity=True)

if __name__ == "__main__":
    main()

