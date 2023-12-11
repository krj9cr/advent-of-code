import copy
import time
import numpy as np

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [[ char for char in line.strip()] for line in file]
        return lines

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def manhattan_distance(a, b):
    return np.abs(a - b).sum()

def part1():
    grid = parseInput(11)
    print_2d_grid(grid)

    # expand the universe
    # find rows that have no galaxy
    newGrid = []
    for row in grid:
        hasGalaxy = False
        for char in row:
            if char == "#":
                hasGalaxy = True
                break
        if not hasGalaxy:
            newGrid.append(row)
            newGrid.append(row)
        else:
            newGrid.append(row)
    # find cols that have no galaxy
    grid = copy.deepcopy(newGrid)
    print()
    print("horizontal grid")
    print_2d_grid(grid)
    colIds = []
    for i in range(len(grid[0])):
        hasGalaxy = False
        for j in range(len(grid)):
            char = grid[j][i]
            if char == "#":
                hasGalaxy = True
                break
        if not hasGalaxy:
            colIds.append(i)
    print(colIds)
    newGrid = []
    for row in grid:
        newRow = []
        for i in range(len(grid[0])):
            newRow.append(row[i])
            if i in colIds:
                newRow.append(row[i])
            for c in colIds:
                c += 1
        newGrid.append(newRow)
    grid = copy.deepcopy(newGrid)
    print()
    print("veritcal grid")
    print_2d_grid(grid)

    # find all the galaxies and number them
    galaxies = {}
    gid = 1
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            char = grid[j][i]
            if char == "#":
                galaxies[gid] = (i, j)
                gid += 1
    print(galaxies)

    # get all pairs
    pairs = [(a, b) for idx, a in enumerate(list(galaxies.keys())) for b in list(galaxies.keys())[idx + 1:]]

    answer = 0
    for (a, b) in pairs:
        # find the min path between two galaxies
        dist = manhattan_distance(np.array(galaxies[a]), np.array(galaxies[b]))

        answer += dist
    print(answer)

# TODO:...
#  smarter way is to not manipulate the grid, just take the coordinates of the galaxies,
#  check what rows/cols to expand, and increase their coordinate values accordingly
def part2():
    grid = parseInput(11)
    print_2d_grid(grid)

    expandSize = 1000000-1

    # find rows that have no galaxy
    rowsNoGalaxy = []
    for j in range(len(grid)):
        hasGalaxy = False
        row = grid[j]
        for i in range(len(row)):
            char = row[i]
            if char == "#":
                hasGalaxy = True
                break
        if not hasGalaxy:
            rowsNoGalaxy.append(j)

    # find cols that have no galaxy
    colsNoGalaxy = []
    for i in range(len(grid[0])):
        hasGalaxy = False
        for j in range(len(grid)):
            char = grid[j][i]
            if char == "#":
                hasGalaxy = True
                break
        if not hasGalaxy:
            colsNoGalaxy.append(i)

    print(rowsNoGalaxy, colsNoGalaxy)

    # find all the galaxies and number them
    galaxies = {}
    gid = 1
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            char = grid[j][i]
            if char == "#":
                galaxies[gid] = (i, j)
                gid += 1
    print(galaxies)

    origGalaxies = copy.deepcopy(galaxies)
    # expand the universe
    # find any galaxies with a higher index, and add by expandSize
    for rowId in rowsNoGalaxy:
        for galaxyId in galaxies:
            x, y = origGalaxies[galaxyId]
            x2, y2 = galaxies[galaxyId]
            if y > rowId:
                galaxies[galaxyId] = (x2, y2 + expandSize)
    print(galaxies)
    for colId in colsNoGalaxy:
        for galaxyId in galaxies:
            x, y = origGalaxies[galaxyId]
            x2, y2 = galaxies[galaxyId]
            if x > colId:
                galaxies[galaxyId] = (x2 + expandSize, y2)
    print(galaxies)

    # print galaxies in 2d grid
    # maxX = 0
    # maxY = 0
    # for galaxyId in galaxies:
    #     x, y = galaxies[galaxyId]
    #     if x > maxX:
    #         maxX = x
    #     if y > maxY:
    #         maxY = y
    # print(maxX, maxY)
    # grid = []
    # for j in range(maxY+1):
    #     row = []
    #     for i in range(maxX+1):
    #         if (i, j) in galaxies.values():
    #             row.append("#")
    #         else:
    #             row.append(".")
    #     grid.append(row)
    
    # print_2d_grid(grid)

    # get all pairs
    pairs = [(a, b) for idx, a in enumerate(list(galaxies.keys())) for b in list(galaxies.keys())[idx + 1:]]

    answer = 0
    for (a, b) in pairs:
        # find the min path between two galaxies
        dist = manhattan_distance(np.array(galaxies[a]), np.array(galaxies[b]))

        answer += dist
    print(answer)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
