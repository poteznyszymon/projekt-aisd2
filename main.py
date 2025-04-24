import os
from models.city import City
from models.algo import *

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data/example_3")

def main():
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR_PATH, "fields.json"))
    city.load_inns_from_json(os.path.join(DATA_DIR_PATH, "inns.json"))
    city.load_breweries_from_json(os.path.join(DATA_DIR_PATH, "breweries.json"))
    city.load_roads_from_json(os.path.join(DATA_DIR_PATH, "roads.json"))
    city.load_sectors_from_json(os.path.join(DATA_DIR_PATH, "sectors.json"))

    for field in city.fields:
        print(f"Field ID: {field.id}, X: {field.x}, Y: {field.y}, sector_yield: {field.sector_yield}")
    for brewerie in city.breweries:
        print(f"Brewerie ID: {brewerie.id}, X: {brewerie.x}, Y: {brewerie.y}, Capacity: {brewerie.capacity}")
    for inn in city.inns:
        print(f"Inn ID: {inn.id}, X: {inn.x}, Y: {inn.y}")
    for road in city.roads:
        print(f"Road ID: {road.id}, Start: {road.start}, End: {road.end}, Capacity: {road.capacity}, Repair Cost: {road.repair_cost}")
    #for sector in city.sectors:
    #   print(f"Sector ID: {sector.id}, Polygon: {sector.polygon}, Yield: {sector.sector_yield}")

    graph, source, sink = build_flow_network(city)
    max_flow, min_cost = min_cost_flow(graph, source, sink, city)
    print(f"Maksymalny przepływ: {max_flow}, Minimalny koszt: {min_cost}")

if __name__ == "__main__":
    main()