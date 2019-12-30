from collections import deque
import itertools


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

    return distToObjects


def checkRules(path, rules):
    for i, j in rules:
        if path.index(i) > path.index(j):
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

    # generate all possible key paths
    # working_orders = {}
    best_path = None
    best_steps = 5206 # found this number after guessing

    # rules
    # rules = [("k","v"),("a","u"),("d","k"),("a","d"),("d","b"),("a","h"),("d","h"),
    #          ("u","c"),("b","c"),("g","c"),("u","i"),("b","i"),("g","i"),("f","n"),
    #          ("z","n"),("w","q"),("w","x"),("p","s"),("p","m"),("p","l"),("q","s"),
    #          ("q","m"),("q","l"),("q","f"),("v","p"),("k","p"),("v","e"),("r","j")]
    rules = []
    possible_start =['g','r','j', 'd','y', 'a', 'u', 'k', 'b', 'h','c', 'i', 'v', 'p', 'o', 't',   'e', 'z', 'w', 'q', 'x', 'f', 's', 'm', 'l', 'n']

    paths = {}
    # copmute paths from start to keys
    for key in keys:
        path = bfs(grid, start, keys[key])
        paths[("start",key)] = path
    # compute paths between keys
    for key in keys:
        for key2 in keys:
            if key != key2:
                path = bfs(grid, keys[key], keys[key2])
                paths[(key,key2)] = path

    letters = list(keys.keys())
    for l in possible_start:
        letters.remove(l)

    all_permutations = itertools.permutations(letters)  # no list(...)

    # for each keypath, try to run it
    for perm in all_permutations:
        key_order = possible_start + list(perm)
        # check some rules before even trying
        if not checkRules(key_order, rules):
            # print("tossing",key_order)
            continue
        currLoc = start
        currKey = "start"
        acquiredKeys = set()
        steps = 0
        badPath = False
        print('testing path', key_order)
        # try to visit each key
        for key in key_order:
            # path_to_key = bfs(grid, currLoc, keys[key])
            path_to_key = paths[(currKey, key)]
            # print("path from",currLoc,"to",key,":", path_to_key)
            # check if the path contains a door
            for coord in path_to_key:
                for door in doors:
                    if door.lower() in acquiredKeys:
                        continue
                    if coord == doors[door]:
                        # print(door,"blocks path")
                        badPath = True
                        break
                if badPath:
                    break
            # otherwise 'move' to the key and pick it up
            currLoc = path_to_key[-1]
            currKey = key
            steps += len(path_to_key) - 1
            acquiredKeys.add(key)
            # stop early if worse than best
            if steps >= best_steps:
                badPath = True
            if badPath:
                break
        if not badPath:
            # once we visited all the keys, save the steps
            if steps < best_steps:
                best_steps = steps
                best_path = key_order
                print("best path",best_path,"with steps", best_steps)

    print("best path", best_path, "with steps", best_steps)


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
