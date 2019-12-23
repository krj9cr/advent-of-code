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
                    keys[char] = (x,y)
                else:
                    doors[char] = (x,y)
    return keys, doors, start

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def isDoor(char):
    if char != wallChar and char != emptyChar and char != startChar and char.isupper():
        return True
    else:
        return False

def bfs(grid, start, end):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                if grid[y2][x2] != wallChar:
                    if (x2, y2) not in seen:
                        queue.append(path + [(x2,y2)])
                        seen.add((x2,y2))

def computeDistances(grid, keys, start, acquiredKeys):
    distToObjects = {}
    for key in keys:
        if key not in acquiredKeys:
            distToObjects[key] = bfs(grid, start, keys[key])
    # for door in doors:
    #     distToObjects[door] = bfs(grid, start, doors[door])
    # print(distToObjects)

    return distToObjects

def allKeys(keys, acquiredKeys):
    for key in keys:
        if key not in acquiredKeys:
            return False
    return True

###########################
# part1
###########################
def part1(grid):
    printGrid(grid)
    keys, doors, start = findKeysAndDoors(grid)
    print("start", start)
    print("keys", keys)
    print("doors", doors)
    steps = 0
    currLoc = start
    acquiredKeys = set()


    distToObjects = computeDistances(grid, keys, currLoc, acquiredKeys)
    blockages = {}
    for object in distToObjects:
        path = distToObjects[object]
        for coord in path:
            for door in doors:
                if coord == doors[door] and object != door:
                    if object in blockages:
                        blockages[object].add(door)
                    else:
                        blockages[object] = set(door)

    print("distances",distToObjects)
    print("blockages", blockages)

    while not allKeys(keys, acquiredKeys):
        distToObjects = computeDistances(grid, keys, currLoc, acquiredKeys)

        # move to closest key, or next alphabetically?
        l = sorted(distToObjects.items(), key=lambda item: item)
        l = sorted(l, key=lambda item: len(item[1]))
        for key, path in l:
            if key not in blockages or blockages[key] is None:
                print("moving towards",key)
                currLoc = path[-1]
                steps += len(path) - 1
                acquiredKeys.add(key)
                distToObjects.pop(key)
                break

        # revist any keys blocked by the one we just got
        for key in blockages.keys():
            doors = blockages[key]
            if doors is not None:
                for door in doors:
                    if door.lower() in acquiredKeys:
                        doors.remove(door)
                        if len(doors) == 0:
                            blockages[key] = None
                        break

        print("actuired keys", acquiredKeys)
        print("distances",distToObjects)
        print("blockages", blockages)
    print("steps",steps)

# 5206 too high


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
