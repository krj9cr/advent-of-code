

def geologicalIndex(x: int, y: int, targetX: int, targetY: int, depth: int):
    if x == 0 and y == 0:
        return 0
    elif x == targetX and y == targetY:
        return 0
    else:
        if y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        else:
            return erosionLevel(x-1, y, targetX, targetY, depth) * erosionLevel(x, y-1, targetX, targetY, depth)


def erosionLevel(x: int, y:int, targetX: int, targetY: int, depth: int):
    return (geologicalIndex(x, y, targetX, targetY, depth) + depth) % 20183


def regionType(x: int, y:int, targetX: int, targetY: int, depth: int):
    return erosionLevel(x, y, targetX, targetY, depth) % 3


def risk(startX: int, startY: int, targetX: int, targetY: int, depth: int):
    total = 0
    for j in range(startY, targetY+1):
        for i in range(startX, targetX+1):
            total += regionType(i, j, targetX, targetY, depth)
    return total


def part1(depth: int, targetX: int, targetY: int):
    totalRisk = risk(0, 0, targetX, targetY, depth)
    print(totalRisk)



# def part2(path: str):
#     lines = parseInput(path)
#     print(lines)
