from lib.Ebene import Ebene
# 0 = wasser
# 1 = land1
# 2 = land2
# 3 = land3
# f(x) = Gesamtkosten
# g(x) = Kosten vom aktuellen Startpunkt
# h(x) = Kosten vom aktuellen Punkt zum Ziel


import csv

# globale Variablen
fieldType = []
costs = []


def fieldcreation(file):
    datareader = csv.reader(file, delimiter=';')
    for row in datareader:
        if row[0] in (None, ""):
            break
        else:
            fieldType.append(row)


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other): # Vieleicht hat das schon vorher getan jetzt tut es auch ;)
        return self.position[0] == other.position[0] and self.position[1] == other.position[1]

    def __repr__(self):
        return f'({self.position[0]}, {self.position[1]}) g={self.g} h={self.h} f={self.f}'


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node: # Ausgabe fails...
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if str(maze[node_position[0]][node_position[1]]) != str(0):
                continue # terrain not walkable

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:   # Here was a fail...
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            betterChildFound = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    betterChildFound = True
                    break # will only break inner for loop not outer that was the problem here # FAIL
            if betterChildFound:
                continue

            # Add the child to the open list
            open_list.append(child)


def main():

    # start setzen 2/14
    # Krone setzen (7/15)
    # Medaillon (5/2)
    # Medaillon (10/15)
    # initialise playground
    file = open("spielfeld_2.csv", "r")
    fieldcreation(file)
    field = fieldType

    start = (0, 0)
    end = (3, 6)

    path = astar(field, start, end)
    print(path)

# main methode aufrufen wenn datei ausgeführt wird
if __name__ == '__main__':
    main()