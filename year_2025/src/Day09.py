import time, os
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from shapely.plotting import plot_polygon

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = tuple([int(i) for i in line.strip().split(',')])
            lines.append(line)
        return lines

def part1():
    lines = parseInput()
    # print(lines)

    maxarea = 0
    for i, (x1, y1) in enumerate(lines):
        for j, (x2, y2) in enumerate(lines):
            if i == j:
                continue
            # print(x1,y1, "and", x2, y2)
            # find the min x, y, and max x, y
            minx = min(x1, x2)
            miny = min(y1, y2)
            maxx = max(x1, x2)
            maxy = max(y1, y2)
            # the area will be (maxx - minx) * (maxy - miny)?
            # print(maxx, minx, maxy, miny)
            area = (maxx - minx + 1) * (maxy - miny + 1)
            # print("area", area)
            if area > maxarea:
                maxarea = area
    print(maxarea)


def part2():
    lines = parseInput()
    # print(lines)

    big_shape = Polygon(lines)

    # fig, ax = plt.subplots()
    # plot_polygon(big_shape, ax=ax, add_points=True, color='green', alpha=0.5)
    # # plot_polygon(rectangle, ax=ax, add_points=True, color='blue', alpha=0.5)
    # ax.set_aspect('equal')
    # plt.show()

    maxarea = 0
    for i, (x1, y1) in enumerate(lines):
        for j, (x2, y2) in enumerate(lines):
            if i == j:
                continue
            # print(x1,y1, "and", x2, y2)
            # find the min x, y, and max x, y
            minx = min(x1, x2)
            miny = min(y1, y2)
            maxx = max(x1, x2)
            maxy = max(y1, y2)
            # the area will be (maxx - minx) * (maxy - miny)?
            # print(maxx, minx, maxy, miny)
            area = (maxx - minx + 1) * (maxy - miny + 1)

            # if area is contained
            rectangle = Polygon([(maxx, miny), (minx, miny), (minx, maxy), (maxx, maxy)])


            if rectangle.within(big_shape):
                # print("area", area)
                if area > maxarea:
                    maxarea = area
    print(maxarea)

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
