import time
import sys
import numpy as np
from copy import deepcopy
import math
import random
from lib.print import print_2d_grid
from year_2020.day_20 import helpers

# puzzle problem with finding a pattern

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

def getTileConfigurations(tile):
    res = []
    for i in range(4):
        res.append(np.rot90(tile, k=i))
    t = np.fliplr(tile)
    for i in range(4):
        res.append(np.rot90(t, k=i-4))
    return res

def checkFit(x, y, x2, y2, currentTile, rot):
    # right
    if (x2, y2) == (x + 1, y):
        return (currentTile[:,-1] == rot[:,0]).all()
    # down
    elif (x2,y2) == (x, y + 1):
        return (currentTile[-1,:] == rot[0,:]).all()
    # left
    elif (x2, y2) ==  (x - 1, y):
        return (currentTile[:,0] == rot[:,-1]).all()
    # up
    elif (x2, y2) == (x, y - 1):
        return (currentTile[:,-1] == rot[:,0]).all()
    else:
        print("Whoops")
        sys.exit(1)

###########################
# part1
###########################
def part1(data):
    tileBorders = {}
    # for each tile, store its 4 borders
    for tileNum, grid in data:
        # top, right, bottom, left
        tileBorders[tileNum] = [grid[0,:], grid[:,-1], grid[-1,:], grid[:,0]]
    print(tileBorders)

    matches = {}
    # init matches
    # by inspection we found that all matches are unique and 1-1
    for tileNum, _ in data:
        matches[tileNum] = {0: None, 1: None, 2: None, 3: None}

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
                        matches[tileNum][b1] = tileNum2
                        # print(borders[b1], borders2[b2])
                        # print()
                    # check flipped matches
                    if (borders[b1] == np.flip(borders2[b2])).all():
                        # print(tileNum, b1, "matches flip", tileNum2, b2+4)
                        matches[tileNum][b1] = tileNum2
                        # print(borders[b1], borders2[b2])
                        # print()
    print(matches)

    # find corners... the 4 tiles with exactly 2 matches for 2 adjacent sides
    corners = []
    for tileNum in matches:
        sides = matches[tileNum]
        if (sides[0] and sides[1] and not sides[2] and not sides[3]) or \
            (sides[1] and sides[2] and not sides[3] and not sides[0]) or \
            (sides[2] and sides[3] and not sides[0] and not sides[1]) or \
            (sides[3] and sides[0] and not sides[1] and not sides[2]):
            corners.append(tileNum)

    print("Corners",corners)
    # add corner id nums
    res = 1
    for corner in corners:
        print(corner, matches[corner])
        res *= corner
    print("PROD", res)
    return matches, corners

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def getTileNumMatchingTileNums(tileNum, matches):
    d = matches[tileNum]
    res = []
    for v in d.values():
        if v is not None:
            res.append(v)
    return res


def tileGridToSingleGrid(tileGrid):
    grid = []
    for row in tileGrid:
        trimmedRow = []
        for tile in row:
            t1 = tile[1:-1, :] # remove first and last row
            t2 = t1[:, 1:-1] # remove first and las col
            trimmedRow.append(t2)
        newRow = np.concatenate(trimmedRow, axis=1)
        # newRow = np.concatenate(row, axis=1)
        grid.append(newRow)
    grid = np.concatenate(grid, axis=0)
    return grid

def fillNeighbors(tileNum, x, y, matches, tiles, biggoGriddo, tileGrid):
    # get current tile
    currentTile = tileGrid[y][x]
    # get this tile's matched tile ids
    matchingIds = getTileNumMatchingTileNums(tileNum, matches)
    # print("matching ids", matchingIds)
    # for each 4 adj spots
    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
        if 0 <= x2 < len(biggoGriddo[0]) and 0 <= y2 < len(biggoGriddo):
            nextItem = biggoGriddo[y2][x2]
            # if spot contains match, remove it
            if nextItem in matchingIds:
                matchingIds.remove(nextItem)
            elif nextItem is not None:
                print("RUH ROH")
                sys.exit(1)
            # if a spot is empty
            else:
                # for each unmatched tile id
                for matchingId in matchingIds:
                    # assume tile not already in the grid
                    # try each tile rotation here
                    tileRots = getTileConfigurations(tiles[matchingId])
                    foundMatch = False
                    for rot in tileRots:
                        # check if this tile fits, based on x,y,x2,y2
                        if checkFit(x,y,x2,y2,currentTile,rot):
                            biggoGriddo[y2][x2] = matchingId
                            tileGrid[y2][x2] = rot
                            fillNeighbors(matchingId, x2, y2, matches, tiles, biggoGriddo, tileGrid)
                            foundMatch = True
                            break
                    if foundMatch:
                        break

def part2(data):

    matches, corners = part1(data)

    # hold the np arrays by tile id
    tiles = {}
    for tileNum, tile in data:
        tiles[tileNum] = tile

    dim = int(math.sqrt(len(data)))

    # a grid of grids
    biggoGriddo = []
    tileGrid = []
    for j in range(dim):
        row = []
        for i in range(dim):
            row.append(None)
        biggoGriddo.append(row)
        tileGrid.append(deepcopy(row))

    # pick upper left corner, where tile is upright
    for corner in corners:
        match = matches[corner]
        if match[1] and match[2]:
            biggoGriddo[0][0] = corner
            tileGrid[0][0] = tiles[corner]
            break
    # print(biggoGriddo)
    upperLeft = biggoGriddo[0][0]
    x, y = (0, 0)
    print("Upper left", upperLeft)

    # fill neighbors in both grids
    fillNeighbors(upperLeft, x, y, matches, tiles, biggoGriddo, tileGrid)
    # print(biggoGriddo)
    # smash the grids together
    resultGrid = tileGridToSingleGrid(tileGrid)
    # print_2d_grid(resultGrid)

    # find and mark the dragons!
    # this prints the result
    helpers.findSeaMonstersAndGetCount(resultGrid)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
