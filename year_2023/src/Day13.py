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

def find_horizontal_mirrors(grid):
    value = None
    for j in range(len(grid)-1):
        row1 = grid[j]
        row2 = grid[j+1]
        if (row1 == row2).all():
            print("horitzontal mirror at:", j, j +1)
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
                print("comparing", upper, lower)
                print(row1)
                print(row2)
                if (row1 == row2).all():
                    print("equal")
                else:
                    mirrored = False
                    print("not equal")
                    break
            if mirrored:
                value = j + 1
                break
    return value

# check if there's exactly one difference between 2 rows, and return its index and which row has the "."
def compare_rows_smudge(row1, row2):
    diff = 0
    diffIdx = None
    whichRow = None
    for i in range(len(row1)):
        char1 = row1[i]
        char2 = row2[i]
        if char1 != char2:
            diff += 1
            diffIdx = i
            if char1 == ".":
                whichRow = 1
            else:
                whichRow = 2
    if diff == 1:
        return diffIdx, whichRow
    return None

def find_smudge(grid):
    value = None
    for j in range(len(grid)-1):
        row1 = grid[j]
        row2 = grid[j+1]
        # TODO: need to check if different by 1 here, too
        if (row1 == row2).all():
            print("horitzontal mirror at:", j, j +1)
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
                print("comparing", upper, lower)
                print(row1)
                print(row2)
                if (row1 == row2).all():
                    print("equal")
                else:
                    # check if rows are different by one
                    # try making a new grid and run "part1" again on it to see if we get a different value than we have in "part1Answers"
                    mirrored = False
                    print("not equal")
                    break
            if mirrored:
                value = j + 1
                break
    return value

def part1():
    grids = parseInput(13)
    for grid in grids:
        print_2d_grid(grid)
        print()

    answer = 0
    for grid in grids:
        value = None
        print_2d_grid(grid)
        print("finding vertical mirrors")
        rotatedGrid = np.rot90(grid, k=3, axes=(0,1))
        print("rotated")
        print_2d_grid(rotatedGrid)
        value = find_horizontal_mirrors(rotatedGrid)
        print("vertical mirror at:", value)

        if not value:
            print("finding horizontal mirrors")
            print_2d_grid(grid)
            value = find_horizontal_mirrors(grid) * 100
            print("horiztonal mirror at:", value)
        print()
        answer += value
    print(answer)
        

def part2():
    grids = parseInput(13)
    for grid in grids:
        print_2d_grid(grid)
        print()

    # run pt 1 and save answers in a dict so we make sure to get a different answer
    part1Answers = {}
    for gid in range(len(grids)):
        grid = grids[gid]
        value = None
        print_2d_grid(grid)
        print("finding vertical mirrors")
        rotatedGrid = np.rot90(grid, k=3, axes=(0,1))
        print("rotated")
        print_2d_grid(rotatedGrid)
        value = find_horizontal_mirrors(rotatedGrid)
        print("vertical mirror at:", value)

        if not value:
            print("finding horizontal mirrors")
            print_2d_grid(grid)
            value = find_horizontal_mirrors(grid) * 100
            print("horiztonal mirror at:", value)
        print()
        part1Answers[gid] = value
    print(part1Answers)

    # for each grid
    for gid in range(len(grids)):
        grid = grids[gid]
        print_2d_grid(grid)
        # find each dot
        for j in range(len(grid)):
            row = grid[j]
            for i in range(len(row)):
                char = row[i]
                if char == ".":
                    print(i,j)
                    # try changing each dot, and see if changing it still matches another line
                    # if it does match another line, run "find_horizontal_mirrors" with that grid, check that it's a different answer from "part1Answers"
        print()


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
