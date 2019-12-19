from collections import deque

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return [char for char in line.strip()]

startChar = "@"
emptyChar = "."
wallChar = "#"

def findKeysAndDoors(grid):
    keys = {}
    doors = {}
    start = None
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            char = grid[y][x]
            if char == startChar:
                start = (x,y)
            if char != wallChar and char != emptyChar and char != startChar:
                if char.islower():
                    keys[(x,y)] = char
                else:
                    doors[(x,y)] = char
    return keys, doors, start

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def bfs(grid, start, end):
    queue = deque([[startChar]])
    seen = set([startChar])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                if grid[(x2,y2)] != wallChar:
                    if (x2, y2) not in seen:
                        queue.append(path + [(x2,y2)])
                        seen.add((x2,y2))

###########################
# part1
###########################
def part1(grid):
    printGrid(grid)
    keys, doors, start = findKeysAndDoors(grid)
    print("start", start)
    print("keys", keys)
    print("doors", doors)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()


    # print("\nPART 2 RESULT")
    # runpart2()
