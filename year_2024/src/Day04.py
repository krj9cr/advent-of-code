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

def checkBounds(grid, x, y):
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        return True
    return False

def getDirLetter(grid, dir, x, y):
    curr = (x, y)
    (x2, y2) = tuple(map(sum, zip(curr, dir)))
    if checkBounds(grid, x2, y2):
        nextItem = grid[y2][x2]
        # print(x2, y2, ":", nextItem)
        return nextItem

def goInDir(grid, dir, x, y, nextLetter):
    curr = (x, y)
    (x2, y2) = tuple(map(sum, zip(curr, dir)))
    if checkBounds(grid, x2, y2):
        nextItem = grid[y2][x2]
        # print(x2, y2, ":", nextItem)
        if nextItem == nextLetter:
            return x2, y2

def checkDir(grid, dir, x, y):
    next = goInDir(grid, dir, x, y, "M")
    if next:
        next2 = goInDir(grid, dir, next[0], next[1], "A")
        if next2:
            next3 = goInDir(grid, dir, next2[0], next2[1], "S")
            if next3:
                return True
    return False


def part1():
    lines = parseInput(4)
    print(lines)
    count = 0
    for y in range(0, len(lines)):
        row = lines[y]
        for x in range(0, len(row)):
            item = row[x]
            if item == "X":
                print(x, y)
                # check 8 conditions for directions
                curr = (x, y)
                # up
                for dir in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)]:
                    if checkDir(lines, dir, x, y):
                        count += 1

    print(count)

def part2():
    lines = parseInput(4)
    print(lines)
    count = 0
    for y in range(0, len(lines)):
        row = lines[y]
        for x in range(0, len(row)):
            item = row[x]
            if item == "A":
                print(x, y)
                firstDiag = False
                # first diag
                one = (-1, -1)
                oneLetter = getDirLetter(lines, one, x, y)
                two = (1, 1)
                twoLetter = getDirLetter(lines, two, x, y)
                if (oneLetter == "M" and twoLetter == "S") or (oneLetter == "S" and twoLetter == "M"):
                    firstDiag = True
                    print("FIRST DIAG", oneLetter, twoLetter)
                # second diag
                one = (1, -1)
                oneLetter = getDirLetter(lines, one, x, y)
                two = (-1, 1)
                twoLetter = getDirLetter(lines, two, x, y)
                if ((oneLetter == "M" and twoLetter == "S") or (oneLetter == "S" and twoLetter == "M")) and firstDiag:
                    count += 1
                    print("COUNTING", x, y)

    print(count)

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
