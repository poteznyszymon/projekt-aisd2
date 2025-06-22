import json
import time
import os
from models.city import City
from utils.algo import bruteforce
import utils.plotter as plotter
from utils.data_generator import Generator
from utils.coding_encoding import huffman_code
from utils.coding_encoding import decode_huffman

def main():
    start = time.time()
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data/example_7")
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR, 'fields.json'))
    city.load_breweries_from_json(os.path.join(DATA_DIR, 'breweries.json'))
    city.load_inns_from_json(os.path.join(DATA_DIR, 'inns.json'))
    city.load_roads_from_json(os.path.join(DATA_DIR, 'roads.json'))
    city.load_sectors_from_json(os.path.join(DATA_DIR, 'sectors.json'))
    city.assign_sector_yeild_to_fields()

    '''
    city = Generator(8,5,6,5).city
    city.assign_sector_yeild_to_fields()
    '''

    max_flow, min_cost, used_roads = bruteforce(city)

    print(f"Maksymalny przepływ: {max_flow}, minimalny koszt: {min_cost}")

    encoded, codes = huffman_code(city, max_flow, min_cost)
    decoded_text = decode_huffman(encoded, codes)

    decoded_data = json.loads(decoded_text)

    print(decoded_data)

    end = time.time()
    print(f"Czas wykonania: {end - start:.4f} sekund")

    plotter.plot_city(city, show_capacity=True, max_flow=max_flow, min_cost=min_cost, repaired = used_roads)


if __name__ == "__main__":
    main()