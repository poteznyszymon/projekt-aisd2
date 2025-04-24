from utils.geometry import Point

class Sector():
    def __init__(self, id, polygon, sector_yield):
        self.id = id
        self.polygon = polygon
        self.sector_yield = sector_yield
        
    def to_point_list(self) -> list[Point]:
        return [Point(x,y) for x,y in self.polygon]