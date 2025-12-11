import copy
import itertools
import time, os

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append([item for item in line])
        return lines

def checkNeighborRolls(x, y, grid):
    neighbors = set()
    for x2, y2 in ((x, y - 1), (x - 1, y), (x - 1, y + 1), (x-1,y-1), (x + 1, y), (x+1,y-1), (x+1,y+1), (x, y + 1)):
        if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
            if grid[y2][x2] == '@':
                neighbors.add((x2, y2))
    return neighbors

def part1():
    lines = parseInput()
    # print(lines)
    allRolls = set()
    for j in range(len(lines)):
        row = lines[j]
        for i in range(len(row)):
            item = row[i]
            if item == '@':
                # print(i,j)
                neighbors = checkNeighborRolls(i, j, lines)
                # print(neighbors)
                if len(neighbors) < 4:
                    # print("adding to all")
                    allRolls.add((i, j))
                    # print("all:", allRolls)
    # print("all:", allRolls)
    print(len(allRolls))

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()


def part2():
    lines = parseInput()
    # print(lines)
    grid = copy.deepcopy(lines)

    turn = 0
    totalRollsRemoved = 0
    while True:
        # print(turn)
        # print_2d_grid(grid)

        # find what we can remove
        allRolls = set()
        for j in range(len(grid)):
            row = grid[j]
            for i in range(len(row)):
                item = row[i]
                if item == '@':
                    # print(i,j)
                    neighbors = checkNeighborRolls(i, j, grid)
                    # print(neighbors)
                    if len(neighbors) < 4:
                        # print("adding to all")
                        allRolls.add((i, j))
                        # print("all:", allRolls)
        # print("all:", allRolls)
        # print(len(allRolls))
        if len(allRolls) == 0:
            break
        else:
            # remove all the rolls from the grid
            newGrid = copy.deepcopy(grid)
            for (x, y) in allRolls:
                newGrid[y][x] = '.'
            grid = newGrid
            totalRollsRemoved += len(allRolls)
            # print("removed", len(allRolls), "total", totalRollsRemoved)
        # TODO: temporary
        # if turn > 5:
        #     break
        turn += 1
    print("total", totalRollsRemoved)

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
