import time
import sympy
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from sympy import solve

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
    # minXY = 7
    # maxXY = 20
    # input
    minXY = 200000000000000
    maxXY = 400000000000000
    area = Polygon([(minXY, minXY), (minXY, maxXY), (maxXY, maxXY), (maxXY, minXY)])
    # print("area", area)

    answer = 0
    num_hailstones = len(hailstones)
    for i in range(num_hailstones):
        hailstone1 = hailstones[i]
        for j in range(i + 1, num_hailstones):
            if i == j:
                continue
            hailstone2 = hailstones[j]
            intersection = hailstone1.intersects(hailstone2)
            # print(hailstone1)
            # print(hailstone2)
            # print("intersects", intersection)
            # check if within area
            if intersection:
                point = Point(intersection)
                contains = area.contains(point)
                # print("contained in area:", contains)
                if contains:
                    answer += 1
            # print()
    print("answer", answer)

# some ideas: https://math.stackexchange.com/questions/4131973/find-a-line-that-crosses-multiple-line-segments

# there is some line with position lp, and velocity lv
# where for each Hailstone with position hp, and velocity hv
# hp + hv * t = lp + lv * t
# for some t >=0, where t is likely different for each hailstone
# e.g.
# hp2 + hv2 * t2 = lp + lv * t2
# hp3 + hv3 * t3 = lp + lv * t3
# better to split it up by x, y, z separately, easier to see the equations
# hp1x + hv1x * t1 = lpx + lvx * t1
# hp1y + hv1y * t1 = lpy + lvy * t1
# hp1z + hv1z * t1 = lpz + lvz * t1
# hp2x + hv2x * t2 = lpx + lvx * t2
# hp2y + hv2y * t2 = lpy + lvy * t2
# hp2z + hv2z * t2 = lpz + lvz * t2
# variables: lpx, lpy, lpz, lvx, lvy, lvz, and each t*
# constraints: each t > 0, we can probably also assume lp's are > 0
def part2():
    hailstones = parseInput(24)

    # try to use sympy, this one can actually do it!
    # https://docs.sympy.org/latest/guides/solving/solve-system-of-equations-algebraically.html

    # for assumptions, see https://docs.sympy.org/latest/modules/core.html#module-sympy.core.assumptions
    lpx = sympy.Symbol('lpx', integer=True, positive=True)
    lpy = sympy.Symbol('lpy', integer=True, positive=True)
    lpz = sympy.Symbol('lpz', integer=True, positive=True)
    lvx = sympy.Symbol('lvx', integer=True)
    lvy = sympy.Symbol('lvy', integer=True)
    lvz = sympy.Symbol('lvz', integer=True)

    equations = []
    symbols = []
    # note: we can just look at the first three stones... this actually finishes
    for i in range(3):
        symbols.append(sympy.Symbol('t' + str(i), integer=True, positive=True))
        hailstone = hailstones[i]
        # the equations are assumed to =0
        equations.append(((hailstone.position[0] + (hailstone.velocity[0] * symbols[i])) - (lpx + (lvx * symbols[i]))))
        equations.append(((hailstone.position[1] + hailstone.velocity[1] * symbols[i]) - (lpy + lvy * symbols[i])))
        equations.append(((hailstone.position[2] + hailstone.velocity[2] * symbols[i]) - (lpz + lvz * symbols[i])))
    symbols = [lpx, lpy, lpz, lvx, lvy, lvz] + symbols
    # print("eq", equations)
    # print("symbols", symbols)
    a = solve(equations, symbols, dict=True)[0]
    # print(a)
    print(a[lpx] + a[lpy] + a[lpz])

    # try to use scipy... didn't work because the number of variables has to match the number of functions
    # def equations(vars):
    #     # lpx, lpy, lpz, lvx, lvy, lvz = vars
    #
    #     eq = []
    #     for i in range(len(hailstones)):
    #         t = 6 + i
    #         hailstone = hailstones[i]
    #         eq.append(((hailstone.position[0] + (hailstone.velocity[0] * t)) - (vars[0] + (vars[3] * vars[t]))))
    #         eq.append(((hailstone.position[1] + hailstone.velocity[1] * vars[t]) - (vars[1] + vars[4] * vars[t])))
    #         eq.append(((hailstone.position[2] + hailstone.velocity[2] * vars[t]) - (vars[2] + vars[5] * vars[t])))
    #
    #     return eq
    #
    # result = fsolve(equations, [1] * (3 * (len(hailstones))))
    # print(result)

    # Try to use pulp: https://realpython.com/linear-programming-python/#using-pulp
    # didn't work because of non-linear programming (multiplying two variables together was not allowed)
    # Create the model
    # model = LpProblem(name="small-problem")  # , sense=LpMaximize) ???
    #
    # # Initialize the decision variables
    # lpx = LpVariable(name="lpx", lowBound=0, cat='Integer')
    # lpy = LpVariable(name="lpy", lowBound=0, cat='Integer')
    # lpz = LpVariable(name="lpz", lowBound=0, cat='Integer')
    # lvx = LpVariable(name="lvx", cat='Integer')
    # lvy = LpVariable(name="lvy", cat='Integer')
    # lvz = LpVariable(name="lvz", cat='Integer')
    #
    # t_variables = []
    # # Add the constraints to the model
    # for i in range(len(hailstones)):
    #     hailstone = hailstones[i]
    #     t = LpVariable(name="t" + str(i), lowBound=0, cat='Integer')
    #     t_variables.append(t)
    #     model += (hailstone.position[0] + (hailstone.velocity[0] * t) == lpx + (lvx * t),
    #               "hailstone" + str(i))
    #     # model += (hailstone.position[1] + hailstone.velocity[1] * t_variables[i] == lpy + lvy * t_variables[i],
    #     #           "hailstone" + str(i))
    #     # model += (hailstone.position[2] + hailstone.velocity[2] * t_variables[i] == lpz + lvz * t_variables[i],
    #     #           "hailstone" + str(i))
    #
    # print(model)
    # # Solve the problem
    # status = model.solve()
    #
    # print(f"status: {model.status}, {LpStatus[model.status]}")
    # print(f"objective: {model.objective.value()}")
    # for var in model.variables():
    #     print(f"{var.name}: {var.value()}")
    # for name, constraint in model.constraints.items():
    #     print(f"{name}: {constraint.value()}")

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
