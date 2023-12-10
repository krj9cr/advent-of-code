import copy
import time
from collections import deque

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [[char for char in line.strip()] for line in file]
        return lines

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def getStart(grid):
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            char = row[i]
            if char == "S":
                return i, j

def getNextSteps(x, y, grid):
    # h = len(grid)
    # w = len(grid[0])
    char = grid[y][x]
    steps = []
    if char == "S":
        # left
        nx, ny = x - 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "L" or nextChar == "F":
            steps.append(tuple([nx, ny]))
        # right
        nx, ny = x + 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "7" or nextChar == "J":
            steps.append(tuple([nx, ny]))
        # up
        nx, ny = x, y - 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "7" or nextChar == "F":
            steps.append(tuple([nx, ny]))
        # down
        nx, ny = x, y + 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "L" or nextChar == "J":
            steps.append(tuple([nx, ny]))
    elif char == "|":
        # up
        nx, ny = x, y - 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "7" or nextChar == "F":
            steps.append(tuple([nx, ny]))
        # down
        nx, ny = x, y + 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "L" or nextChar == "J":
            steps.append(tuple([nx, ny]))
    elif char == "-":
        # left
        nx, ny = x - 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "L" or nextChar == "F":
            steps.append(tuple([nx, ny]))
        # right
        nx, ny = x + 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "7" or nextChar == "J":
            steps.append(tuple([nx, ny]))
    elif char == "L":
        # right
        nx, ny = x + 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "7" or nextChar == "J":
            steps.append(tuple([nx, ny]))
        # up
        nx, ny = x, y - 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "7" or nextChar == "F":
            steps.append(tuple([nx, ny]))
    elif char == "J":
        # left
        nx, ny = x - 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "L" or nextChar == "F":
            steps.append(tuple([nx, ny]))
        # up
        nx, ny = x, y - 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "7" or nextChar == "F":
            steps.append(tuple([nx, ny]))
    elif char == "7":
        # left
        nx, ny = x - 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "L" or nextChar == "F":
            steps.append(tuple([nx, ny]))
        # down
        nx, ny = x, y + 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "L" or nextChar == "J":
            steps.append(tuple([nx, ny]))
    elif char == "F":
        # right
        nx, ny = x + 1, y
        nextChar = grid[ny][nx]
        if nextChar == "-" or nextChar == "7" or nextChar == "J":
            steps.append(tuple([nx, ny]))
        # down
        nx, ny = x, y + 1
        nextChar = grid[ny][nx]
        if nextChar == "|" or nextChar == "L" or nextChar == "J":
            steps.append(tuple([nx, ny]))
    return steps

def findPipePath(grid):
    startPos = getStart(grid)
    # print(startPos)
    totalSteps = {startPos: 0}
    maxSteps = 0
    queue = deque([[startPos]])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        nextSteps = getNextSteps(x, y, grid)
        # print("at", x, y)
        # print("next steps:", nextSteps)
        for nextStep in nextSteps:
            # print(nextStep)
            if nextStep not in totalSteps:
                queue.append(path + [nextStep])
                steps = len(path)
                totalSteps[nextStep] = steps
                # find max totalSteps
                if steps > maxSteps:
                    maxSteps = steps
    return totalSteps, maxSteps

def part1():
    grid = parseInput(10)
    totalSteps, maxSteps = findPipePath(grid)

    print(maxSteps)

