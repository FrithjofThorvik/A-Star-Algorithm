import math
from Node import Node


def get_neighbors_from_node(node):
    # Get array of neighbor positions
    (x, y) = node.pos  # Fetch x & y from current node position
    neighbors = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]  # Create array of  the 4 neighbor positions
    return neighbors


class AStar:
    """A* algorithm implementation taking in a Map_Object instance, finds the shortest path to the goal, and fills
    out the path on the map"""

    def __init__(self, map):
        self.map = map
        self.start_node = Node(map.get_start_pos())
        self.end_node = Node(map.get_goal_pos())
        self.open_set = []
        self.closed_set = []
        self.find_shortest_path()

    def find_shortest_path(self):
        # Finds the shortest path on the map instance of the object
        node0 = self.start_node  # Init start node
        node0.h = self.heuristic(node0)  # Set node's heuristic cost
        node0.f = node0.g + node0.h  # Set estimated total cost
        self.open_set.append(node0)  # Add node to open set

        while len(self.open_set) > 0:
            # Loop through nodes until open set has been emptied out
            self.open_set.sort()  # Sort open set based on the total cost of nodes
            current_node = self.open_set.pop(0)  # Fetch the first node from sorted open set
            self.closed_set.append(current_node)  # Add current node to closed set

            if current_node == self.end_node:
                # Check if end node has been reached
                path = []  # Initialize path to store shortest path

                while current_node != self.start_node:
                    # Loop through all nodes until start node has been reached
                    path.append(current_node.pos)  # Append node position to path
                    current_node = current_node.parent  # Update current node to parent node
                self.show_path(path)
                return path

            neighbors = get_neighbors_from_node(current_node)

            for neighbor in neighbors:
                # Loop through node neighbors
                if self.map.get_cell_value(neighbor) == -1:
                    # Check if neighbor is an obstacle
                    continue

                neighbor_node = Node(neighbor, current_node)  # Create node instance with current node as parent

                if (neighbor_node not in self.open_set) and (neighbor_node not in self.closed_set):
                    # Check if neighbor node is not in open set or closed set. Node has not been reached before
                    # Attach the node to parent and calculate cost
                    self.attach_node_to_parent(neighbor_node, current_node)
                    self.open_set.append(neighbor_node)

                elif current_node.g + self.map.get_cell_value(current_node.pos) < neighbor_node.g:
                    # Check if neighbor node can be reached through current node with lower cost, update parent & cost
                    self.attach_node_to_parent(neighbor_node, current_node)

                    if neighbor_node in self.closed_set:
                        # Check if neighbor has been expanded, and propagate new path cost
                        self.propagate_path_improvements(neighbor_node)

        return False

    def heuristic(self, node):
        # Calculates heuristic distance between current node and end node
        x = (node.pos[0] - self.end_node.pos[0]) * 2
        y = (node.pos[1] - self.end_node.pos[1]) * 2
        return math.sqrt(abs(x) + abs(y))

    def attach_node_to_parent(self, node, parent):
        # Attaches node to parent and calculates different costs
        node.parent = parent  # Set parent node
        node.g = parent.g + self.map.get_cell_value(parent.pos)  # Set path cost to parent path cost + cost for moving
        # from parent to child
        node.h = self.heuristic(node)
        node.f = node.g + node.h

    def propagate_path_improvements(self, node):
        # Propagate path improvements through a node and it's parent
        neighbors = get_neighbors_from_node(node)

        for neighbor in neighbors:
            # Loop through neighbors
            neighbor_node = Node(neighbor)  # Get node instance

            if node.g + 1 < neighbor_node.g:
                # Check if path cost for node is less than neighbor node
                neighbor_node.parent = node
                neighbor_node.g = node.g + self.map.get_cell_value(node.pos)
                neighbor_node.h = self.heuristic(neighbor_node)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

    def show_path(self, path):
        # Updates the map with the given path
        for pos in path:
            self.map.set_cell_value(pos, "P")  # Update map cell value
        self.map.show_map()  # Display the entire map

