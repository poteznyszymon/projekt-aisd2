from models.city import City
from models.field import Field
from models.breweries import Breweries
from models.inn import Inn
from models.sector import Sector
from models.road import Road
import random
import numpy as np
from scipy.spatial import Delaunay


class Generator:
    def __init__(
        self,
        number_of_fields,
        number_of_breweries,
        number_of_inns,
        percentage_of_broken_roads
    ):
        self.city = City()

        # tworzenie siatki punktów z odstepem 0.1 w zakresie 0–10
        grid_points = [[round(x, 1), round(y, 1)]
                       for x in np.arange(0, 10.1, 0.1)
                       for y in np.arange(0, 10.1, 0.1)]
        random.shuffle(grid_points)

        def get_next_point():
            print(grid_points[-1])
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

        # przygotowanie punktow do triangulacji
        all_points = []
        all_points.extend([[f.x, f.y] for f in self.city.fields])
        all_points.extend([[b.x, b.y] for b in self.city.breweries])
        all_points.extend([[inn.x, inn.y] for inn in self.city.inns])

        points = np.array(all_points)
        num_points = len(points)

        if num_points < 3:
            # Do triangulacji potrzebne sa co najmniej 3 punkty
            return

        # tworzenie triangulacji delaunaya
        tri = Delaunay(points)
        edges = set()
        for simplex in tri.simplices:
            edges.add(tuple(sorted((simplex[0], simplex[1]))))
            edges.add(tuple(sorted((simplex[1], simplex[2]))))
            edges.add(tuple(sorted((simplex[2], simplex[0]))))

        edges = list(edges)
        num_broken_roads = int(len(edges) * (percentage_of_broken_roads / 100))
        broken_indices = set(random.sample(range(len(edges)), num_broken_roads))

        # tworzenie drog
        for idx, (i, j) in enumerate(edges):
            p1 = points[i]
            p2 = points[j]
            repair_cost = random.randint(10, 40) if idx in broken_indices else 0
            road = Road(idx, p1.tolist(), p2.tolist(), random.randint(40, 80), repair_cost)
            self.city.roads.append(road)
