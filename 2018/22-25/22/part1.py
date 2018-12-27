

def geologicalIndex(board, x: int, y: int, targetX: int, targetY: int):
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
            return board[y][x-1] * board[y-1][x]


def geologicalIndexEdges(x: int, y: int, targetX: int, targetY: int):
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
            return 0


def erosionLevelEdges(x: int, y:int, targetX: int, targetY: int, depth: int):
    return (geologicalIndexEdges(x, y, targetX, targetY) + depth) % 20183


def erosionLevel(board, x: int, y:int, targetX: int, targetY: int, depth: int):
    return (geologicalIndex(board, x, y, targetX, targetY) + depth) % 20183


def risk(board, startX: int, startY: int, targetX: int, targetY: int):
    total = 0
    for j in range(startY, targetY+1):
        for i in range(startX, targetX+1):
            total += board[j][i] % 3
    return total


def fillBoard(board, depth: int):
    targetY = len(board)
    targetX = len(board[0])
    for y in range(1, targetY):
        row = board[y]
        for x in range(1, targetX):
            board[y][x] = erosionLevel(board, x, y, targetX-1, targetY-1, depth)


def printBoard(board):
    for row in board:
        for item in row:
            regionType = item % 3
            if regionType == 0:
                print(".", end="")
            elif regionType == 1:
                print("=", end ="")
            elif regionType == 2:
                print("|", end="")
            else:
                print("?", end="")
        print("")

def initBoard(startX: int, startY: int, targetX: int, targetY: int, depth: int):
    board = []
    for j in range(startY, targetY+1):
        row = []
        for i in range(startX, targetX+1):
            if i == 0 or j == 0:
                row.append(erosionLevelEdges(i, j, targetX, targetY, depth))
            else:
                row.append(0)
        board.append(row)
    return board


def part1(depth: int, targetX: int, targetY: int):
    board = initBoard(0, 0, targetX, targetY, depth)
    # printBoard(board)
    fillBoard(board, depth)
    # printBoard(board)
    totalRisk = risk(board, 0, 0, targetX, targetY)
    print(totalRisk)
