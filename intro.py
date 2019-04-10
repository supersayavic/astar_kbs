import csv
import argparse

# globale Variablen
fieldType = []
costs = []

# creates the field
# file is the input file that the user provides
def fieldcreation(file):

    return list(list(item for item in line.rstrip("\n\r").split(";")) for line in file)

# node class
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

# a star function(fieldInput fron user, start position, end position (Krone), medaillon array)
def astar(maze, start, end, medaillons):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    ## 1
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

        ## 2
        # Found the goal
        # Set medaillon true
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current)
                current = current.parent
            return path[::-1]  # Return reversed path

        ## 3
        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            ## 3.1
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            ## 3.2
            # Check if water
            if not current_node.medaillon and str(maze[node_position[0]][node_position[1]]) == str(0):
                continue # terrain not walkable

            ## 3.3
            # Check if node has medaillon and if L1 -> L3
            if current_node.medaillon and str(maze[current_node.position[0]][current_node.position[1]]) == str(1) and str(maze[node_position[0]][node_position[1]]) == str(3):
                continue

            # Check if node has medaillon and if L3 -> L1
            if current_node.medaillon and str(maze[current_node.position[0]][current_node.position[1]]) == str(3) and str(maze[node_position[0]][node_position[1]]) == str(1):
                continue

            ## 3.4
            # check if the current node is a medaillon field
            # compares input values from item file with current position of the node
            # if the coordinates are equal, the medaillon attribute is set true
            medaillon = current_node.medaillon
            if(not medaillon):
                for medPos in medaillons:
                    if medPos == node_position:
                        medaillon = True
                        break

            ## 3.5
            # Create new node
            new_node = Node(current_node, node_position, medaillon)

            # Append
            children.append(new_node)

        ## 4
        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            ## 4.1
            # Create the f, g, and h values
            # if node moves in water, adds 2 instead of 1 for g
            if child.medaillon and str(maze[child.position[0]][child.position[1]]) == str(0):
                child.g = current_node.g + 2
            else:
                child.g = current_node.g + 1

            ## 4.2
            # determines h value according to the neighbor nodes, end node and the medaillons
            # see function
            child.h = calcHvalue(child, end_node, medaillons)
            # cals f value
            child.f = child.g + child.h

            ## 4.3
            # Child is already in the open list
            betterChildFound = False
            for open_node in open_list:
                if child == open_node:
                    if child.g > open_node.g:
                        betterChildFound = True
                        break
                    else:
                        betterChildFound= True
                        open_node.g = child.g
                        open_node.parent = child.parent
                        open_node.f = child.f
                        break
            if betterChildFound:
                continue

            ## 5
            # Add the child to the open list
            open_list.append(child)

# calculates the total distance according to the number of inserted medaillons
# chooses the shortest path
def calcHvalue (node, end_node, medaillons):
    # if we already start on a medaillon, go directly to the crown
    if(node.medaillon):
        return abs(node.position[0]-end_node.position[0]) + abs(node.position[1]-end_node.position[1])
    #
    else:
        # calculates a reference distance that is used for comparison with the next medaillon
        minimum = ((abs(node.position[0]-medaillons[0][0]) + abs(node.position[1]-medaillons[0][1])) + (abs(node.position[0]-medaillons[0][0]) + abs(node.position[1]-medaillons[0][1])))
        for m in medaillons:
            # compares the two paths and writes the smaller one into the variable
            minimum = min(minimum, ((abs(node.position[0]-m[0]) + abs(node.position[1]-m[1])) + (abs(node.position[0]-m[0]) + abs(node.position[1]-m[1]))))
        return minimum


def main():
    parser = argparse.ArgumentParser(description='WBS - Suche B_A1')
    parser.add_argument('-x', dest='x', help='X Start coordingate', nargs='?', type=int, required=True)
    parser.add_argument('-y', dest='y', help='Y Start coordingate', nargs='?', type=int, required=True)
    parser.add_argument('--field', dest='file', help='Set field from a file', nargs='?', type=argparse.FileType('r'), required=True)
    parser.add_argument('--items', dest='items', help='Set items from a file', nargs='?', type=argparse.FileType('r'), required=True)
    args = parser.parse_args()

    file = args.file
    fieldType = fieldcreation(file)
    field = fieldType

    start = (args.x, args.y)
    end = (-1, -1)
    items = []

    for line in args.items:
        lineSplit = line.split(";")
        if lineSplit[0] == "Medaillon":
            items.append((int(lineSplit[1]), int(lineSplit[2])))
        if lineSplit[0] == "Krone":
            end = (int(lineSplit[1]), int(lineSplit[2]))

    ## only used for debugging
    # def stuff(x):
    #     if x < 10:
    #         return f'0{x}'
    #     return str(x)
    # def foo(x, y, item):
    #     if (x, y) in items:
    #         return f'({stuff(x)},{stuff(y)}) {item} M '
    #     if (x, y) == end:
    #         return f'({stuff(x)},{stuff(y)}) {item} K '
    #     return f'({stuff(x)},{stuff(y)}) {item}   '
    #
    # for x, item in enumerate(fieldType):
    #     print("; ".join(map(lambda bar: foo(x, bar[0], bar[1]), enumerate(item))))

    path = astar(field, start, end, items)

    if(not path):
        print('No path was found. Start position is be surrounded by water.')
    else:
        for x in path:
            print(x)

if __name__ == '__main__':
    main()