import json
from models.field import Field
<<<<<<< HEAD
from models.inn import Inn
=======
from models.breweries import Breweries
>>>>>>> 495ebc9a5842c1dbe40c4a864b61cb76eab63cb1

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
<<<<<<< HEAD
            
    def load_inns_from_json(self, json_data):
        inns_data = json.load(open(json_data))['inns']
        for inn in inns_data:
            self.inns.append(Inn(inn['id'], inn['x'] , inn['y'], inn['demand']))
=======

    def load_breweries_from_json(self, json_data):
        breweries_data = json.load(open(json_data))['breweries']
        for breweries in breweries_data:
            self.breweries.append(Breweries(breweries['id'], breweries['x'], breweries['y'], breweries['capacity']))
>>>>>>> 495ebc9a5842c1dbe40c4a864b61cb76eab63cb1
