import time
import numpy as np
from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        # read lines
        rawlines = [line.strip() for line in file]

        # batch them into lists separated by empty line
        batchedlines = []
        currBatch = []
        for line in rawlines:
            if line != '':
                currBatch.append(line)
            else:
                tileNum = int(currBatch[0].replace("Tile ", "").replace(":", ""))
                grid = currBatch[1:]
                grid = [ [ char for char in row] for row in grid ]
                batchedlines.append(tuple([tileNum, np.array(grid)]))
                currBatch = []
        # last one
        tileNum = int(currBatch[0].replace("Tile ", "").replace(":", ""))
        grid = currBatch[1:]
        grid = [ [ char for char in row] for row in grid ]
        batchedlines.append(tuple([tileNum, np.array(grid)]))

        return batchedlines

def parseLine(line: str):
    return line.strip()

###########################
# part1
###########################
def part1(data):
    # print(data)
    # firstNum, firstGrid = data[0]

    tileBorders = {}
    # for each tile, store its 8 configurations
    for tileNum, grid in data:
        # top, right, bottom, left
        tileBorders[tileNum] = [grid[0,:], grid[:,-1], grid[-1,:], grid[:,0]]
    print(tileBorders)


    matches = {}
    # init matches
    for tileNum, _ in data:
        matches[tileNum] = {0: set(), 1: set(), 2: set(), 3: set()}

    # find some matches
    for tileNum in tileBorders:
        borders = tileBorders[tileNum]
        for tileNum2 in tileBorders:
            if tileNum2 == tileNum:
                continue
            borders2 = tileBorders[tileNum2]
            for b1 in range(len(borders)):
                for b2 in range(len(borders2)):
                    if (borders[b1] == borders2[b2]).all():
                        # print(tileNum, b1, "matches", tileNum2, b2)
                        matches[tileNum][b1].add(tuple([tileNum2, b2]))
                        # print(borders[b1], borders2[b2])
                        # print()
                    # check flipped matches
                    if (borders[b1] == np.flip(borders2[b2])).all():
                        # print(tileNum, b1, "matches flip", tileNum2, b2+4)
                        matches[tileNum][b1].add(tuple([tileNum2, b2+4]))
                        # print(borders[b1], borders2[b2])
                        # print()

    print(matches)

    # find corners... the 4 tiles with exactly 2 matches for 2 adjacent sides
    corners = []
    for tileNum in matches:
        sides = matches[tileNum]
        if (len(sides[0]) == len(sides[1]) == 1 and len(sides[2]) == len(sides[3]) == 0) or \
            (len(sides[1]) == len(sides[2]) == 1 and len(sides[3]) == len(sides[0]) == 0) or \
            (len(sides[2]) == len(sides[3]) == 1 and len(sides[0]) == len(sides[1]) == 0) or \
            (len(sides[3]) == len(sides[0]) == 1 and len(sides[1]) == len(sides[2]) == 0) == 1:
            # print("CORNERNRNNRNR",tileNum)
            corners.append(tileNum)

    print(corners)
    # add corner id nums
    res = 1
    for corner in corners:
        res *= corner
    print("PROD", res)


def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def part2(data):
    print(data)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\nPART 2 RESULT")
    # runpart2()
