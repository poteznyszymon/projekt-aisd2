import os
from models.city import City

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data")

def main():
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR_PATH, "fields.json"))
    city.load_inns_from_json(os.path.join(DATA_DIR_PATH, "inns.json"))
    city.load_breweries_from_json(os.path.join(DATA_DIR_PATH, "breweries.json"))
    city.load_roads_from_json(os.path.join(DATA_DIR_PATH, "roads.json"))
    city.load_sectors_from_json(os.path.join(DATA_DIR_PATH, "sectors.json"))

    for field in city.fields:
        print(f"Field ID: {field.id}, X: {field.x}, Y: {field.y}, sector_yield: {field.sector_yield}")
    for inn in city.inns:
        print(f"Inn ID: {inn.id}, X: {inn.x}, Y: {inn.y}")
    for breweries in city.breweries:
        print(f"Field ID: {breweries.id}, X: {breweries.x}, Y: {breweries.y}, Capacity: {breweries.capacity}")
    for road in city.roads:
        print(f"Road ID: {road.id}, Start: {road.start}, End: {road.end}, Capacity: {road.capacity}, Repair Cost: {road.repair_cost}")
    for sector in city.sectors:
        print(f"Sector ID: {sector.id}, Polygon: {sector.polygon}, Yield: {sector.sector_yield}")

if __name__ == "__main__":
    main()