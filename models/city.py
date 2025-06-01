import json
from models.field import Field
from models.inn import Inn
from models.breweries import Breweries
from models.road import Road
from models.sector import Sector
from utils.geometry import is_point_inside_polygon

class City():
    def __init__(self):
        self.fields: list[Field] = []
        self.breweries: list[Breweries] = []
        self.inns: list[Inn] = []
        self.roads: list[Road] = []
        self.sectors: list[Sector] = []
        
    def load_fields_from_json(self, json_data):
        fields_data = json.load(open(json_data))['fields']
        for field in fields_data:
            self.fields.append(Field(field['id'], field['x'], field['y'], field['sector_yield']))
            
    def load_inns_from_json(self, json_data):
        inns_data = json.load(open(json_data))['inns']
        for inn in inns_data:
            self.inns.append(Inn(inn['id'], inn['x'] , inn['y'], inn['demand']))

    def load_breweries_from_json(self, json_data):
        breweries_data = json.load(open(json_data))['breweries']
        for brewerie in breweries_data:
            self.breweries.append(Breweries(brewerie['id'], brewerie['x'], brewerie['y'], brewerie['capacity']))
            
    def load_roads_from_json(self, json_data):
        roads_data = json.load(open(json_data))['roads']
        for road in roads_data:
            self.roads.append(Road(road['id'], road['from'], road['to'], road['capacity'], road['repair_cost']))
            
    def load_sectors_from_json(self, json_data):
        sectors_data = json.load(open(json_data))['shire_sectors']
        for sector in sectors_data:
            self.sectors.append(Sector(sector['id'], sector['polygon'], sector['yield']))
    
    def assign_sector_yeild_to_fields(self):
        for field in self.fields:
            for sector in self.sectors:
                if is_point_inside_polygon(field.to_point(), sector.to_point_list()):
                    field.sector_yield += sector.sector_yield
                    break