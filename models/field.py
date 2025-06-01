from utils.geometry import Point

class Field():
    def __init__(self, id, x, y, sector_yield):
        self.id = id
        self.x = x
        self.y = y
        # 20 bazowo plus premia zalezna od tego w jakiej cwiartce jest
        self.sector_yield = 20
    
    def to_point(self):
        return Point(self.x, self.y)

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "sector_yield": self.sector_yield
        }