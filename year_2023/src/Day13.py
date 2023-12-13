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

# 22376 too low
        

def part2():
    lines = parseInput(13)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