# TODO: the way we're copying grids is probably inefficient, but nice for visualization
def part2():
    grid = parseInput(10)
    origGrid = copy.deepcopy(grid)
    # print(grid)

    # find the path first like in part 1... so that we can mark junk pieces as dots I guess
    totalSteps, _ = findPipePath(grid)

    # mark the path in the grid
    for pos in totalSteps:
        grid[pos[1]][pos[0]] = "X"
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    # print()

    # get coordinates of junk pieces, and mark in origGrid
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            char = row[i]
            if char != "X":
                origGrid[j][i] = "."
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in origGrid]))
    # print()

    # space out grid to handle squeezing???
    # add horizontal spacing
    spacedGrid = []
    for j in range(len(origGrid)):
        row = origGrid[j]
        newRow = []
        for i in range(len(row)-1):
            char = row[i]
            nextChar = row[i+1]
            if char == ".":
                newRow.append(".")
                newRow.append("#")
            elif char == "S":
                newRow.append("S")
                if nextChar == "-" or nextChar == "J" or nextChar == "7":
                    newRow.append("-")
                else:
                    newRow.append("#")
            elif (char == "|" or char == "J" or char == "7") \
                    and nextChar == "|" or nextChar == "L" or nextChar == "F" or nextChar == ".":
                newRow.append(char)
                newRow.append("#")
            elif (char == "-" or char == "L" or char == "F") \
                    and (nextChar == "-" or nextChar == "J" or nextChar == "7" or nextChar == "S"):
                newRow.append(char)
                newRow.append("-")
            else:
                newRow.append(char)
                newRow.append("#")
        newRow.append(row[-1])
        spacedGrid.append(newRow)
    # print("spacedGrid")
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid]))
    # print()

    # add vertical spacing
    spacedGrid2 = []
    for j in range(len(spacedGrid)-1):
        row = spacedGrid[j]
        nextRow = spacedGrid[j+1]
        newRow = []
        for i in range(len(row)):
            char = row[i]
            nextChar = nextRow[i]
            if char == "." or char == "#":
                newRow.append("#")
            elif char == "S":
                if nextChar == "|" or nextChar == "L" or nextChar == "J":
                    newRow.append("|")
                else:
                    newRow.append("#")
            elif char == "-" or char == "L" or char == "J":
                newRow.append("#")
            elif char == "|" or char == "F" or char == "7":
                newRow.append("|")
            else:
                newRow.append("#")
        spacedGrid2.append(row)
        spacedGrid2.append(newRow)
    spacedGrid2.append(spacedGrid[-1])
    # print("spacedGrid2")
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid2]))
    # print()

    spacedGrid = spacedGrid2
    h = len(spacedGrid)
    w = len(spacedGrid[0])

    # find main loop again, which is bigger, now
    totalSteps, _ = findPipePath(spacedGrid)

    # mark the grid with the main loop
    for pos in totalSteps:
        spacedGrid[pos[1]][pos[0]] = "X"
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid]))

    # see if there's a way out for each "."
    answer = 0
    seenWayOut = set()
    seenNoWayOut = set()
    for j in range(len(spacedGrid)):
        row = spacedGrid[j]
        for i in range(len(row)):
            char = row[i]
            if char == ".":
                # check if the dot is contained
                startPos = (i, j)
                queue = deque([[startPos]])
                seen = {startPos}
                wayOut = False

                # short  circuit if we've seen this point already
                if (i, j) in seenNoWayOut:
                    spacedGrid[j][i] = "I"
                    answer += 1
                    continue
                if (i, j) in seenWayOut:
                    spacedGrid[j][i] = "O"
                    continue

                # do bfs
                while queue:
                    if wayOut:
                        break
                    path = queue.popleft()
                    x, y = path[-1]
                    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                        if 0 <= x2 < w and 0 <= y2 < h:
                            next = (x2, y2)
                            nextItem = spacedGrid[y2][x2]
                            if next not in seen and nextItem != "X":
                                queue.append(path + [next])
                                seen.add(next)
                        # if we go out of bounds, that means there's a way out
                        else:
                            wayOut = True
                            break
                if not wayOut:
                    for s in seen:
                        seenNoWayOut.add(s)
                    spacedGrid[j][i] = "I"
                    answer += 1
                if wayOut:
                    for s in seen:
                        seenWayOut.add(s)
                    spacedGrid[j][i] = "O"

    # replace X's with original grid (for debugging)
    # for j in range(len(spacedGrid)):
    #     row = spacedGrid[j]
    #     for i in range(len(row)):
    #         char = row[i]
    #         if char == "X":
    #             spacedGrid[j][i] = origSpacedGrid[j][i]
    # print()
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid]))

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
