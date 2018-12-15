from sortedcontainers import SortedDict
from collections import deque

startingHP = 200
goblinAttackPower = 3

def parseInput(path: str):
    with open(path, 'r') as file:
        return [parseLine(line) for line in file]


def parseLine(line: str):
    return [c for c in line.strip()]


def fillBoardWithUnits(board, units):
    for j in range(0, len(board)):
        row = board[j]
        for i in range(0, len(row)):
            unit = units.get((j, i))
            if unit is not None:
                board[j][i] = unit[0]
    return board


def printBoard(board):
    for j in range(0, len(board)):
        row = board[j]
        for i in range(0, len(row)):
            print(row[i], end="")
        print("")


def getUnits(board):
    units = {}
    for j in range(0, len(board)):
        row = board[j]
        for i in range(0, len(row)):
            char = row[i]
            if char in "EG":
                units[(j, i)] = (char, startingHP)
    # sort by 'read order'
    return SortedDict(sorted(units.items(), key=lambda k: k[0][0] + (k[0][1]*len(board[k[0][1]]))))


def isNextToBadGuy(board, y, x, goal):
    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
        if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] == goal:
            return True
    return False


def findSpots(board, goal):
    candidates = []
    for y in range(0, len(board)):
        row = board[y]
        for x in range(0, len(row)):
            item = row[x]
            if item == goal:
                for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                    if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] == ".":
                        candidates.append((y2, x2))
    return candidates


def bfs(board, start, end):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        y, x = path[-1]
        if (y, x) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] not in "#EG":
                if (y2, x2) not in seen:
                    queue.append(path + [(y2, x2)])
                    seen.add((y2, x2))


def attack(board, units, y, x, unitChar, elfAttackPower):
    oppChar = getOpposing(unitChar)
    possibleOpps = []

    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
        if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] == oppChar:
            unitToAttack = units.get((y2, x2))
            if unitToAttack is not None:
                possibleOpps.append((y2, x2, unitToAttack))

    if len(possibleOpps) > 0:
        # sort by HP, otherwise it's already sorted in read order
        possibleOpps = sorted(possibleOpps, key=lambda k: k[2][1])
        # print(unitChar, (y,x), possibleOpps)
        ay, ax, unitToAttack = possibleOpps[0]
        attackPower = elfAttackPower
        if unitChar == "G":
            attackPower = goblinAttackPower
        newHp = unitToAttack[1] - attackPower
        if newHp > 0:  # add attacked unit if it's still alive
            units[(ay, ax)] = (unitToAttack[0], newHp)
        else:  # remove unit
            units.pop((ay, ax))
            board[ay][ax] = "."
    return units


def getOpposing(char):
    if char == "E":
        return "G"
    elif char == "G":
        return "E"
    else:
        print("bad character")


def isOpposition(units):
    foundGoblin = False
    foundElf = False
    for unit in units:
        char = units[unit][0]
        if char == "E":
            foundElf = True
        elif char == "G":
            foundGoblin = True
        if foundElf and foundGoblin:
            break
    return foundElf and foundGoblin


def countElves(units):
    count = 0
    for u in units:
        if units[u][0] == "E":
            count += 1
    return count


def part1(board, units, numStartingElves: int, elfAttackPower: int):
    # board = parseInput(path)
    # units = getUnits(board)
    # numStartingElves = countElves(units)

    # print(units)
    # printBoard(board)

    # start rounds
    numRounds = 0
    while isOpposition(units):
        hadTurn = []
        # each unit takes a turn
        # for y, x in units:
        for y in range(0, len(board)):
            row = board[y]
            for x in range(0, len(row)):
                # print(hadTurn)
                if board[y][x] in "EG" and (y, x) not in hadTurn:
                    # pop unit off the list
                    unit = units.pop((y, x))
                    badGuy = getOpposing(unit[0])

                    if isNextToBadGuy(board, y, x, badGuy):
                        attack(board, units, y, x, unit[0], elfAttackPower)
                        units[(y, x)] = unit
                        hadTurn.append((y, x))
                    else:
                        # find open spots
                        candidates = findSpots(board, badGuy)
                        # find paths to those spots
                        candidatePaths = [bfs(board, (y, x), candidate) for candidate in candidates]
                        candidatePaths = [path for path in candidatePaths if path is not None]
                        candidatePaths = sorted(sorted(candidatePaths, key=lambda d: d[0]), key=lambda c: len(c))
                        # try to move unit + attack
                        if len(candidatePaths) > 0:
                            path = candidatePaths[0]
                            if path is not None and len(path) > 1:
                                board[y][x] = "."
                                ny, nx = path[1]
                                board[ny][nx] = unit[0]
                                attack(board, units, ny, nx, unit[0], elfAttackPower)
                                units[(ny, nx)] = unit
                                hadTurn.append((ny, nx))
                            else:
                                attack(board, units, y, x, unit[0], elfAttackPower)
                                units[(y, x)] = unit
                                hadTurn.append((y, x))
                        else:
                            units[(y, x)] = unit
                            hadTurn.append((y, x))
        if countElves(units) != numStartingElves:
            return None
        # increment
        numRounds += 1
        # print(numRounds)
        # print(units)
        # printBoard(board)
    print(units)
    printBoard(board)
    print("")
    numRounds = numRounds - 1
    print("elf power:", elfAttackPower)
    print("numRounds:",numRounds)
    totalHP = sum([units.get((y, x))[1] for y, x in units])
    print("HP:", totalHP)
    answer = numRounds * totalHP
    print("answer:", numRounds * totalHP)
    return answer


def part2(path: str):
    board = parseInput(path)
    units = getUnits(board)
    numStartingElves = countElves(units)
    power = 4
    result = None
    while result is None:
        print(power)
        result = part1(board, units, numStartingElves, power)
        power += 1
