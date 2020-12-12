from lib.search import bfs_2d_grid
from lib.print import print_2d_grid

# keys and doors map
# part2 in fewest steps

###########################
# helpers
###########################
def parseInputFile(name):
    with open((__file__.rstrip("code.py") + name), 'r') as file:
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

def findKeysAndDoorsAndStarts(grid):
    keys = {}
    doors = {}
    starts = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            char = grid[y][x]
            if char == startChar:
                starts.append((x,y))
                continue
            if char != wallChar and char != emptyChar and char != startChar:
                if char.islower():
                    keys[char] = (x,y)
                else:
                    doors[char] = (x,y)
    return keys, doors, starts

###########################
# part1
###########################
def part1(grid):
    print_2d_grid(grid)
    keys, doors, start = findKeysAndDoors(grid)
    keys["start"] = start
    print("start", start)
    print("keys", keys)
    print("doors", doors)

    # manually inspected the map and figured this out...
    key_order =['g','r','j', 'd', 'y', 'a', 'u', 'k', 'b', 'h','c', 'i', 'v', 'p', 'o', 't', 'e', 'z', 'w', 'q', 'x', 'f', 's', 'm', 'l', 'n']

    currKey = "start"
    steps = 0
    print('testing path', key_order, 'of length', len(key_order))
    # try to visit each key
    for key in key_order:
        path_to_key = bfs_2d_grid(grid, keys[currKey], keys[key], exclude=wallChar)
        if path_to_key is None:
            print("error: bad path from", currKey, "to", key)
            exit(1)
        # 'move' to the next key
        currKey = key
        steps += len(path_to_key) - 1

    print("steps", steps)


def runpart1():
    part1(parseInputFile("input1.txt"))

###########################
# part2
###########################
def part2(grid):
    print_2d_grid(grid)
    keys, doors, starts = findKeysAndDoorsAndStarts(grid)
    print("start", starts)
    print("keys", keys)
    print("doors", doors)

    steps = 0

    # manually count number of steps on each path
    robot_paths = [
        ['y','a','c','i','q','x','n'],
        ['u','k','b','h'],
        ['o','r','j','d','v','p'],
        ['t','g','e','z','w','f','s','m','l']
    ]

    for i in range(len(starts)):
        start = starts[i]
        big_path = robot_paths[i]
        print("robot",start,"going to",big_path[0])
        path = bfs_2d_grid(grid, start, keys[big_path[0]], exclude=wallChar)
        currLoc = path[-1]
        steps += len(path) - 1
        for j in range(1, len(big_path)):
            path = bfs_2d_grid(grid, currLoc, keys[big_path[j]], exclude=wallChar)
            currLoc = path[-1]
            steps += len(path) - 1

    print("steps",steps)

def runpart2():
    part2(parseInputFile("input2.txt"))

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
