import numpy as np
from utils.geometry import Point


class Triangle:
    def __init__(self, a: Point, b: Point, c: Point):
        self.vertices = [a, b, c]

    def circumcircle_contains(self, point: Point) -> bool:
        ax, ay = self.vertices[0].x, self.vertices[0].y
        bx, by = self.vertices[1].x, self.vertices[1].y
        cx, cy = self.vertices[2].x, self.vertices[2].y
        dx, dy = point.x, point.y

        mat = np.array([
            [ax - dx, ay - dy, (ax - dx) ** 2 + (ay - dy) ** 2],
            [bx - dx, by - dy, (bx - dx) ** 2 + (by - dy) ** 2],
            [cx - dx, cy - dy, (cx - dx) ** 2 + (cy - dy) ** 2]
        ])

        return np.linalg.det(mat) > 0


def bowyer_watson(points: list[list[float]]):
    input_points = [Point(x, y) for x, y in points]

    # Super trojkat ktory musi byc bardz duzy aby wszyskie punkty napewno byly w srodku
    super_triangle = Triangle(
        Point(-1e5, -1e5),
        Point(1e5, -1e5),
        Point(0, 1e5)
    )

    triangulation = [super_triangle]

    for point in input_points:
        bad_triangles = []
        for triangle in triangulation:
            if triangle.circumcircle_contains(point):
                bad_triangles.append(triangle)

        # Szukanie krawedzi wewnetrznych
        boundary = []
        for triangle in bad_triangles:
            for i in range(3):
                edge = (triangle.vertices[i], triangle.vertices[(i + 1) % 3])
                reversed_edge = (edge[1], edge[0])
                if reversed_edge in boundary:
                    boundary.remove(reversed_edge)
                else:
                    boundary.append(edge)

        for triangle in bad_triangles:
            triangulation.remove(triangle)

        for edge in boundary:
            new_triangle = Triangle(edge[0], edge[1], point)
            triangulation.append(new_triangle)

    # Usuwanie trojkatow zawierajace krawedzie laczace sie z super trojkatem
    final_triangulation: list[Triangle] = []
    for triangle in triangulation:
        if any(v in super_triangle.vertices for v in triangle.vertices):
            continue
        final_triangulation.append(triangle)

    # Zwarcamy liste trojkatow ktore sa drogami w miescie
    return final_triangulation
