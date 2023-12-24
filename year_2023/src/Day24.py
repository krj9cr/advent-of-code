import time
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

class Hailstone:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return str(self.position) + " @ " + str(self.velocity)

    def get_position(self, t):
        return self.position + (self.velocity * (t, t, t))

    # https://stackoverflow.com/a/2931703
    # The two lines intersect if there is an intersection point p:
    # p = as + ad * u
    # p = bs + bd * v
    # If this equation system has a solution for u>=0 and v>=0
    # (the positive direction is what makes them rays), the rays intersect.
    def intersects(self, other):
        asx, asy = (self.position[0], self.position[1])
        bsx, bsy = (other.position[0], other.position[1])
        adx, ady = (self.velocity[0], self.velocity[1])
        bdx, bdy = (other.velocity[0], other.velocity[1])
        try:
            u = (asy * bdx + bdy * bsx - bsy * bdx - bdy * asx) / (adx * bdy - ady * bdx)
            v = (asx + adx * u - bsx) / bdx
        except ZeroDivisionError:
            return None
        if u >= 0 and v >= 0:
            # this is p, the point of intersection
            return asx + (adx * u), asy + (ady * u)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        hailstones = []
        for line in file:
            line = line.strip().split(" @ ")
            position = tuple([int(i) for i in line[0].split(", ")])
            velocity = tuple([int(i) for i in line[1].split(", ")])
            hailstones.append(Hailstone(position, velocity))
        return hailstones

def part1():
    hailstones = parseInput(24)

    # example
    minXY = 7
    maxXY = 20
    # input
    minXY = 200000000000000
    maxXY = 400000000000000
    area = Polygon([(minXY, minXY), (minXY, maxXY), (maxXY, maxXY), (maxXY, minXY)])
    print("area", area)

    answer = 0
    num_hailstones = len(hailstones)
    for i in range(num_hailstones):
        hailstone1 = hailstones[i]
        for j in range(i + 1, num_hailstones):
            if i == j:
                continue
            hailstone2 = hailstones[j]
            intersection = hailstone1.intersects(hailstone2)
            print(hailstone1)
            print(hailstone2)
            print("intersects", intersection)
            # check if within area
            if intersection:
                point = Point(intersection)
                contains = area.contains(point)
                print("contained in area:", contains)
                if contains:
                    answer += 1
            print()
    print("answer", answer)


def part2():
    lines = parseInput(24)
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
