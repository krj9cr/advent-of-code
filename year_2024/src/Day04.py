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

def goInDir(grid, dir, x, y, nextLetter):
    curr = (x, y)
    (x2, y2) = tuple(map(sum, zip(curr, dir)))
    if checkBounds(grid, x2, y2):
        nextItem = grid[y2][x2]
        print(x2, y2, ":", nextItem)
        if nextItem == nextLetter:
            return x2, y2

def checkDir(grid, dir, x, y):
    next = goInDir(grid, dir, x, y, "M")



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
                dir = (0, -1)
                (x2, y2) = tuple(map(sum, zip(curr, dir)))
                if checkBounds(lines, x2, y2):
                    nextItem = lines[y2][x2]
                    print(x2, y2, ":", nextItem)
                    if nextItem == "M":

                # down
                dir = (0, 1)
                # left
                dir = (-1, 0)
                # right
                dir = (1, 0)
                # up left
                dir = (-1, -1)
                # up right
                dir = (1, -1)
                # down left
                dir = (-1, 1)
                # down right
                dir = (1, 1)

    print(count)

def part2():
    lines = parseInput(4)
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
