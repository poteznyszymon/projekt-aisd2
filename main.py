import json
import os

DATA_DIR_PATH = os.path.join(os.path.dirname(__file__), "data")

def main():
    with open(os.path.join(DATA_DIR_PATH, "fields.json"), "r") as f:
        fields = json.load(f)
    print(fields['fields'][0])

if __name__ == "__main__":
    main()