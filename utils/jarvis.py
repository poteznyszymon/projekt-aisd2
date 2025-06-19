from utils.geometry import Point
from utils.geometry import orientation
from math import sqrt


def distance(p1: Point, p2: Point) -> float:
    return sqrt(((p1.x - p2.x)*(p1.x - p2.x)) + ((p1.y - p2.y)*(p1.y - p2.y)))


def convert_to_jarvis_points(points) -> list[list[float]]:
    jarvis_points: list[Point] = []
    input_points: list[Point] = []

    for point in points:
        input_points.append(Point(point[0], point[1]))

    bottom_point: Point = min(input_points, key=lambda p: (p.y, p.x))
    #upper_point: Point = max(input_points, key=lambda p: (p.y, p.x))

    current_point = bottom_point
    while True:
        next_point = input_points[0]
        for candidate in input_points:
            if candidate == current_point:
                continue
            det = orientation(current_point, next_point, candidate)
            if det > 0:
                next_point = candidate

            elif det == 0:
                if distance(current_point, candidate) > distance(current_point, next_point):
                    next_point = candidate

        if next_point == bottom_point:
            break
        jarvis_points.append(next_point)
        current_point = next_point

        jarvis_points.insert(0, bottom_point)

    return [[p.x, p.y] for p in jarvis_points]

