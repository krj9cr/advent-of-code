import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [ line.strip().split(" ") for line in file]
        res = []
        for line in lines:
            res.append([line[0], int(line[1])])
        return res


def manhattan(head, tail):
    x1 = head[0]
    x2 = tail[0]
    y1 = head[1]
    y2 = tail[1]
    return abs(x1 - x2) + abs(y1 - y2)

def moveTail(head, tail):
    dist = manhattan(head, tail)
    if dist > 1:
        # if in same row
        if head[1] == tail[1]:
            if head[0] < tail[0]:
                return tail[0] - 1, tail[1]
            else:
                return tail[0] + 1, tail[1]
        # if in same col
        if head[0] == tail[0]:
            if head[1] < tail[1]:
                return tail[0], tail[1] - 1
            else:
                return tail[0], tail[1] + 1
        # not in same col/row, so move diagonally
        if dist > 2:
            # print("diagonally")
            if head[0] < tail[0]:
                if head[1] < tail[1]:
                    # print("left, up")
                    return tail[0] - 1, tail[1] - 1
                else:
                    # print("left, down")
                    return tail[0] -1 , tail[1] + 1
            else:
                if head[1] < tail[1]:
                    # print("right, up")
                    return tail[0] + 1, tail[1] -1
                else:
                    # print("right, down")
                    return tail[0] + 1, tail[1] + 1

    return tail[0], tail[1]


def part1():
    lines = parseInput(9)
    # print(lines)
    head = (0, 0)
    tail = (0, 0)
    uniqueTails = {}
    for line in lines:
        direction = line[0]
        steps = line[1]
        # print("direction:", direction, "steps:",steps)
        for i in range(steps):
            if direction == "R":
                head = (head[0] + 1, head[1])
                tail = moveTail(head, tail)
            elif direction == "L":
                head = (head[0] - 1, head[1])
                tail = moveTail(head, tail)
            elif direction == "U":
                head = (head[0], head[1] - 1)
                tail = moveTail(head, tail)
            elif direction == "D":
                head = (head[0], head[1] + 1)
                tail = moveTail(head, tail)
            uniqueTails[tail] = True
            # print("head:", head)
            # print("tail:", tail)
            # print()
    # print("Unique tails:", uniqueTails.keys())
    print(len(uniqueTails))


def moveKnots(head, knots):
    new_knots = []
    for i in range(len(knots)):
        if i == 0:
            new_knots.append(moveTail(head, knots[i]))
        else:
            new_knots.append(moveTail(new_knots[i-1], knots[i]))
    # print(new_knots)
    return new_knots

def part2():
    lines = parseInput(9)
    # print(lines)
    head = (0, 0)
    knots = [ (0, 0) for _ in range(9) ]
    # print(knots)
    uniqueTails = {}
    for line in lines:
        direction = line[0]
        steps = line[1]
        # print("direction:", direction, "steps:",steps)
        for i in range(steps):
            if direction == "R":
                head = (head[0] + 1, head[1])
                knots = moveKnots(head, knots)
            elif direction == "L":
                head = (head[0] - 1, head[1])
                knots = moveKnots(head, knots)
            elif direction == "U":
                head = (head[0], head[1] - 1)
                knots = moveKnots(head, knots)
            elif direction == "D":
                head = (head[0], head[1] + 1)
                knots = moveKnots(head, knots)
            uniqueTails[knots[8]] = True
            # print("head:", head)
            # print("knots:", knots)
            # print()
    # print("Unique tails:", uniqueTails.keys())
    print(len(uniqueTails))

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
