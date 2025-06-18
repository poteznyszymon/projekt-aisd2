from models.city import City
from models.field import Field
from models.breweries import Breweries
from models.inn import Inn
from models.sector import Sector
from models.road import Road
import random
import numpy as np
from utils.delaunay import bowyer_watson
from utils.delaunay import Triangle


class Generator:
    def __init__(
        self,
        number_of_fields,
        number_of_breweries,
        number_of_inns,
        numbers_of_destroyed_roads
    ):
        self.city = City()

        # tworzenie siatki punktów z odstepem 0.1 w zakresie 0–10
        grid_points = [[round(x, 1), round(y, 1)]
                       for x in np.arange(0, 10.1, 0.1)
                       for y in np.arange(0, 10.1, 0.1)]
        random.shuffle(grid_points)

        def get_next_point():
            return grid_points.pop()


        # generowanie losowych pol
        for _ in range(number_of_fields):
            x, y = get_next_point()
            field = Field(len(self.city.fields), x, y, 10)
            self.city.fields.append(field)

        # generowanie losowych browarow
        for _ in range(number_of_breweries):
            x, y = get_next_point()
            capacity = random.randint(40, 200)
            brewery = Breweries(len(self.city.breweries), x, y, capacity)
            self.city.breweries.append(brewery)

        # Generowanie losowych karczm
        for _ in range(number_of_inns):
            x, y = get_next_point()
            demand = random.randint(40, 200)
            inn = Inn(len(self.city.inns), x, y, demand)
            self.city.inns.append(inn)

        # generowanie losowych sektorow
        x_1 = random.randint(2, 8)
        x_2 = random.randint(2, 8)
        y_1 = random.randint(2, 8)
        data = [
            [[0, 0], [x_1, 0], [x_1, y_1], [0, y_1]],
            [[0, y_1 + 0.1], [x_2, y_1 + 0.1], [x_2, 10], [0, 10]],
            [[x_2 + 0.1, y_1 + 0.1], [x_2 + 0.1, 10], [10, 10], [10, y_1 + 0.1]],
            [[x_1 + 0.1, 0], [x_1 + 0.1, y_1], [10, y_1], [10, 0]]
        ]

        for i in range(4):
            sector = Sector(i, data[i], random.randint(80, 180))
            self.city.sectors.append(sector)

        # punkty do triangulacji
        all_points = []
        all_points.extend([[f.x, f.y] for f in self.city.fields])
        all_points.extend([[b.x, b.y] for b in self.city.breweries])
        all_points.extend([[inn.x, inn.y] for inn in self.city.inns])

        points = np.array(all_points)
        num_points = len(points)

        if num_points < 3:
            # Do triangulacji potrzebne sa co najmniej 3 punkty
            return

        triangles: list[Triangle] = bowyer_watson(all_points)
        edges = set()
        for triangle in triangles:
            verts = triangle.vertices
            for i in range(3):
                a, b = verts[i], verts[(i + 1) % 3]
                edge = tuple(sorted([(a.x, a.y), (b.x, b.y)]))
                edges.add(edge)

        edges = list(edges)

        for idx, (p1, p2) in enumerate(edges):
            repair_cost = random.randint(20, 40) if idx < numbers_of_destroyed_roads else 0
            road = Road(idx, list(p1), list(p2), random.randint(40, 80), repair_cost)
            self.city.roads.append(road)
