class Road():
    def __init__(self, id, start, end, capacity, repair_cost):
        self.id = id
        self.start = start
        self.end = end
        self.capacity = capacity
        self.repair_cost = repair_cost

    def to_dict(self):
        return {
            "id": self.id,
            "start": self.start,
            "end": self.end,
            "capacity": self.capacity,
            "repair_cost": self.repair_cost
        }