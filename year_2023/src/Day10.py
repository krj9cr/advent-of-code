import time
from collections import deque

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [[char for char in line.strip()] for line in file]
        return lines

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

seen = set()
totalSteps = {}

def longestPath(x, y, grid, steps):
    nextSteps = getNextSteps(x, y, grid)
    if len(nextSteps) == 0:
        return steps
    maxSteps = steps
    print("at: ", x, y)
    takeNextSteps = []
    for nextStep in nextSteps:
        if nextStep not in totalSteps:
            totalSteps[nextStep] = steps + 1
            takeNextSteps.append(nextStep)
    for nextStep in takeNextSteps:
        print("next step", nextStep)
        print("seen", totalSteps)
        l = longestPath(nextStep[0], nextStep[1], grid, steps + 1)
        if l > maxSteps:
            maxSteps = l
    return maxSteps

def part1():
    grid = parseInput(10)
    h = len(grid)
    w = len(grid[0])
    print(grid)
    startPos = getStart(grid)
    print(startPos)
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
    lines = parseInput(10)
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
