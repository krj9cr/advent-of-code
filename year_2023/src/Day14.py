import copy
import time
import numpy as np

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        grid = []
        for line in file:
            line = line.strip()
            grid.append([char for char in line])
        return grid

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def roll(grid):
    for j in range(len(grid)):
        row = grid[j]
        # print("row", row)
        newRow = copy.deepcopy(row)
        # go backwards to find O's
        for i in range(len(row)-1, -1, -1):
            char = row[i]
            moved = False
            if char == "O":
                # roll it forward until it hits the end, another O, or #
                # print(i)
                for i2 in range(i+1, len(row)):
                    char2 = row[i2]
                    if char2 == "O" or char2 == "#":
                        row[i2-1] = "O"
                        if i2-1 != i:
                            row[i] = "."
                        # print("moved", i, "to", i2-1, row)
                        moved = True
                        break
                # we walked off the edge
                if not moved:
                    row[len(row)-1] = "O"
                    if len(row)-1 != i:
                        row[i] = "."
                    # print("moved", i, "to", len(row)-1, row)

def cycle(grid):
    northGrid = np.rot90(grid, k=3)
    roll(northGrid)
    westGrid = np.rot90(northGrid, k=3)
    roll(westGrid)
    southGrid = np.rot90(westGrid, k=3)
    roll(southGrid)
    eastGrid = np.rot90(southGrid, k=3)
    roll(eastGrid)
    # print_2d_grid(eastGrid)
    return eastGrid

def part1():
    grid = parseInput(14)
    # print_2d_grid(grid)
    # rotate grid, so we can just slide everything right
    rotatedGrid = np.rot90(grid, k=3)
    print_2d_grid(rotatedGrid)
    roll(rotatedGrid)
    print()
    print_2d_grid(rotatedGrid)

    # calculate load
    answer = 0
    for j in range(len(rotatedGrid)):
        row = rotatedGrid[j]
        for i in range(len(row)):
            char = row[i]
            if char == "O":
                answer += i + 1
    print(answer)

def gridToString(grid):
    return "".join(["".join(row) for row in grid])


def part2():
    grid = parseInput(14)
    origGrid = copy.deepcopy(grid)

    seen = {}

    for i in range(3):
        # print(i)
        grid = cycle(grid)
        gridHash = gridToString(grid)
        if seen.get(gridHash) is not None:
            print(i, "SEEN", seen[gridHash])
        else:
            seen[gridHash] = i

    cycle_start = 137
    # starts at 93
    cycle_length = 43
    cycle_end = 1000000000
    cycle_num = (cycle_end - cycle_start) % cycle_length
    print("cycle_num", cycle_num)

    # get the grid for 4
    for i in range(93 + 33):
        print(i)
        origGrid = cycle(origGrid)
    print_2d_grid(origGrid)

    # calculate load, after rotating, since we rely on it being rotated
    origGrid = np.rot90(origGrid, k=3)
    answer = 0
    for j in range(len(origGrid)):
        row = origGrid[j]
        for i in range(len(row)):
            char = row[i]
            if char == "O":
                answer += i + 1
    print(answer)

# 101029 too high

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
