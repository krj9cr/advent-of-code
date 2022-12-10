import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

def checkCycle(cycle, x):
    # print("cycle", cycle, "x", x)
    if cycle == 20 or cycle == 60 or cycle == 100 or \
        cycle == 140 or cycle == 180 or cycle == 220:
        # print("------ cycle", cycle, "x", x)
        return cycle * x
    return 0

def part1():
    lines = parseInput(10)
    # print(lines)
    x = 1
    cycle = 0
    total = 0
    for line in lines:
        # print(line)
        if line == "noop":
            cycle += 1
            total += checkCycle(cycle, x)
        elif line.startswith("addx"):
            cycle += 1
            total += checkCycle(cycle, x)
            cycle += 1
            total += checkCycle(cycle, x)
            x += int(line.split(" ")[1])
    print("total", total)

w, h = 40, 6

def drawPixel(board, cycle, x):
    mod = cycle % w
    y_coord = cycle // w
    x_coord = mod
    pixel = '.'
    newx = x + (w * y_coord)
    if cycle == newx - 1 or cycle == newx or cycle == newx + 1:
        pixel = '#'
    # print("cycle", cycle, "x", x, "UPDATING:", x_coord, y_coord, "pixel", pixel)
    board[y_coord][x_coord] = pixel

def drawBoard(board):
    for row in board:
        for item in row:
            print(item, end="")
        print()

def part2():
    lines = parseInput(10)
    # print(lines)
    x = 1
    cycle = 0
    total = 0
    board = [['.' for x in range(w)] for y in range(h)]
    # drawBoard(board)
    for line in lines:
        # print(line)
        if line == "noop":
            drawPixel(board, cycle, x)
            cycle += 1
            # total += checkCycle(cycle, x)
        elif line.startswith("addx"):
            drawPixel(board, cycle, x)
            cycle += 1
            # total += checkCycle(cycle, x)
            drawPixel(board, cycle, x)
            cycle += 1
            # total += checkCycle(cycle, x)
            x += int(line.split(" ")[1])
        # drawBoard(board)
    drawBoard(board)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
