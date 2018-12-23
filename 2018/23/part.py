from z3 import *


def parseInput(path: str):
    with open(path, 'r') as file:
        return [parseLine(line) for line in file]


def parseLine(line: str):
    line = line.strip()
    split_line = line.split(", ")
    pos = split_line[0].replace("pos=<", "").replace(">", "")
    pos = pos.split(",")
    pos = tuple([int(p) for p in pos])
    r = int(split_line[1].replace("r=", ""))
    return pos, r


def findStrongest(bots):
    strongest = None
    maxr = 0
    for bot in bots:
        if bot[1] > maxr:
            maxr = bot[1]
            strongest = bot
    return strongest


def dist3D(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


# from a given bot, find other bots within range of this bot's radius
def findBotsInRange(bots, strongestBot):
    inrange = set()
    strongestPos = strongestBot[0]
    r = strongestBot[1]
    for bot in bots:
        dist = dist3D(strongestPos, bot[0])
        if dist <= r:
            inrange.add(bot)
    return inrange


def part1(path: str):
    bots = parseInput(path)
    strongest = findStrongest(bots)
    botsInRange = findBotsInRange(bots, strongest)
    print("part1:", len(botsInRange))


def z3_abs(x):
    return If(x >= 0, x, -x)


def z3_dist(x, y):
    return z3_abs(x[0] - y[0]) + z3_abs(x[1] - y[1]) + z3_abs(x[2] - y[2])


def part2(path: str):
    bots = parseInput(path)

    # init stuff for z3
    x, y, z = Ints("x y z")
    op = Optimize()
    cost = x * 0

    # add constraints
    for bot_pos, bot_r in bots:
        cost += If(z3_dist((x, y, z), bot_pos) <= bot_r, 1, 0)
    # consequently there were no ties, so we didn't have to check for the point closest to (0, 0, 0)
    op.maximize(cost)

    # get info from z3
    op.check()
    model = op.model()
    print(model)
    print(dist3D((0, 0, 0), (model[x].as_long(), model[y].as_long(), model[z].as_long())))
