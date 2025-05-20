# Projekt symulacja maksymalnego przesy w miescie Shire

## Wymagania:

- Python 3.8+
- matplotlib

## Uruchamianie:
`python main.py`

## Struktura projektu

#### Dane wejsciowe w katalogu data/ 

dane wejściowe w formacie json dzięki których budujemy obiekty w programie (zakładamy z góry ze miasto ma wielkość 10x10 na układzie współrzędnych)
- `fields.json`: (pola z danymi)  `id`, `x`, `x`

- `inns.json`: (karczmy z danymi) `id`, `x`, `y`, `demand`

- `breweries.json`: (browary z danymi) `id`, `x`, `y`, `capacity`

- `roads.json`: (drogi z danymi) `id`, `from: [x,y]`, `to: [x,y]`, `capacity`, `repair_cost`

- `sectors.json`: (sektory shire z danymi) `id`, `polygon: [[x,y],...,[x,y]]`, `yield`

### Struktura w katalogu models
- `city.py` Klasa reprezentujaca model miasta z polami takimi jak:
- - `field.py` Klasa reprezentująca pole
- - `inn.py` Klasa reprezentująca karczme
- - `breweries.py` Klasa reprezentująca browar
- - `road.py` Klasa reprezentująca drogę
- - `sector.py` Klasa reprezentująca sektor shire

### Struktura katalogu utils
`algo.py` Algorytmy geometryczne z funkcjami do obliczania:

Przekazujemy w tych funkcjach obiekt punktu który posiada poprostu współrzędną x i y`Point(x,y)`

- wzajemnego polożenia dwóch punktów na płaszczyźnie `orientation(p1: Point, p2: Point, p3: Point)`
- czy dany punkt należy do danego odcinka `is_point_on_segment(p: Point, start: Point, end: Point)`
- czy dwa dane odcinki się przecinają `do_segments_intersects(p1: Point, p2: Point, p3: Point, p4: Point)`
- czy dane punkty należą do danego wielokąta wypukłego `is_point_inside_polygon(p: Point, polygon: list[Point])`

`algo.py` Algorytmy do obliczania największej przepustowości miasta

`plotter.py` Funkcja przyjmująca parametry miasta i następnie wyświetla odpowiednią mape miasta:
- `plot_city(
    city: City,
    show_capacity=False,
    show_sector_yield=True
    )`
