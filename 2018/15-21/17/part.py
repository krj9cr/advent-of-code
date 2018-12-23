def readInput(path):
    minX = 500
    maxX = 500
    minY = 0
    maxY = 0
    with open(path, 'r') as file:
        coords = [(500, 0)]
        for line in file:
            line = line.strip().split(", ")
            if "x" in line[0]:
                x = int(line[0].replace("x=", ""))
                y = line[1].replace("y=", "")
                y1, y2 = y.split("..")
                y1 = int(y1)
                y2 = int(y2)
                if x > maxX:
                    maxX = x
                if x < minX:
                    minX = x
                if y1 < minY:
                    minY = y1
                if y2 > maxY:
                    maxY = y2
                for ys in range(y1, y2 + 1):
                    coords.append((x, ys))
            else:
                y = int(line[0].replace("y=", ""))
                x = line[1].replace("x=", "")
                x1, x2 = x.split("..")
                x1 = int(x1)
                x2 = int(x2)
                if x2 > maxX:
                    maxX = x2
                if x1 < minX:
                    minX = x1
                if y < minY:
                    minY = y
                if y > maxY:
                    maxY = y
                for xs in range(x1, x2 + 1):
                    coords.append((xs, y))
                # +/-1 to X to give a little buffer on each side
    return coords, minX - 1, maxX + 1, minY, maxY


def initBoard(coords, minX, maxX, minY, maxY):
    width = maxX - minX + 1
    height = maxY - minY + 1  # add end goal row

    board = []
    for j in range(0, height):
        row = []
        for i in range(0, width):
            row.append(".")
        board.append(row)

    for coord in coords:
        y = coord[1] - minY
        x = coord[0] - minX
        if coord == (500, 0):
            board[y][x] = "+"
        else:
            board[y][x] = "#"

    return board


def printBoard(board, numRows):
    for j in range(0, numRows):
        row = board[j]
        print(''.join(row))


def countWater(board):
    count = 0
    for j in range(0, len(board)):
        row = board[j]
        for i in range(0, len(row)):
            if row[i] in "|~":
                count += 1
    return count


def flow(board, start):
    canFall = set([start])
    canSpread = set()
    while canFall or canSpread:
        while canFall:
            down = canFall.pop()
            nextDown = flowDown(board, down)
            if nextDown:
                canSpread.add(nextDown)
        # printBoard(board, 10)
        while canSpread:
            mid = canSpread.pop()
            left = flowLeft(board, mid)
            right = flowRight(board, mid)
            if left is None and right is None and 0 <= mid[1]-1:
                canSpread.add((mid[0], mid[1]-1))
            else:
                if left:
                    canFall.add(left)
                if right:
                    canFall.add(right)


def flowDown(board, start):
    x, y = start
    while y < len(board):
        y2 = y + 1
        if y2 < len(board) and board[y2][x] in ".~|":
            board[y][x] = "|"
        elif y2 >= len(board):  # we hit bottom!
            board[y][x] = "|"
            return None
        else:
            return x, y
        y += 1
    return None


def flowLeft(board, start):
    x, y = start
    y2 = y + 1
    # x = x - 1
    while 0 <= x < len(board):
        # print(x, y)
        if board[y][x] != "#":
            board[y][x] = "~"
            if y2 < len(board) and board[y2][x] in ".|":
                return x, y
        else:
            return None
        x = x - 1
    return None

def flowRight(board, start):
    x, y = start
    y2 = y + 1
    # x += 1
    while 0 <= x < len(board[y]):
        if board[y][x] != "#":
            board[y][x] = "~"
            if y2 < len(board) and board[y2][x] in ".|":
                return x, y
        else:
            return None
        x += 1
    return None


def part1(path):
    coords, minX, maxX, minY, maxY = readInput(path)
    board = initBoard(coords, minX, maxX, minY, maxY)
    # printBoard(board, 20)

    currentSpot = (500 - minX, 0)
    end = (currentSpot[0], len(board) -1)
    # path, seen = bfs(board, currentSpot)
    flow(board, currentSpot)


    # print(path)
    # drawPath(board, path)
    printBoard(board, 20)
    answer = countWater(board)
    print("part1:", answer-7)  # minus for start line(s)
