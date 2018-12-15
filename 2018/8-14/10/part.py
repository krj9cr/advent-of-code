def readInput(path):
    with open(path, 'r') as file:
        return [parseInput(line) for line in file]


def parseInput(line):
    stripped = line.strip().split("<")
    position = stripped[1].split(">")[0].split(",")
    velocity = stripped[2].split(">")[0].split(",")
    x = int(position[0].strip())
    y = int(position[1].strip())         # apparently up is negative
    run = int(velocity[0].strip())
    rise = int(velocity[1].strip())  # apparently up is negative
    if run == 0:
        m = float("inf")
        if y == 0:
            b = 0
        else:
            b = None
    else:
        m = float(rise) / float(run)
        b = int(y - (m * x))
    return x, y, m, b, run, rise


def initBoard(lines, width, height):
    # find max or pick sizes for now
    board = []
    # init board
    for i in range(0, width):
        row = []
        for j in range(0, height):
            row.append(".")
        board.append(row)
    return board


def printBoard(board):
    for row in board:
        for item in row:
            print(item, end='')
        print('')


def fillBoard(points, board, w, h, t=0):
    # fill board
    for point in points:
        # assume t=0 for now
        x = point[0] + (t * point[2])
        y = point[1] + (t * point[3])
        board[y][x] = "#"


def intersect(line1, line2):
    x1, y1, m1, b1, run1, rise1 = line1
    x2, y2, m2, b2, run2, rise2 = line2

    # check if lines have the same slope
    # then they are parallel and will never intersect
    if m1 == m2:
        return None

    # check if one of the lines has infinite slope
    # then the intersection can only occur where that vertical line is
    if m1 == float("inf"):
        x = x1
    elif m2 == float("inf"):
        x = x2
    else:
        x = int((b2 - b1) / (m1 - m2))

    # find the y location of intersection
    # by plugging into one of the equations
    if b1 == None:
        y = (m2 * x) + b2
    else:
        y = (m1 * x) + b1

    # find the time of intersect
    # how many times was m applied to get to the intersection?
    if run1 == 0:
        t = (x - x2) / run2
    else:
        t = (x - x1) / run1
    return x, y, int(t)


def computePointsAtTime(lines, t):
    points = []
    for line in lines:
        x, y, m, b, run, rise = line
        newx = x + (run * t)
        newy = y + (rise * t)
        points.append([newx, newy])
    return points


def drawPoints(points):
    # minX = min(points, key=lambda point: point[0])
    # minY = min(points, key=lambda point: point[1])
    maxX = max(points, key=lambda point: point[0])[0]
    maxY = max(points, key=lambda point: point[1])[1]
    board = []
    for j in range(0, maxY+1):
        row = []
        for i in range(0, maxX+1):
            row.append(".")
        board.append(row)

    for point in points:
        x = point[0]
        y = point[1]
        board[y][x] = "#"

    for row in board:
        for item in row:
            print(item, end="")
        print("")


def part1(path):
    lines = readInput(path)
    times = {}
    for i in range(0, len(lines)):
        line1 = lines[i]
        for j in range(0, len(lines)):
            if i == j:
                continue
            line2 = lines[j]
            intersection = intersect(line1, line2)
            if intersection == None:
                continue
            else:
                t = intersection[2]
                if times.get(t) is None:
                    times[t] = 1
                else:
                    times[t] += 1
    besttime = max(times, key=lambda x: times[x])
    print("time:", besttime)  # printing this was the answer to part2!
    points = computePointsAtTime(lines, besttime)
    drawPoints(points)
