import time
import re
import math

class Robot:
    def __init__(self, p_x, p_y, v_x, v_y):
        self.p_x = p_x
        self.p_y = p_y
        self.v_x = v_x
        self.v_y = v_y

    def __str__(self):
        return "p: " + str(self.p_x) + "," + str(self.p_y) + " v: " + str(self.v_x) + "," + str(self.v_y)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        robots = []
        for line in file:
            line = line.strip()
            match = re.match(r"p=([-0-9]+),([-0-9]+) v=([-0-9]+),([-0-9]+)", line)
            robot = Robot(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))
            robots.append(robot)
        return robots

def print_points(points, w, h):
    for j in range(h):
        for i in range(w):
            if (i, j) in points:
                print("X", end="")
            else:
                print(".", end="")
        print()
    print()

def part1():
    robots = parseInput(14)

    # example width/height
    w = 11
    h = 7
    # actual width/height
    w = 101
    h = 103

    steps = 100
    points = []
    for robot in robots:
        # print(robot)
        # project out where it will be after steps, modded by size
        p2_x = (robot.p_x + (robot.v_x * steps))
        p2_y = (robot.p_y + (robot.v_y * steps))
        point = (p2_x % w, p2_y % h)
        print(point)
        points.append(point)
        # print(math.fmod(p2_x, w), math.fmod(p2_y, h))
    print_points(points, w, h)

    # count quadrants
    mid_x = w // 2
    mid_y = h // 2
    print(mid_x, mid_y)
    quad1 = 0
    quad2 = 0
    quad3 = 0
    quad4 = 0
    for (x, y) in points:
        # left half
        if x < mid_x:
            # upper
            if y < mid_y:
                print(x, y)
                quad1 += 1
            # lower
            elif y > mid_y:
                quad3 += 1
        # right half
        elif x > mid_x:
            # upper
            if y < mid_y:
                quad2 += 1
            # lower
            elif y > mid_y:
                quad4 += 1
    print(quad1, quad2, quad3, quad4)
    print(quad1 * quad2 * quad3 * quad4)

def get_num_neighbors(point, points, w, h):
    x, y = point
    neighbors = []
    for nx, ny in (x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1):
        if 0 <= nx < w and 0 <= ny < h and (nx ,ny) in points:
            neighbors.append([nx, ny])
    return len(neighbors)

def part2():
    robots = parseInput(14)

    # example width/height
    w = 11
    h = 7
    # actual width/height
    w = 101
    h = 103

    steps = 100
    while True:
        points = []
        for robot in robots:
            # print(robot)
            # project out where it will be after steps, modded by size
            p2_x = (robot.p_x + (robot.v_x * steps))
            p2_y = (robot.p_y + (robot.v_y * steps))
            point = (p2_x % w, p2_y % h)
            points.append(point)
            # print(math.fmod(p2_x, w), math.fmod(p2_y, h))
        # print_points(points, w, h)

        # if more than 10 points have at least 2 adjacent neighbors...?
        num_close_points = 0
        for point in points:
            num = get_num_neighbors(point, points, w, h)
            if num >= 4:
                num_close_points += 1
        if num_close_points >= 15:
            print_points(points, w, h)
            print(steps)
            break
        steps += 1

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
