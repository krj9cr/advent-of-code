import time
from copy import deepcopy

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        lines2 = []
        for line in lines:
            scoords = line.split(" -> ")
            line2 = []
            for scoord in scoords:
                line2.append([ int(c) for c in scoord.split(",")])
            lines2.append(line2)
        return lines2

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()


def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def part1():
    lines = parseInput(14)

    # Initialize Grid
    minx = 9999999
    maxx = 0
    miny = 0 # always 0
    maxy = 0
    for line in lines:
        print(line)
        for coord in line:
            if coord[1] > maxy:
                maxy = coord[1]
            # if coord[1] < miny:
            #     miny = coord[1]
            if coord[0] < minx:
                minx = coord[0]
            if coord[0] > maxx:
                maxx = coord[0]
    print("min/max X:", minx, maxx, "  min/max Y:", miny, maxy)
    w = maxx - minx + 1
    h = maxy - miny + 1
    print("w", w, "h", h)
    grid = []
    for j in range(h):
        row = []
        for i in range(w):
            row.append('.')
        grid.append(row)
    # print_2d_grid(grid)

    # Draw some lines
    for line in lines:
        for pair in zip(line, line[1:]):
            startx = pair[0][0]
            starty = pair[0][1]
            endx = pair[1][0]
            endy = pair[1][1]
            if startx == endx: # same col, vertical line
                x = startx - minx
                # print("Drawing pair", pair)
                if starty > endy:
                    for i in range(0, starty-endy+1, 1):
                        grid[starty+i][x] = "#"
                else:
                    for i in range(0, endy-starty+1, 1):
                        grid[starty+i][x] = "#"

            else: # horizontal line
                y = starty
                # print("Drawing pair", pair)
                if startx > endx:
                    x = endx - minx
                    # print("startx, endx",endx-minx, startx-minx)
                    for i in range(0, startx-endx+1, 1):
                        # print("x, y, i", x, y, i)
                        grid[y][x+i] = "#"
                else:
                    x = startx - minx
                    # print("startx, endx",endx-minx, startx-minx)
                    for i in range(0, endx-startx+1, 1):
                        # print("x, y", x+i, y)
                        grid[y][x+i] = "#"
    print_2d_grid(grid)

    # model sand falling
    sand_start = (500-minx, 0)
    print(sand_start)

    sand_count = 0
    sand_in_bounds = True
    while sand_in_bounds:
        # move one piece of sand
        (x, y) = deepcopy(sand_start)
        can_move = True
        while can_move:
            # print_2d_grid(grid)
            moved = False
            for (x2, y2) in [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]:
                if x2 < 0 or x2 >= w or y2 < 0 or y2 >= h:
                    sand_in_bounds = False
                    break
                if grid[y2][x2] == ".":
                    grid[y][x] = "."
                    grid[y2][x2] = "o"
                    (x, y) = (x2, y2)
                    moved = True
                    break
            if not moved:
                can_move = False
                break
            if not sand_in_bounds:
                break
        # sand comes to rest
        print("sand came to rest at:", x, y)
        sand_count += 1
        if not sand_in_bounds:
            print("sand out of bounds at ", x,y)
            break
    print("sand count", sand_count)
    print_2d_grid(grid)


# 271 too low


def part2():
    lines = parseInput(14)
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
