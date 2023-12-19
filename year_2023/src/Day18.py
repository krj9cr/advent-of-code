import time
from collections import deque

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            parts = line.split(" ")
            lines.append((parts[0], int(parts[1]), parts[2].strip("(").strip(")").strip("#")))
        return lines

def bfs_2d_grid(start, points, minX, maxX, minY, maxY):
    queue = deque([start])
    seen = set([start])
    while queue:
        (x, y) = queue.popleft()
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if minX <= x2 < maxX and minY <= y2 < maxY:
                next = (x2, y2)
                if next not in seen and next not in points:
                    queue.append(next)
                    seen.add(next)
        if len(seen) % 100000 == 0:
            print(len(seen))
    return seen

def part1():
    digs = parseInput(18)
    print(digs)

    startPos = (0, 0)
    locations = {startPos: 0}
    vertices = [startPos]
    x, y = startPos
    for (direction, steps, _) in digs:
        if direction == "R":
            for i in range(steps + 1):
                locations[(x + i, y)] = 0
            x, y = x + steps, y
            vertices.append((x, y))
        elif direction == "L":
            for i in range(steps + 1):
                locations[(x - i, y)] = 0
            x, y = x - steps, y
            vertices.append((x, y))
        elif direction == "U":
            for i in range(steps + 1):
                locations[(x, y - i)] = 0
            x, y = x, y - steps
            vertices.append((x, y))
        elif direction == "D":
            for i in range(steps + 1):
                locations[(x, y + i)] = 0
            x, y = x, y + steps
            vertices.append((x, y))
    points = set(list(locations.keys()) + [startPos])
    print(points)
    print("vertices", vertices[:-1])

    # find the minX/maxX and Y of all the vertices
    minX = minY = 99999
    maxX = maxY = 0
    for (x, y) in vertices:
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    print("mins", minX, minY, "maxes", maxX, maxY)

    # try to print the thing
    # for j in range(minY, maxY + 1):
    #     for i in range(minX, maxX + 1):
    #         if (i, j) in points:
    #             print("#", end="")
    #         else:
    #             print(".", end="")
    #     print()

    # we're going to "cheat" and just pick a point we know is inside and do a flood fill with bfs
    # find some points near the top of the grid
    # for x, y in points:
    #     if y == minY:
    #         print("minY point", x, y)
    # inside = (1, 1)  # example case
    inside = (135, -77)  # my input
    seen = bfs_2d_grid(inside, points, minX, maxX, minY, maxY)
    print(len(seen))
    print(len(seen) + len(points))

# 0 means R, 1 means D, 2 means L, and 3 means U.
hexDirection = {
    0: "R",
    1: "D",
    2: "L",
    3: "U"
}

def part2():
    digs = parseInput(18)
    print(digs)

    digs2 = []
    for (_, _, hexStr) in digs:
        steps = int(hexStr[:5], 16)
        direction = hexDirection[int(hexStr[-1])]
        # print(direction, steps)
        digs2.append((direction, steps))
    print(digs2)

    startPos = (0, 0)
    locations = {startPos: 0}
    vertices = [startPos]
    x, y = startPos
    for (direction, steps) in digs2:
        if direction == "R":
            for i in range(steps + 1):
                locations[(x + i, y)] = 0
            x, y = x + steps, y
            vertices.append((x, y))
        elif direction == "L":
            for i in range(steps + 1):
                locations[(x - i, y)] = 0
            x, y = x - steps, y
            vertices.append((x, y))
        elif direction == "U":
            for i in range(steps + 1):
                locations[(x, y - i)] = 0
            x, y = x, y - steps
            vertices.append((x, y))
        elif direction == "D":
            for i in range(steps + 1):
                locations[(x, y + i)] = 0
            x, y = x, y + steps
            vertices.append((x, y))
    points = set(list(locations.keys()) + [startPos])
    # print(points)
    # print("vertices", vertices[:-1])

    # find the minX/maxX and Y of all the vertices
    minX = minY = 99999
    maxX = maxY = 0
    for (x, y) in vertices:
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    print("mins", minX, minY, "maxes", maxX, maxY)

    # try to print the thing...?
    # with open("myfile.txt", "w") as file1:
    #     for j in range(minY, maxY + 1):
    #         for i in range(minX, maxX + 1):
    #             if (i, j) in points:
    #                 file1.write("#")
    #             else:
    #                 file1.write(".")
    #         file1.write("\n")

    # we're going to "cheat" and just pick a point we know is inside and do a flood fill with bfs
    # find some points near the top of the grid
    # for x, y in points:
    #     if y == minY:
    #         print("minY point", x, y)
    inside = (1, 1)  # example case and input case wow
    seen = bfs_2d_grid(inside, points, minX, maxX, minY, maxY)
    print(len(seen))
    print(len(seen) + len(points))

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
