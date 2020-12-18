import time
from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code2.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return [c for c in line.strip()]

def findAdj4d(x, y, z, w):
    adjacent = []
    for x2 in (x, x-1, x+1):
        for y2 in (y, y-1,y+1):
            for z2 in (z, z-1, z+1):
                for w2 in (w, w-1, w+1):
                    if (x2,y2,z2,w2) != (x,y,z,w):
                        adjacent.append(tuple([x2, y2, z2, w2]))
    return adjacent


def countAdjType4d(activeCoords, x, y, z, w):
    adjacent = findAdj4d(x, y, z, w)
    count = 0
    for a in adjacent:
        if a in activeCoords:
            count += 1
    return count

###########################
# part2
###########################
def part2(data):
    print(data)

    activeCoords = set()
    for y in range(len(data)):
        row = data[y]
        for x in range(len(row)):
            item = row[x]
            if item == "#":
                activeCoords.add(tuple([x, y, 0, 0]))
    print(activeCoords)

    # do one round
    for t in range(1, 7):

        nextActive = set()

        # find all possible neighbors of active things
        allPossibleNeighbors = set()
        for (x, y, z, w) in activeCoords:
            for a in findAdj4d(x, y, z, w):
                allPossibleNeighbors.add(a)
        # print(allPossibleNeighbors)

        # for each possible neighbor, count its active neighbors
        for (x, y, z, w) in allPossibleNeighbors:
            numActive = countAdjType4d(activeCoords, x, y, z, w)
            if (x, y, z, w) in activeCoords:
                if numActive == 2 or numActive == 3:
                    nextActive.add(tuple([x,y,z,w]))
            else:
                if numActive == 3:
                    nextActive.add(tuple([x,y,z,w]))
        activeCoords = deepcopy(nextActive)

    print("Total bugs:",len(activeCoords))

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 2 RESULT")
    runpart2()
