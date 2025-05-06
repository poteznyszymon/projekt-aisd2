Projekt symulacja maksymalnego przesy w miescie Shire

Struktura projektu:

project/
│
├── main.py # Glowny program uruchamiajacy produkcje
├── data/example_2/ # Przykladowe dane wejsciowe w formacie JSON
├── models/ # Klasy obietkow uzywanych w projekcie
├── utils/ #
│ ├── algo.py # Algorytmy budowy i obliczania maksymalnego przesylu
│ ├── geometry.py # Operacje geometryczne (np. sprawdzanie przynależności punktu do sektora)
│ └── plotter.py # Wizualizacja miasta i sieci
└── README.md # Dokumentacja projektu

Wymagania:

- Pyhton 3.8+
- matplotlib

Uruchamianie:
python main.py

Dane wejsciowe w katalogu data/example_1/ :

- fields.json: pola uprawne

- inns.json: karczmy z zapotrzebowaniem

- breweries.json: browary z pojemnością

- roads.json: sieć dróg z kosztami i przepustowościami

- sectors.json: sektory z przypisanym plonem
