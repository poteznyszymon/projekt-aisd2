from utils.geometry import Point

class Field():
    def __init__(self, id, x, y, sector_yield):
        self.id = id
        self.x = x
        self.y = y
        self.sector_yield = None
    
    def to_point(self):
        return Point(self.x, self.y)