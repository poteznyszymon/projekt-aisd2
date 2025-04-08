import json
from models.field import Field
from models.breweries import Breweries

class City():
    def __init__(self):
        self.fields = []
        self.breweries = []
        self.inns = []
        self.roads = []
        self.sectors = []
        
    def load_fields_from_json(self, json_data):
        fields_data = json.load(open(json_data))['fields']
        for field in fields_data:
            self.fields.append(Field(field['id'], field['x'], field['y']))

    def load_breweries_from_json(self, json_data):
        breweries_data = json.load(open(json_data))['breweries']
        for breweries in breweries_data:
            self.breweries.append(Breweries(breweries['id'], breweries['x'], breweries['y'], breweries['capacity']))