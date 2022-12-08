import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        grid = []
        for line in lines:
            row = [int(char) for char in line]
            grid.append(row)
        return grid

def isVisible(x, y, grid, width, height):
    item = grid[y][x]
    # go up
    visibleUp = True
    for y2 in range(y-1, -1, -1):
        if 0 <= y2 < height:
            item2 = grid[y2][x]
            if item2 >= item:
                visibleUp = False
                break
    # go left
    visibleLeft = True
    # print("Working with x:", x, "for item: ", item)
    for x2 in range(x-1, -1, -1):
        # print("x2: ", x2)
        if 0 <= x2 < width:
            item2 = grid[y][x2]
            # print("comparing: ", x, ",", x2, "items: ", item, ",", item2)
            # print("is ", item2, ">", item)
            if item2 >= item:
                # print("not visible left")
                visibleLeft = False
                break
    # go down
    visibleDown = True
    for y2 in range(y+1, height):
        if 0 <= y2 < height:
            item2 = grid[y2][x]
            if item2 >= item:
                visibleDown = False
                break
    # go right
    visibleRight = True
    for x2 in range(x + 1, width):
        if 0 <= x2 < width:
            item2 = grid[y][x2]
            if item2 >= item:
                visibleRight = False
                break
    return visibleUp or visibleLeft or visibleRight or visibleDown

def part1():
    grid = parseInput(8)
    # print(grid)
    count = 0
    width = len(grid[0])
    height = len(grid)
    for y in range(height):
        row = grid[y]
        for x in range(width):
            # if item is visible
            visible = isVisible(x, y, grid, width, height)
            # print(grid[y][x], "is ", visible)
            # print()
            if visible:
                count += 1
    print(count)



def scenicScore(x, y, grid, width, height):
    item = grid[y][x]
    # go up
    visibleUp = 0
    for y2 in range(y-1, -1, -1):
        if 0 <= y2 < height:
            item2 = grid[y2][x]
            if item2 >= item:
                visibleUp += 1
                break
            else:
                visibleUp += 1
    # go left
    visibleLeft = 0
    # print("Working with x:", x, "for item: ", item)
    for x2 in range(x-1, -1, -1):
        # print("x2: ", x2)
        if 0 <= x2 < width:
            item2 = grid[y][x2]
            # print("comparing: ", x, ",", x2, "items: ", item, ",", item2)
            # print("is ", item2, ">", item)
            if item2 >= item:
                visibleLeft += 1
                break
            else:
                visibleLeft += 1
    # go down
    visibleDown = 0
    for y2 in range(y+1, height):
        if 0 <= y2 < height:
            item2 = grid[y2][x]
            if item2 >= item:
                visibleDown += 1
                break
            else:
                visibleDown += 1
    # go right
    visibleRight = 0
    for x2 in range(x + 1, width):
        if 0 <= x2 < width:
            item2 = grid[y][x2]
            if item2 >= item:
                visibleRight += 1
                break
            else:
                visibleRight += 1
    # print(visibleUp, "*", visibleLeft, "*", visibleRight, "*", visibleDown)
    return visibleUp * visibleLeft * visibleRight * visibleDown


def part2():
    grid = parseInput(8)
    # print(grid)
    count = 0
    width = len(grid[0])
    height = len(grid)
    maxScore = 0
    for y in range(height):
        row = grid[y]
        for x in range(width):
            # if item is visible
            score = scenicScore(x, y, grid, width, height)
            # print(grid[y][x], "score: ", score)
            if score > maxScore:
                maxScore = score
    print(maxScore)

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
