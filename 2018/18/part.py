from copy import deepcopy


def readInput(path):
    with open(path, 'r') as file:
        lines = []
        for line in file:
            lines.append([c for c in line.strip()])
        return lines


def printBoard(board):
    for row in board:
        print(''.join(row))


def countAdjType(board, x, y, target):
    count = 0
    for x2, y2 in ((x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1,y+1), (x, y+1), (x+1, y+1)):
        if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] == target:
            count += 1
    return count


def oneMinute(board):
    nextBoard = deepcopy(board)
    for y in range(0,len(board)):
        row = board[y]
        for x in range(0, len(row)):
            item = row[x]
            if item == ".":
                numTrees = countAdjType(board, x, y, "|")
                if numTrees >= 3:
                    nextBoard[y][x] = "|"
            elif item == "|":
                if countAdjType(board, x, y, "#") >= 3:
                    nextBoard[y][x] = "#"
            elif item == "#":
                numLum = countAdjType(board, x, y, "#")
                numTree = countAdjType(board, x, y, "|")
                if numLum < 1 or numTree < 1:
                    nextBoard[y][x] = "."
    return nextBoard


def countType(board, target):
    count = 0
    for y in range(0, len(board)):
        row = board[y]
        for x in range(0, len(row)):
            if row[x]  == target:
                count += 1
    return count


def part1(path):
    board = readInput(path)
    printBoard(board)
    numIters = 10
    for i in range(0, numIters):
        board = oneMinute(board)
        print(i)
        printBoard(board)
        print("")
    totalTrees = countType(board, "|")
    totalLum = countType(board, "#")
    print("Trees:",totalTrees,"lum:", totalLum)
    print("answer:", totalTrees * totalLum)


def part2(path):
    board = readInput(path)
    printBoard(board)
    numIters = 1000
    # since my input looks like a spiral,
    # the answer for 1000000000 is apparently the same as 1000
    for i in range(0, numIters):
        board = oneMinute(board)
        print(i)
        printBoard(board)
        print("")
    totalTrees = countType(board, "|")
    totalLum = countType(board, "#")
    print("Trees:",totalTrees,"lum:", totalLum)
    print("answer:", totalTrees * totalLum)
