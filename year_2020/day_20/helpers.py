import numpy as np
import sys
from lib.print import print_2d_grid

###########################
# helpers
###########################
def parseMaskFile():
    with open((__file__.rstrip("helpers.py") + "mask.txt"), 'r') as file:
        return [[ c for c in line.strip('\n')] for line in file]

def parseExampleFile():
    with open((__file__.rstrip("helpers.py") + "example.txt"), 'r') as file:
        return [[ c for c in line.strip('\n')] for line in file]

def getGridSpotsMatchingMask(grid, maskGrid):
    rows = len(grid)
    columns = len(grid[0])

    maskRows = len(maskGrid)
    maskCols = len(maskGrid[0])

    spotMatches = []

    # Level 1: traversing the matrix
    for y in range(rows):
        for x in range(columns):
            spotMatchesMask = True

            # Level 2: traversing the window (3x3 size)
            for mask_y in range(0, maskRows):
                win_y = mask_y + y
                for mask_x in range(0, maskCols):
                    win_x = mask_x + x
                    if win_y >= columns or win_x >= rows:
                        spotMatchesMask = False
                        break
                    gridItem = grid[win_y][win_x]
                    maskItem = maskGrid[mask_y][mask_x]
                    if maskItem == "#" and gridItem != "#":
                        spotMatchesMask = False
                        break
                if not spotMatchesMask:
                    break
            if spotMatchesMask:
                # do it again and set everything to "O"?
                spotMatches.append(tuple([x, y]))
    return spotMatches

def markMatchingSpots(grid, maskGrid, spots):
    maskRows = len(maskGrid)
    maskCols = len(maskGrid[0])

    # Level 1: traversing the matrix
    for (x, y) in spots:
        # Level 2: traversing the window (3x3 size)
        for mask_y in range(0, maskRows):
            win_y = mask_y + y
            for mask_x in range(0, maskCols):
                win_x = mask_x + x
                gridItem = grid[win_y][win_x]
                maskItem = maskGrid[mask_y][mask_x]
                if maskItem == "#" and gridItem == "#":
                    grid[win_y][win_x] = "O"

def countGridHashes(grid):
    count = 0
    rows = len(grid)
    columns = len(grid[0])

    for y in range(rows):
        for x in range(columns):
            if grid[y][x] == "#":
                count += 1
    return count

def rotateGridUntilMatches(grid, maskGrid):
    spots = getGridSpotsMatchingMask(grid, maskGrid)
    if len(spots) > 0:
        return spots, grid

    i = 1
    grid2 = None
    while len(spots) == 0 and i < 4:
        grid2 = np.rot90(grid, k=i)
        spots = getGridSpotsMatchingMask(grid2, maskGrid)
        i += 1
    if len(spots) > 0:
        return spots, grid2

    grid2 = np.fliplr(grid)
    spots = getGridSpotsMatchingMask(grid2, maskGrid)
    if len(spots) > 0:
        return spots, grid2

    i = 1
    grid3 = None
    while len(spots) == 0 and i < 4:
        grid3 = np.rot90(grid2, k=i)
        spots = getGridSpotsMatchingMask(grid3, maskGrid)
        i += 1

    if len(spots) > 0:
        return spots, grid3
    else:
        print("nothing found :(")
        sys.exit(1)

def findSeaMonstersAndGetCount(grid):
    mask = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '#', '.'], ['#', '.', '.', '.', '.', '#', '#', '.', '.', '.', '.', '#', '#', '.', '.', '.', '.', '#', '#', '#'], ['.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '#', '.', '.', '.']]
    matchingCoords, newGrid = rotateGridUntilMatches(grid, mask)
    # print(matchingCoords)
    markMatchingSpots(newGrid, mask, matchingCoords)
    print_2d_grid(newGrid)
    res = countGridHashes(newGrid)
    print("res", res)
    return res

###########################
# test
###########################
if __name__ == '__main__':
    example = np.array(parseExampleFile())
    findSeaMonstersAndGetCount(example)
