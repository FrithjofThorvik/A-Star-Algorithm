class Node:
    """Node objects contains information of the node's position, parent, and the different costs from A* algorithm"""

    def __init__(self, pos, parent=None):
        # Init node with position and parent, where parent can be none
        self.pos = pos
        self.parent = parent
        self.g = 0  # Path cost
        self.h = 0  # Heuristic cost
        self.f = 0  # Total cost

    def __eq__(self, other):
        # Overrides "=" operator to check for duplicates
        return self.pos == other.pos

    def __lt__(self, other):
        # Overrides "<" operator to sort nodes
        return self.f < other.f

    def __str__(self):
        # Defines representation of a node as string
        return str(self.pos)
