from models.city import City
from models.field import Field
from models.breweries import Breweries
from models.inn import Inn
from models.sector import Sector
from models.road import Road
import random
import numpy as np
from scipy.spatial import Delaunay  # Zmieniono import na Delaunay


class Generator:
    city: City = City()
    used_points = []

    def _get_unique_point(self):
        while True:
            point = [round(random.uniform(0, 10), 1), round(random.uniform(0, 10), 1)]
            if point not in self.used_points:
                self.used_points.append(point)
                return point

    def __init__(
            self,
            number_of_fields,
            number_of_breweries,
            number_of_inns,
            percentage_of_broken_roads
    ):
        # Generowanie losowych pól uprawnych
        for i in range(number_of_fields):
            x, y = self._get_unique_point()
            random_field: Field = Field(len(self.used_points), x, y, 10)
            self.city.fields.append(random_field)

        # Generowanie losowych browarów
        for i in range(number_of_breweries):
            x, y = self._get_unique_point()
            random_capacity = random.randint(40, 200)
            random_breweries: Breweries = Breweries(len(self.used_points), x, y, random_capacity)
            self.city.breweries.append(random_breweries)

        # Generowanie losowych karczm
        for i in range(number_of_inns):
            x, y = self._get_unique_point()
            random_demand = random.randint(40, 200)
            random_inn: Inn = Inn(len(self.used_points), x, y, random_demand)
            self.city.inns.append(random_inn)

        # Generowanie losowych sektorow
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

        points = np.array(self.used_points)
        num_points = len(points)

        if num_points < 3:
            # do algorytmu trangualcji wymagane sa co najmniej 3 punkty
            return
        else:
            # Krok 1: Wykonaj Triangulację Delaunaya
            # points muszą być numpy array
            tri = Delaunay(points)

            # Krok 2: Wyodrębnij unikalne krawędzie z trójkątów Delaunaya
            # Kazdy simplex to krotka indeksow punktow
            # np. (0, 1, 2) oznacza trójkąt z punktów o indeksach 0, 1, 2
            # Z tego trójkąta powstają 3 krawędzie: (0,1), (1,2), (2,0)

            edges = set()
            for simplex in tri.simplices:
                # Krawędzie trójkąta (simplex): (p0,p1), (p1,p2), (p2,p0)
                # Sortujemy krotkę (min(i,j), max(i,j)) aby mieć unikalną reprezentację krawędzi
                edges.add(tuple(sorted((simplex[0], simplex[1]))))
                edges.add(tuple(sorted((simplex[1], simplex[2]))))
                edges.add(tuple(sorted((simplex[2], simplex[0]))))

            id = 0
            edges = list(edges)
            num_broken_roads = int(len(edges) * (percentage_of_broken_roads / 100))
            broken_indices = set(random.sample(range(len(edges)), num_broken_roads))

            for idx, (i, j) in enumerate(edges):
                p1 = points[i]
                p2 = points[j]

                repair_cost = random.randint(10, 40) if idx in broken_indices else 0

                road = Road(id, p1.tolist(), p2.tolist(), random.randint(40, 80), repair_cost)
                self.city.roads.append(road)
                id += 1
