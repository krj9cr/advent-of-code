import time
from shapely.geometry import Polygon

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            parts = line.split(" ")
            lines.append((parts[0], int(parts[1]), parts[2]))
        return lines

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
    points = list(locations.keys()) + [startPos]
    print(points)
    print("vertices", vertices[:-1])

    # this is... not working for concave polygon
    pgon = Polygon(points)
    print(pgon.area)

    # idea:
    # find the minX/maxX and Y of all the vertices
    # for each spot in the grid
    #   if it's in the list of points, count it
    #   otherwise try to shoot out in each direction, it should hit a polygon point in all 4 directions
    #   if it goes out of bounds, we know it's not contained
    #   count the contained points

def part2():
    lines = parseInput(18)
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
