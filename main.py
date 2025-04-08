import json
import os

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data")

def main():
    with open(os.path.join(DATA_DIR_PATH, "fields.json"), "r") as f:
        fields_list = json.load(f)['fields']
    print(fields_list)

if __name__ == "__main__":
    main()