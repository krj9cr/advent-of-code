import time
from copy import deepcopy
from lib.print import print_2d_grid

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return [c for c in line.strip()]

def findAdj3d(x, y, z):
    adjacent = []
    for x2 in (x, x-1, x+1):
        for y2 in (y, y-1,y+1):
            for z2 in (z, z-1, z+1):
                if (x2,y2,z2) != (x,y,z):
                    adjacent.append(tuple([x2, y2, z2]))
    return adjacent

def countAdjType3d(layers, x, y, z):
    adjacent = findAdj3d(x, y, z)
    count = 0
    for x2, y2, z2 in adjacent:
        if (x2,y2,z2) in layers:
            count += 1
    return count

###########################
# part1
###########################
def part1(data):
    activeCoords = set()
    for y in range(len(data)):
        row = data[y]
        for x in range(len(row)):
            item = row[x]
            if item == "#":
                activeCoords.add(tuple([x, y, 0]))
    print(activeCoords)

    # do one round
    for t in range(1, 7):

        nextActive = set()

        # find all possible neighbors of active things
        allPossibleNeighbors = set()
        for (x, y, z) in activeCoords:
            for a in findAdj3d(x, y, z):
                allPossibleNeighbors.add(a)

        # for each possible neighbor, count its active neighbors
        for (x, y, z) in allPossibleNeighbors:
            numActive = countAdjType3d(activeCoords, x, y, z)
            if (x, y, z) in activeCoords:
                if numActive == 2 or numActive == 3:
                    nextActive.add(tuple([x,y,z]))
            else:
                if numActive == 3:
                    nextActive.add(tuple([x,y,z]))
        activeCoords = deepcopy(nextActive)

    print("Total bugs:",len(activeCoords))

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()
