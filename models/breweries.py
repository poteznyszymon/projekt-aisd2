class Breweries():
    def __init__(self, id, x, y, capacity):
        self.id = id
        self.x = x
        self.y = y
        self.capacity = capacity

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "capacity": self.capacity
        }
