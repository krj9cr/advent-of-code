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
    char = grid[y][x]
    steps = []
    # wayOut = False
    # if char != "X":
    # left
    nx, ny = x - 1, y
    if 0 <= nx < w and 0 <= ny < h:
        nextChar = grid[ny][nx]
        # if nextChar == "-" or nextChar == "L" or nextChar == "F":
        #     return None
        if nextChar != "X":
            steps.append(tuple([nx, ny]))
    else:
        return None
    # right
    nx, ny = x + 1, y
    if 0 <= nx < w and 0 <= ny < h:
        nextChar = grid[ny][nx]
        # if nextChar == "-" or nextChar == "7" or nextChar == "J":
        #     return None
        if nextChar != "X":
            steps.append(tuple([nx, ny]))
    else:
        return None
    # up
    nx, ny = x, y - 1
    if 0 <= nx < w and 0 <= ny < h:
        nextChar = grid[ny][nx]
        # if nextChar == "|" or nextChar == "7" or nextChar == "F":
        #     return None
        if nextChar != "X":
            steps.append(tuple([nx, ny]))
    else:
        return None
    # down
    nx, ny = x, y + 1
    if 0 <= nx < w and 0 <= ny < h:
        nextChar = grid[ny][nx]
        # if nextChar == "|" or nextChar == "L" or nextChar == "J":
        #     return None
        if nextChar != "X":
            steps.append(tuple([nx, ny]))
    else:
        return None
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
    # maxSteps = 0
    # end = None
    # for pos in totalSteps:
    #     if totalSteps[pos] > maxSteps:
    #         maxSteps = totalSteps[pos]
    #         end = pos
    # print(maxSteps, end)

    # create a grid of totalSteps...?
    for pos in totalSteps:
        # if totalSteps[pos] != 0:
        grid[pos[1]][pos[0]] = "X"
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid]))

    grid2 = copy.deepcopy(grid)
    # find all dots
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            char = row[i]
            if char != "X":
                # check if the dot is contained
                startPos = (i, j)
                print("START", startPos)
                totalSteps = {}
                totalSteps[startPos] = 0
                queue = deque([[startPos]])
                seen = {startPos}
                maxSteps = 0
                steps = 0
                wayOut = False
                while queue:
                    path = queue.popleft()
                    x, y = path[-1]
                    nextSteps = dotNextSteps(x, y, grid)
                    # print("at", x, y)
                    # print("next steps:", nextSteps)
                    if nextSteps is None:  # this means it's not in a loop, or next to an edge
                        # for p in path:
                        #     del totalSteps[p]
                        wayOut = True
                        break
                    if len(nextSteps) == 0:
                        break
                    for nextStep in nextSteps:
                        print(nextStep)
                        if nextStep not in seen:
                            queue.append(path + [nextStep])
                            seen.add(nextStep)
                            totalSteps[nextStep] = len(path)
                print(totalSteps)
                if not wayOut:
                    # create a grid of totalSteps...?
                    for pos in totalSteps:
                        # if totalSteps[pos] != 0:
                        grid2[pos[1]][pos[0]] = "I"
                if wayOut:
                    # create a grid of totalSteps...?
                    for pos in totalSteps:
                        # if totalSteps[pos] != 0:
                        grid2[pos[1]][pos[0]] = "O"

    # np.set_printoptions(precision=2)
    # print(np.array(grid2))
    # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid2]))
    # print(contained)
    # then just count the number of dots?
    answer = 0
    for j in range(len(grid2)):
        row = grid2[j]
        for i in range(len(row)):
            char = row[i]
            if char == "I":
                answer += 1
    print(answer)

    # replace X's with original grid
    for j in range(len(grid2)):
        row = grid2[j]
        for i in range(len(row)):
            char = row[i]
            if char == "X":
                grid2[j][i] = origGrid[j][i]
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in grid2]))

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
