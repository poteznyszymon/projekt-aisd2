import json
from models.field import Field
from models.inn import Inn

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
            
    def load_inns_from_json(self, json_data):
        inns_data = json.load(open(json_data))['inns']
        for inn in inns_data:
            self.inns.append(Inn(inn['id'], inn['x'] , inn['y'], inn['demand']))