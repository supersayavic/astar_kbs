import csv
import argparse

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

    def __init__(self, parent=None, position=None, medaillon=False):
        self.parent = parent
        self.position = position
        self.medaillon = medaillon

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position[0] == other.position[0] and self.position[1] == other.position[1] and self.medaillon == other.medaillon

    def __repr__(self):
        return f'({self.position[0]}, {self.position[1]}, {self.medaillon}) g={self.g} h={self.h} f={self.f}'


def astar(maze, start, end, medaillons):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end, medaillon=True)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []


    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        # search for item in openlist that has smaller f than current item
        # if found
        current_node = open_list[0]
        current_index = 0
        # item = (1, 2) Koordinate
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        # Found the goal
        # Set medaillon true
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Check if water
            if not current_node.medaillon and str(maze[node_position[0]][node_position[1]]) == str(0):
                continue # terrain not walkable

            if current_node.medaillon and str(maze[current_node.position[0]][current_node.position[1]]) == str(1) and str(maze[node_position[0]][node_position[1]]) == str(3):
                continue

            if current_node.medaillon and str(maze[current_node.position[0]][current_node.position[1]]) == str(3) and str(maze[node_position[0]][node_position[1]]) == str(1):
                continue

            medaillon = current_node.medaillon

            if(not medaillon):
                for medPos in medaillons:
                    if medPos == node_position:
                        medaillon = True
                        break

            # Create new node
            new_node = Node(current_node, node_position, medaillon)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:   # Here was a fail...
                continue


            # Create the f, g, and h values
            # if current_node.medaillon == true and child.value == 0
            # child.g = current_node.g + 2
            if child.medaillon and str(maze[node_position[0]][node_position[1]]) == str(0):
                child.g = current_node.g + 2
            else:
                child.g = current_node.g + 1
            child.h = calcHvalue(child, end_node, medaillons)
            child.f = child.g + child.h

            # Child is already in the open list
            betterChildFound = False
            for open_node in open_list:
                if child == open_node:
                    if child.g > open_node.g:
                        betterChildFound = True
                        break # will only break inner for loop not outer that was the problem here # FAIL
                    else:
                        betterChildFound= True
                        open_node.g = child.g
                        open_node.parent = child.parent
                        open_node.f = child.f
                        break
            if betterChildFound:
                continue

            # Add the child to the open list
            open_list.append(child)
    print("No Path was found to bad")


def calcHvalue (node, end_node, medaillons):
    # raise BaseException('Not yet implemented')
    if(node.medaillon):
        return abs(node.position[0]-end_node.position[0]) + abs(node.position[1]-end_node.position[1])
    else:
        minimum = ((abs(node.position[0]-medaillons[0][0]) + abs(node.position[1]-medaillons[0][1])) + (abs(node.position[0]-medaillons[0][0]) + abs(node.position[1]-medaillons[0][1])))
        for m in medaillons:
            minimum = min(minimum, ((abs(node.position[0]-m[0]) + abs(node.position[1]-m[1])) + (abs(node.position[0]-m[0]) + abs(node.position[1]-m[1]))))
        return minimum


def main():
    parser = argparse.ArgumentParser(description='WBS foo')
    parser.add_argument('-x', dest='x', help='X Start coordingate', nargs='?', type=int, required=True)
    parser.add_argument('-y', dest='y', help='Y Start coordingate', nargs='?', type=int, required=True)
    parser.add_argument('--spielfeld', dest='file', help='Set field from a file', nargs='?', type=argparse.FileType('r'), required=True)
    parser.add_argument('--other', dest='medaillon', help='Set items from a file', nargs='?', type=argparse.FileType('r'), required=True)
    args = parser.parse_args()

    file = args.file
    fieldcreation(file)
    field = fieldType

    start = (args.x, args.y)
    end = (-1, -1)
    medaillons = []
    for line in args.medaillon:
        lineSplit = line.split(";")
        if lineSplit[0] == "Medaillon":
            medaillons.append((int(lineSplit[1]), int(lineSplit[2])))
        if lineSplit[0] == "Krone":
            end = (int(lineSplit[1]), int(lineSplit[2]))

    path = astar(field, start, end, medaillons)

    #astar muss path und kosten returnen
    for x in path:
        print(x)

# main methode aufrufen wenn datei ausgeführt wird
if __name__ == '__main__':
    main()