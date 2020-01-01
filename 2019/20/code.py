from collections import deque
import networkx as nx

###########################
# helpers
###########################
width = 122 # specific to input

def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    l = [char for char in line.strip("\n").ljust(width, ' ')]
    print(l)
    return l

emptyChar = "."
wallChar = "#"

def findDoors(grid):
    doors = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            char = grid[y][x]
            if char == emptyChar:
                # check up
                x2, y2 = (x, y - 1)
                if grid[y2][x2].isalpha():
                    x3, y3 = (x, y - 2)
                    s = grid[y3][x3] + grid[y2][x2]
                    doors.append((s, (x,y)))

                # check left
                x2, y2 = (x - 1, y)
                if grid[y2][x2].isalpha():
                    x3, y3 = (x - 2, y)
                    s =  grid[y3][x3] + grid[y2][x2]
                    doors.append((s, (x,y)))

                # check right
                x2, y2 = (x + 1, y)
                if grid[y2][x2].isalpha():
                    x3, y3 = (x + 2, y)
                    s = grid[y2][x2] + grid[y3][x3]
                    doors.append((s, (x,y)))

                # check down
                x2, y2 = (x, y + 1)
                if grid[y2][x2].isalpha():
                    x3, y3 = (x, y + 2)
                    s =  grid[y2][x2] + grid[y3][x3]
                    doors.append((s, (x,y)))

    return doors

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def bfs(grid, start, end):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                if grid[y2][x2] == emptyChar:
                    if (x2, y2) not in seen:
                        queue.append(path + [(x2,y2)])
                        seen.add((x2,y2))

def getPairs(source):
    result = []
    for p1 in range(len(source)):
        for p2 in range(p1 + 1, len(source)):
            result.append([source[p1], source[p2]])
    return result

###########################
# part1
###########################
def part1(grid):
    printGrid(grid)
    doors = findDoors(grid)
    print("doors", doors)

    start = end = None
    for door in doors:
        if door[0] == "AA":
            start = door
        elif door[0] == "ZZ":
            end = door

    # construct a graph where
    #  - each door is a node
    #  - edges between different doors are weighted as the number of steps
    #  - edges between same doors are weight 0
    G = nx.Graph()
    # add nodes
    for door, coord in doors:
        G.add_node((door, coord))

    # add edges between different doors
    for pair in getPairs(doors):
        door, coord = pair[0]
        door2, coord2 = pair[1]
        if coord != coord2 and not G.has_edge(door2, door):
            if door != door2:
                path = bfs(grid, coord, coord2)
                if path is not None:
                    w = len(path)-1
                    print("adding", w, "edge",(door, coord), (door2, coord2))
                    G.add_edge((door, coord), (door2, coord2), weight=w)
            else: # same door, so it's a free portal
                print("adding 0 edge",(door, coord), (door2, coord2))
                G.add_edge((door, coord), (door2, coord2), weight=1)
    res = nx.shortest_path_length(G, start, end, weight='weight')
    print("answer",res)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(grid):
    printGrid(grid)
    doors = findDoors(grid)
    num_layers = 30

    # distinguish between inner and outer doors
    newdoors = []
    for door, coord in doors:
        x, y = coord
        # outer door
        if y == 2 or x == 2 or y == 116 or x == 118:
            newdoors.append((door, coord, True))
        else:
            newdoors.append((door, coord, False))
    doors = newdoors
    print("doors", doors)

    # set start and end
    start = end = None
    for door in doors:
        if door[0] == "AA":
            start = (0, door[0], door[1], door[2])
        elif door[0] == "ZZ":
            end = (0, door[0], door[1], door[2])

    # construct a graph where
    # for each "layer":
    #  - each door is a node
    #  - edges between different doors are weighted as the number of steps
    #  - edges between same doors in the different layers are weight 1
    G = nx.Graph()

    # for each layer, add doors and edges within that layer
    for i in range(num_layers):
        # add nodes
        for door, coord, isOuter in doors:
            # only add these to the first layer
            if door == "AA" or door == "ZZ":
                if i == 0:
                    G.add_node((i, door, coord, isOuter))
                    print("add node",(i, door, coord, isOuter))
                    continue
                else:
                    continue
            # for the first layer, don't add outer doors
            if isOuter and i == 0:
                continue
            # for the last layer, don't add inner doors
            if not isOuter and i == num_layers - 1:
                continue
            G.add_node((i, door, coord, isOuter))
            print("add node",(i, door, coord, isOuter))

        # add edges between different doors in this layer
        for pair in getPairs(doors):
            door, coord, isOuter = pair[0]
            door2, coord2, isOuter2 = pair[1]
            u = (i, door, coord, isOuter)
            v = (i, door2, coord2, isOuter2)
            # make sure we have both nodes (e.g. not outer for first layer)
            if G.has_node(u) and G.has_node(v):
                if door != door2 and coord != coord2 and not G.has_edge(u, v):
                    path = bfs(grid, coord, coord2)
                    if path is not None:
                        w = len(path)-1
                        print("adding", w, "edge",u, v)
                        G.add_edge(u, v, weight=w)

    # add edges between layers....
    # connect inner to outer
    for i in range(num_layers-1):
        for door, coord, isOuter in doors:
            for door2, coord2, isOuter2 in doors:
                if door == door2 and coord != coord2 and not isOuter:
                    G.add_edge((i, door, coord, isOuter), (i+1, door2, coord2, isOuter2), weight=1)
                    print("adding", 1, "layer jump",(i, door, coord, isOuter), (i+1, door2, coord2, isOuter2))

    # Find the shortest path
    res = nx.shortest_path_length(G, start, end, weight='weight')
    print("answer",res)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
