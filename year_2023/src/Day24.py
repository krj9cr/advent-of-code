import time
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable

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

# some ideas: https://math.stackexchange.com/questions/4131973/find-a-line-that-crosses-multiple-line-segments

# there is some line with position lp, and velocity lv
# where for each Hailstone with position hp, and velocity hv
# hp + hv * t = lp + lv * t
# for some t >=0, where t is likely different for each hailstone
# e.g.
# hp2 + hv2 * t2 = lp + lv * t2
# hp3 + hv3 * t3 = lp + lv * t3
# better to split it up by x, y, z separately, less variables and easier to see the equations
# hp1x + hv1x * t1 = lpx + lvx * t1
# hp1y + hv1y * t1 = lpy + lvy * t1
# hp1z + hv1z * t1 = lpz + lvz * t1
# hp2x + hv2x * t2 = lpx + lvx * t2
# hp2y + hv2y * t2 = lpy + lvy * t2
# hp2z + hv2z * t2 = lpz + lvz * t2
# variables: lpx, lpy, lpz, lvx, lvy, lvz, and each t*
# constraints: t1 > 0, t2 > t1, etc. or just t2 > 0

# Try to follow https://realpython.com/linear-programming-python/#using-pulp
def part2():
    hailstones = parseInput(24)

    # Create the model
    model = LpProblem(name="small-problem")  # , sense=LpMaximize) ???

    # Initialize the decision variables
    lpx = LpVariable(name="lpx", lowBound=0)
    lpy = LpVariable(name="lpy", lowBound=0)
    lpz = LpVariable(name="lpz", lowBound=0)
    lvx = LpVariable(name="lvx", lowBound=0)
    lvy = LpVariable(name="lvy", lowBound=0)
    lvz = LpVariable(name="lvz", lowBound=0)

    # Add the constraints to the model
    model += (2 * lpx + lpy <= 20, "red_constraint")
    model += lpx + 2 * lpy

    print(model)
    # Solve the problem
    status = model.solve()

    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")
    for name, constraint in model.constraints.items():
        print(f"{name}: {constraint.value()}")

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
