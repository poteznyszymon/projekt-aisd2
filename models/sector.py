from utils.geometry import Point
from utils.jarvis import convert_to_jarvis_points

class Sector():
    def __init__(self, id, polygon, sector_yield):
        self.id = id
        self.polygon = convert_to_jarvis_points(polygon)
        #self.polygon = polygon
        self.sector_yield = sector_yield
        
    def to_point_list(self) -> list[Point]:
        return [Point(x, y) for x, y in self.polygon]

    def to_dict(self):
        return {
            "id": self.id,
            "polygon": self.polygon,
            "sector_yield": self.sector_yield
        }