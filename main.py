from AStar import AStar
from Map import Map_Obj

for i in range(1, 5):
    # Loop through all maps
    current_map = Map_Obj(i)  # Get map instance
    optimal_path = AStar(current_map)  # Show map as image, and store optimal path

