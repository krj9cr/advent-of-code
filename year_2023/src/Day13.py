import copy
import time
import numpy as np

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        grids = []
        currGrid = []
        for line in file:
            line = line.strip()
            if line == "":
                grids.append(np.array(currGrid))
                currGrid = []
            else:
                currGrid.append([char for char in line])
        
        if currGrid != []:
            grids.append(np.array(currGrid))
        return grids

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def find_mirror_value(grid, vertical=True, notValue=None):
    values = set()
    for j in range(len(grid)-1):
        row1 = grid[j]
        row2 = grid[j+1]
        if (row1 == row2).all():
            # if vertical:
            #     print("vertical ", end="")
            # else:
            #     print("horizonal ", end="")
            # print("mirror at:", j, j +1)
            # print_2d_grid(grid)
            # check all the other pairs
            upper = j
            lower = j + 1
            mirrored = True
            while True:
                upper -= 1
                lower += 1
                if upper < 0 or lower >= len(grid):
                    break
                row1 = grid[upper]
                row2 = grid[lower]
                # print("comparing", upper, lower)
                # print(row1)
                # print(row2)
                if (row1 == row2).all():
                    # print("equal")
                    True  # do nothing
                else:
                    mirrored = False
                    # print("not equal")
                    break
            if mirrored:
                # if value and value != notValue:
                #     print("found another value", end="")
                value = j + 1
                if not vertical:
                    value *= 100
                # print(value)
                values.add(value)

    return values

def find_mirror(grid, notValue=None):
    # print_2d_grid(grid)
    # print("finding horizontal mirrors")
    # print_2d_grid(grid)
    values = find_mirror_value(grid, vertical=False)
    # print("horiztonal mirror at:", value)

    # if not value or (notValue and value == notValue):
    # print("finding vertical mirrors")
    rotatedGrid = np.rot90(grid, k=3, axes=(0, 1))
    # print("rotated")
    # print_2d_grid(rotatedGrid)
    values2 = find_mirror_value(rotatedGrid, vertical=True)

    values = values.union(values2)
    # print(values)
    return values

def part1():
    grids = parseInput(13)
    # for grid in grids:
    #     print_2d_grid(grid)
    #     print()

    answer = 0
    for grid in grids:
        value = find_mirror(grid).pop()
        answer += value
    print(answer)
        

def part2():
    grids = parseInput(13)
    answer = 0

    # run pt 1 and save answers in a dict, so we make sure to get a different answer
    part1Answers = {}
    for gid in range(len(grids)):
        grid = grids[gid]
        value = find_mirror(grid).pop()
        part1Answers[gid] = value
    # print(part1Answers)

    # for each grid
    for gid in range(len(grids)):
        grid = grids[gid]
        gridValue = part1Answers[gid]
        # rotatedGrid = np.rot90(grid, k=3, axes=(0, 1))
        # print_2d_grid(grid)
        foundAnswer = False
        # for each position
        for j in range(len(grid)):
            row = grid[j]
            for i in range(len(row)):
                # print(i, j)
                char = row[i]
                if char == ".":
                    newChar = "#"
                else:
                    newChar = "."

                # run "find_horizontal_mirrors" with that grid
                newGrid = copy.deepcopy(grid)
                newGrid[j][i] = newChar
                # print_2d_grid(newGrid)

                # check that it's a different answer from "part1Answers"
                values = find_mirror(newGrid, notValue=gridValue)
                try:
                    values.remove(gridValue)
                except:
                    True  # do nothing
                if len(values) > 1:
                    print("found multiple answers")
                elif len(values) > 0:
                    value = values.pop()
                    # print_2d_grid(grid)
                    # print("prev answer", gridValue, "found answer", value, "changing", i, j, "to", newChar)
                    answer += value
                    foundAnswer = True
                    break
            if foundAnswer:
                break
        # print()
    print(answer)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
