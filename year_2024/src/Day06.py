import copy
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            l = []
            for char in line:
                l.append(char)
            lines.append(l)
        return lines

def getGuardStart(grid):
    for j in range(0, len(grid)):
        row = grid[j]
        for i in range(0, len(row)):
            item = row[i]
            if item == "^":
                return i, j

def guardStep(grid, guardDir, guardLoc):
    nextDir = (0, 0)
    nextGuardDir = ""
    if guardDir == "^":
        nextDir = (0, -1)
        nextGuardDir = ">"
    elif guardDir == "<":
        nextDir = (-1, 0)
        nextGuardDir = "^"
    elif guardDir == ">":
        nextDir = (1, 0)
        nextGuardDir = "v"
    elif guardDir == "v":
        nextDir = (0, 1)
        nextGuardDir = "<"
    else:
        print("UH OH")
    i, j = (guardLoc[0] + nextDir[0], guardLoc[1] + nextDir[1])
    # check bounds
    if 0 <= j < len(grid) and 0 <= i < len(grid[j]):
        nextSpot = grid[j][i]
        if nextSpot == "#":
            # don't move, turn
            return guardLoc, nextGuardDir
        else:
            # move forward
            return (i, j), guardDir
    else:
        return None, None

def print_2d_grid(grid, seen):
    count = 0
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = grid[j][i]
            if seen.get((i, j)):
                print("X", end="")
                count += 1
            else:
                print(item, end="")
        print()

    print("COUNT", count)

# run sim and detect if any loops
def runSim(grid, guardStart):
    guardDir = "^"
    guardLoc = guardStart
    seen = {guardLoc: guardDir}
    steps = 0
    while True:
        nextGuardLoc, nextGuardDir = guardStep(grid, guardDir, guardLoc)
        # guard walked off the map case (no loop)
        if nextGuardLoc is None or nextGuardDir is None:
            return False
        # loop case? we've been at this spot facing the same direction before
        elif seen.get(nextGuardLoc) and seen[nextGuardLoc] == nextGuardDir:
            return True
        else:
            guardDir = nextGuardDir
            guardLoc = nextGuardLoc
            seen[guardLoc] = guardDir
            # TODO... smarter thing would be to keep track of all the directions we've been at at this location, I think
            steps += 1
        if steps > len(grid) * len(grid[0]):
            print("steps", steps)
            # assume loop....?
            print("ASSUMING LOOP")
            return True

def part1():
    grid = parseInput(6)
    guardDir = "^"
    guardStart = getGuardStart(grid)
    guardLoc = guardStart
    seen = {guardLoc: guardDir}
    while True:
        print(guardLoc, guardDir)
        nextGuardLoc, nextGuardDir = guardStep(grid, guardDir, guardLoc)
        if nextGuardLoc is None or nextGuardDir is None:
            break
        else:
            guardDir = nextGuardDir
            guardLoc = nextGuardLoc
            seen[guardLoc] = guardDir
    print_2d_grid(grid, seen)
    print(len(seen))

def part2():
    grid = parseInput(6)
    guardStart = getGuardStart(grid)

    total = 0
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = grid[j][i]
            if item == ".":
                # just start with one
                simGrid = copy.deepcopy(grid)
                # add an obstacle
                simGrid[j][i] = "#"
                loop = runSim(simGrid, guardStart)
                if loop:
                    print(i, j, " LOOP")
                    total += 1
                else:
                    print(i, j, " NOT LOOP")
    print(total)


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
