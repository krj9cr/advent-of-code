import copy
import time
from collections import deque
import numpy as np

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
    h = len(grid)
    w = len(grid[0])
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

def dotNextSteps(x, y, grid):
    h = len(grid)
    w = len(grid[0])
    steps = []
    # left
    nx, ny = x - 1, y
    # if 0 <= nx < w and 0 <= ny < h:
    nextChar = grid[ny][nx]
    if nextChar != "X":
        steps.append(tuple([nx, ny]))
    # right
    nx, ny = x + 1, y
    # if 0 <= nx < w and 0 <= ny < h:
    nextChar = grid[ny][nx]
    if nextChar != "X":
        steps.append(tuple([nx, ny]))
    # up
    nx, ny = x, y - 1
    # if 0 <= nx < w and 0 <= ny < h:
    nextChar = grid[ny][nx]
    if nextChar != "X":
        steps.append(tuple([nx, ny]))
    # down
    nx, ny = x, y + 1
    # if 0 <= nx < w and 0 <= ny < h:
    nextChar = grid[ny][nx]
    if nextChar != "X":
        steps.append(tuple([nx, ny]))
    return steps

seen = set()

def part1():
    grid = parseInput(10)
    h = len(grid)
    w = len(grid[0])
    print(grid)
    startPos = getStart(grid)
    print(startPos)
    totalSteps = {}
    totalSteps[startPos] = 0
    # print(longestPath(startPos[0], startPos[1], grid, 0))
    # print(getNextSteps(3, 3, grid))
    queue = deque([[startPos]])
    seen = {startPos}
    maxSteps = 0
    steps = 0
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        nextSteps = getNextSteps(x, y, grid)
        print("at", x, y)
        print("next steps:", nextSteps)
        if len(nextSteps) == 0:
            print(path)
            break
        for nextStep in nextSteps:
            print(nextStep)
            if nextStep not in seen:
                queue.append(path + [nextStep])
                seen.add(nextStep)
                totalSteps[nextStep] = len(path)
    print(totalSteps)

    # find max totalSteps
    maxSteps = 0
    for pos in totalSteps:
        if totalSteps[pos] > maxSteps:
            maxSteps = totalSteps[pos]
    print(maxSteps)

def part2():
    grid = parseInput(10)
    origGrid = copy.deepcopy(grid)
    h = len(grid)
    w = len(grid[0])
    print(grid)

    # find the path first like in part 1... so that we can mark junk pieces as dots I guess
    startPos = getStart(grid)
    print(startPos)
    totalSteps = {}
    totalSteps[startPos] = 0
    queue = deque([[startPos]])
    seen = {startPos}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        nextSteps = getNextSteps(x, y, grid)
        # print("at", x, y)
        # print("next steps:", nextSteps)
        if len(nextSteps) == 0:
            # print(path)
            break
        for nextStep in nextSteps:
            # print(nextStep)
            if nextStep not in seen:
                queue.append(path + [nextStep])
                seen.add(nextStep)
                totalSteps[nextStep] = len(path)
    print(totalSteps)

    # create a grid of totalSteps...?
    for pos in totalSteps:
        grid[pos[1]][pos[0]] = "X"
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))
    print()

    # get coordinates of junk pieces, and mark in origGrid
    junk = []
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            char = row[i]
            if char != "X":
                junk.append(tuple([i, j]))
                origGrid[j][i] = "."

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in origGrid]))
    print()

    # space out grid to handle squeezing???
    spacedGrid = []
    for j in range(len(origGrid)):
        row = origGrid[j]
        newRow = []
        # add horizontal spacing
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

    print("spacedGrid")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid]))
    print()

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


    print("spacedGrid2")
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid2]))
    print()



    spacedGrid = spacedGrid2
    h = len(spacedGrid)
    w = len(spacedGrid[0])

    origSpacedGrid = copy.deepcopy(spacedGrid)

    # find main loop again
    startPos = getStart(spacedGrid)
    print(startPos)
    totalSteps = {}
    totalSteps[startPos] = 0
    queue = deque([[startPos]])
    seen = {startPos}
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        nextSteps = getNextSteps(x, y, spacedGrid)
        # print("at", x, y)
        # print("next steps:", nextSteps)
        if len(nextSteps) == 0:
            # print(path)
            break
        for nextStep in nextSteps:
            # print(nextStep)
            if nextStep not in seen:
                queue.append(path + [nextStep])
                seen.add(nextStep)
                totalSteps[nextStep] = len(path)
    print(totalSteps)

    # create a grid of totalSteps...?
    for pos in totalSteps:
        spacedGrid[pos[1]][pos[0]] = "X"
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in spacedGrid]))

    # see if there's a way out for each "."
    grid2 = copy.deepcopy(spacedGrid)
    for j in range(len(grid2)):
        row = grid2[j]
        for i in range(len(row)):
            char = row[i]
            if char == ".":
                # check if the dot is contained
                startPos = (i, j)
                queue = deque([[startPos]])
                seen = {startPos}
                wayOut = False
                while queue:
                    if wayOut:
                        break
                    path = queue.popleft()
                    x, y = path[-1]
                    # if x < 0 or x >= w or y < 0 or y >= h:
                    #     wayOut = True
                    #     break
                    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                        if 0 <= x2 < w and 0 <= y2 < h:
                            next = (x2, y2)
                            nextItem = spacedGrid[y2][x2]
                            if next not in seen and nextItem != "X":
                                queue.append(path + [next])
                                seen.add(next)
                        else:
                            wayOut = True
                            if startPos == (20, 8):
                                print("x2, y2", x2, y2)
                                print("PATH", path)
                            break
                # print(totalSteps)
                if not wayOut:
                    if grid2[j][i] == ".":
                        grid2[j][i] = "I"
                if wayOut:
                    if grid2[j][i] == ".":
                        grid2[j][i] = "O"

    # replace X's with original grid
    for j in range(len(grid2)):
        row = grid2[j]
        for i in range(len(row)):
            char = row[i]
            if char == "X":
                grid2[j][i] = origSpacedGrid[j][i]
    print()
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid2]))

    # then just count the number of dots?
    answer = 0
    for j in range(len(grid2)):
        row = grid2[j]
        for i in range(len(row)):
            char = row[i]
            if char == "I":
                answer += 1
    print(answer)

# 547 too high
# 530 too high

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
