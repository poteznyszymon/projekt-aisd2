import matplotlib.pyplot as plt
from models.field import Field
from models.breweries import Breweries
from models.inn import Inn
from models.road import Road
from models.sector import Sector


def plot_city(
    fields: list[Field],
    breweries: list[Breweries],
    inns: list[Inn],
    roads: list[Road],
    sectors: list[Sector],
    show_capacity=False,
    show_sector_yield=True
    ):
    # Staly rozmiar miasta 10 x 10
    plt.figure(figsize=(7, 7))
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.title("Mapa miasta Shire")
    
    colors = ["gold", "purple", "blueviolet", "hotpink"]
    
    for index, sector in enumerate(sectors):
        polygon = sector.polygon
        closed_polygon = polygon + [polygon[0]]
        x_coords = [point[0] for point in closed_polygon]
        y_coords = [point[1] for point in closed_polygon]
        plt.plot(x_coords, y_coords, color=colors[index], linestyle='-', linewidth=1, alpha=0.5)
        plt.fill(x_coords, y_coords, color=colors[index], alpha=0.1)
        
        if show_sector_yield:
            center_x = sum(point[0] for point in polygon) / len(polygon)
            center_y = sum(point[1] for point in polygon) / len(polygon)
            label = sector.sector_yield
            plt.text(center_x, center_y, label, 
                        ha='center', va='center',
                        fontsize=8, weight='bold',
                        color='darkred',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    
    for road in roads:
        start_x, start_y = road.start
        end_x, end_y = road.end
        plt.plot([start_x, end_x], [start_y, end_y], color="slategray", linestyle='-', linewidth=2)
        if show_capacity:
            plt.text((start_x + end_x )/ 2, (start_y + end_y) / 2, f"{road.capacity}", 
                            ha='center', va='center',
                            fontsize=8, weight='bold',
                            color='darkred',
                            bbox=dict(facecolor='slategray', edgecolor='none'))
        
    for index, field in enumerate(fields):
        plt.plot(field.x, field.y, color="green", linestyle='solid', linewidth=3, 
                marker='o')
        plt.text(field.x + 0.1, field.y + 0.1, f"Pole nr: {index + 1}")
        
    for index, brewery in enumerate(breweries):
        plt.plot(brewery.x, brewery.y, color="red", linestyle='solid', linewidth=3, 
                marker='o')
        plt.text(brewery.x + 0.1, brewery.y + 0.1, f"Browar nr: {index + 1}")
        
    for index, inn in enumerate(inns):
        plt.plot(inn.x, inn.y, color="blue", linestyle='solid', linewidth=3, 
                marker='o')
        plt.text(inn.x + 0.1, inn.y + 0.1, f"Karczma nr: {index + 1}")   
        
    plt.grid()
    plt.show()