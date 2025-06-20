from utils.geometry import Point
from utils.geometry import orientation
from math import sqrt


def distance(p1: Point, p2: Point) -> float:
    return sqrt(((p1.x - p2.x)*(p1.x - p2.x)) + ((p1.y - p2.y)*(p1.y - p2.y)))


def convert_to_jarvis_points(points) -> list[list[float]]:
    jarvis_points: list[Point] = []
    input_points: list[Point] = [Point(p[0], p[1]) for p in points]

    if len(input_points) < 3:
        return points

    bottom_point: Point = min(input_points, key=lambda p: (p.y, p.x))
    jarvis_points.append(bottom_point)

    current_point = bottom_point

    while True:
        next_point = input_points[0]
        for candidate in input_points:
            if candidate == current_point:
                continue
            det = orientation(current_point, next_point, candidate)
            if det > 0 or (det == 0 and distance(current_point, candidate) > distance(current_point, next_point)):
                next_point = candidate

        if next_point == bottom_point:
            break

        jarvis_points.append(next_point)
        current_point = next_point

    return [[p.x, p.y] for p in jarvis_points]
