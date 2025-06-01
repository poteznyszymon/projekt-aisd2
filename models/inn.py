class Inn():
    def __init__(self, id, x, y, demand):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand

    def to_dict(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "demand": self.demand
        }