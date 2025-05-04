import math

# Klasa punkt zeby prosciej przekazywac x i y obiektow zamiast uzywania listy
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Funckja do obliczania wzajemnego polozenia puntow na plaszczyznie
# Ktora zwaraca liczbe D:
# Jezeli D > 0 to p3 lezy po lewej stronie wektora p1p2
# Jezeli D < 0 to p3 lezy po prawej stronie wektora p1p2
# Jezeli D = 0 to punkty p1, p2, p3 sa wspolliniowe
def orientation(p1: Point, p2: Point, p3: Point) -> float:
    return (p2.x - p1.x) * (p3.y - p1.y)  - (p3.x - p1.x) * (p2.y - p1.y)


# Funckja ktora sprawdza czy punkt nalezy do odcinka
def is_point_on_segment(p: Point, start: Point, end: Point) -> bool:
    # Jezeli p nie sa wspolliniowe z ab to napewno p nienalezy do odcinka ab
    if orientation(start, end, p) != 0: return False
    # Teraz skoro p jest wspolliniowe z ab musimy sprawdzic czy lezy pomiedzy startem a koncem punktu ab
    min_x: int = min(start.x, end.x)
    max_x: int = max(start.x, end.x)
    min_y: int = min(start.y, end.y)
    max_y: int = max(start.y, end.y)
    
    return (min_x <= p.x <= max_x) and (min_y <= p.y <= max_y)

# Funckja ktora sprawdza czy dwa odcinki sie przecinaja 
def do_segments_intersects(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    # odcinki p1p2 oraz p3p4 przecinaja sie w sposob wlasciwy kiedy zachodzi:
    # D1 * D2 < 0 oraz D3 * D4 < 0
    # jezeli jakis D = 0 to sprawdzamy czy punkt nalezy do danego odcinka
    d1: float = orientation(p1, p2, p3)
    d2: float = orientation(p1, p2, p4)
    d3: float = orientation(p3, p4, p1)
    d4: float = orientation(p3, p4, p2)
    
    if (d1 == 0): return is_point_on_segment(p3, p1, p2)
    elif (d2 == 0): return is_point_on_segment(p4, p1, p2)
    elif (d3 == 0): return is_point_on_segment(p1, p3, p4)
    elif (d4 == 0): return is_point_on_segment(p2, p3, p4)
    
    if ((d1 * d2 < 0) and (d3 * d4 < 0)):
        return True
    
    return False

# Funkcja ktora sprawdza czy punkt nalezy do wielokatu wypuklego
# metoda ktora zlicza czy ilosc przeciec prostej z punkt p z 
# krawedziami wielokatu:
# jezeli liczba przeciec jest nieparzysta to p lezy wewnatrz wielokatu
# jezeli liczba przeciec jest parzysta to p lezy na zewnatrz wielokatu
def is_point_inside_polygon(p: Point, polygon: list[Point]) -> bool:
    # punkt "promien" z ktorym bedziemy sprawdzac ilosc przeciec
    extreme_point = Point(math.inf, p.y)
    n = len(polygon)
    count = 0

    for i in range(n):
        current_point = polygon[i]
        next_point = polygon[(i + 1) % n]
        
        if (do_segments_intersects(p, extreme_point, current_point, next_point)):
            if orientation(current_point, next_point, p) == 0:
                return is_point_on_segment(p, current_point, next_point)
            count += 1
    
    return count % 2 != 0