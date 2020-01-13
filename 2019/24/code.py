from copy import deepcopy
from lib.print import print_2d_grid

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return [char for char in line.strip()]

def countAdjType(board, x, y, target="#"):
    count = 0
    for x2, y2 in ((x, y-1), (x-1, y), (x+1, y), (x, y+1)):
        if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] == target:
            count += 1
    return count

def oneMinute(board):
    nextBoard = deepcopy(board)
    for y in range(0,len(board)):
        row = board[y]
        for x in range(0, len(row)):
            item = row[x]
            # bug
            if item == "#":
                numBugs = countAdjType(board,x,y)
                if numBugs != 1:
                    nextBoard[y][x] = "."
            elif item == ".":
                numBugs = countAdjType(board,x,y)
                if numBugs == 1 or numBugs == 2:
                    nextBoard[y][x] = "#"
    return nextBoard

def calcBio(board):
    total = 0
    for y in range(0,len(board)):
        row = board[y]
        for x in range(0, len(row)):
            item = row[x]
            if item == "#":
                pow = 2 ** (x + (len(row)*y))
                print("adding",x,y,"as",pow)
                total += pow
    return total


###########################
# part1
###########################
def part1(board):
    print_2d_grid(board)
    prevBoards = [deepcopy(board)]
    numIters = 1
    while True:
        board = oneMinute(board)
        # check previous boards
        for prevBoard in prevBoards:
            if board == prevBoard:
                print("SAME")
                print_2d_grid(board)
                print("answer:",calcBio(board))
                exit(0)
        print(numIters)
        numIters += 1
        print_2d_grid(board)
        print("")
        prevBoards.append(deepcopy(board))

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def getEmptyLayer():
    board = []
    for y in range(5):
        row = []
        for x in range(5):
            if x == 2 and y == 2:
                row.append("?")
            else:
                row.append(".")
        board.append(row)
    return board

def printLayers(layers):
    for i in sorted(layers.keys()):
        print("Layer",i)
        print_2d_grid(layers[i])
        print()

def countBugs(layer):
    total = 0
    for row in layer:
        for item in row:
            if item == "#":
                total += 1
    return total

def findAdj(x, y, z):
    # ignore center square
    if (x,y) == (2,2):
        return []

    adjacent = []

    # look left
    if x == 0:
        # looking out
        adjacent.append((1, 2, z - 1))
    elif (x, y) == (3, 2):
        # looking in
        adjacent.extend((4, yy, z + 1) for yy in range(5))
    else:
        adjacent.append((x - 1, y, z))

    # look right
    if x == 4:
        # looking out
        adjacent.append((3, 2, z - 1))
    elif (x, y) == (1, 2):
        # looking in
        adjacent.extend((0, yy, z + 1) for yy in range(5))
    else:
        adjacent.append((x + 1, y, z))

    # look up
    if y == 0:
        # looking out
        adjacent.append((2, 1, z - 1))
    elif (x, y) == (2, 3):
        # looking in
        adjacent.extend((xx, 4, z + 1) for xx in range(5))
    else:
        adjacent.append((x, y - 1, z))

    # look down
    if y == 4:
        # looking out
        adjacent.append((2, 3, z - 1))
    elif (x, y) == (2, 1):
        # looking in
        adjacent.extend((xx, 0, z + 1) for xx in range(5))
    else:
        adjacent.append((x, y + 1, z))

    return adjacent



def countAdjType3d(layers, x, y, z, target="."):
    adjacent = findAdj(x,y,z)

    board = layers[z]
    ch = board[y][x]
    count = 0

    for x2, y2, z2 in adjacent:
        if layers.get(z2) is None:
            continue
        if layers[z2][y2][x2] == "#":
            count += 1
    return count

def oneMinute2(layers):
    nextLayers = {}
    for i in layers:
        board = layers[i]
        nextBoard = deepcopy(board)
        for y in range(0,len(board)):
            row = board[y]
            for x in range(0, len(row)):
                if (x,y) == (2,2):
                    continue
                item = row[x]
                # bug
                if item == "#":
                    numBugs = countAdjType3d(layers,x,y,i)
                    if numBugs == 1:
                        nextBoard[y][x] = "#"
                    else:
                        nextBoard[y][x] = "."
                else:
                    numBugs = countAdjType3d(layers,x,y,i)
                    if numBugs == 1 or numBugs == 2:
                        nextBoard[y][x] = "#"
                    else:
                        nextBoard[y][x] = "."
        nextLayers[i] = nextBoard
    return nextLayers

def part2(data):
    print(data)

    # set question mark spot
    data[2][2] = "?"

    # keep track of layers in a dict
    # initialize with layer 0, and an empty top and bottom layer
    layers = {
        -1: getEmptyLayer(),
        0: deepcopy(data),
        1: getEmptyLayer()
    }

    printLayers(layers)

    # pass time
    for t in range(1, 201):
        # pass a minute
        layers = oneMinute2(layers)

        sortedLayers = sorted(layers.keys())

        # if the lowest layer has a bug, add another empty layer on bottom
        lowestLayer = sortedLayers[0]
        lowestCount = countBugs(layers[lowestLayer])
        if lowestCount > 0:
            layers[lowestLayer-1] = getEmptyLayer()

        # if the highest layer has a bug, add another empty layer on top
        highestLayer = sortedLayers[-1]
        highestCount = countBugs(layers[highestLayer])
        if highestCount > 0:
            layers[highestLayer+1] = getEmptyLayer()

        print("Time",t)
        printLayers(layers)


    # count the number of bugs in all layers
    totalBugs = 0
    for i in layers:
        totalBugs += countBugs(layers[i])
    print("Total bugs:",totalBugs)


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
