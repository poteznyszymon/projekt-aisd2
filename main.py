import json
import os
from models.city import City

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data")

def main():
    #with open(os.path.join(DATA_DIR_PATH, "fields.json"), "r") as f:
    #    fields_list = json.load(f)['fields']
    #print(fields_list)
    
    city = City()
    city.load_fields_from_json(os.path.join(DATA_DIR_PATH, "fields.json"))
    city.load_inns_from_json(os.path.join(DATA_DIR_PATH, "inns.json"))
    
    for field in city.fields:
        print(f"Field ID: {field.id}, X: {field.x}, Y: {field.y}")
    for inn in city.inns:
        print(f"Inn ID: {inn.id}, X: {inn.x}, Y: {inn.y}")

if __name__ == "__main__":
    main()