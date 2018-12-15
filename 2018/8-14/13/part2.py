import copy
from collections import OrderedDict

def readInput(path):
    with open(path, 'r') as file:
        return [[c for c in line.replace('\n','')] for line in file]


def printBoard(board):
    for row in board:
        for c in row:
            print(c, end='')
        print('')

def printBoardWithCarts(board, carts):
    for j in range(0, len(board)):
        row = board[j]
        for i in range(0, len(row)):
            cart = carts.get((i, j))
            if cart is not None:
                print(cart[0], end='')
            else:
                print(row[i], end='')
        print('')


def intersectionTurn(c, nextDir):
    if nextDir == 'left':
        nextDir = "straight"
        if c == ">":
            return "^", nextDir
        elif c == "<":
            return "v", nextDir
        elif c == "v":
            return ">", nextDir
        elif c == "^":
            return "<", nextDir
    elif nextDir == 'straight':
        nextDir = "right"
        return c, nextDir
    elif nextDir == 'right':
        nextDir = "left"
        if c == ">":
            return "v", nextDir
        elif c == "<":
            return "^", nextDir
        elif c == "v":
            return "<", nextDir
        elif c == "^":
            return ">", nextDir


def part2(path):
    board = readInput(path)
    # printBoard(board)

    # init board and carts
    carts = {}  # (x, y) => (icon, nextDir)
    for j in range(0, len(board)):
        row = board[j]
        for i in range(0, len(row)):
            c = row[i]
            if c in "<>":
                carts[(i, j)] = (c, "left")
                board[j][i] = "-"
            elif c in "v^":
                carts[(i, j)] = (c, "left")
                board[j][i] = "|"
    carts = OrderedDict(sorted(carts.items(), key=lambda k: k[0][0] + (k[0][1]*len(board[k[0][1]]))))
    # printBoardWithCards(board, carts)

    # run loop
    collision = False
    while len(carts) > 1:
        for cartLoc in carts:
            nextCarts = copy.deepcopy(carts)
            # print(nextCarts)
            # print(cartLoc)
            c, nextDir = nextCarts.pop(cartLoc, None)
            if c in "<v>^":
                # move and turn cart as necessary
                if c == ">":
                    nextLoc = (cartLoc[0] + 1, cartLoc[1])
                    nextChar = board[nextLoc[1]][nextLoc[0]]
                    if nextCarts.pop(nextLoc, None) is not None:
                        carts = nextCarts
                        break
                    if nextChar == "\\":
                        c = "v"
                    elif nextChar == "/":
                        c = "^"
                    elif nextChar == "+":
                        c, nextDir = intersectionTurn(c, nextDir)
                    nextCarts[nextLoc] = (c, nextDir)
                elif c == "<":
                    nextLoc = (cartLoc[0] - 1, cartLoc[1])
                    nextChar = board[nextLoc[1]][nextLoc[0]]
                    if nextCarts.pop(nextLoc, None) is not None:
                        carts = nextCarts
                        break
                    if nextChar == "\\":
                        c = "^"
                    elif nextChar == "/":
                        c = "v"
                    elif nextChar == "+":
                        c, nextDir = intersectionTurn(c, nextDir)
                    nextCarts[nextLoc] = (c, nextDir)
                elif c == "^":
                    nextLoc = (cartLoc[0], cartLoc[1] - 1)
                    nextChar = board[nextLoc[1]][nextLoc[0]]
                    if nextCarts.pop(nextLoc, None) is not None:
                        carts = nextCarts
                        break
                    if nextChar == "\\":
                        c = "<"
                    elif nextChar == "/":
                        c = ">"
                    elif nextChar == "+":
                        c, nextDir = intersectionTurn(c, nextDir)
                    nextCarts[nextLoc] = (c, nextDir)
                elif c == "v":
                    nextLoc = (cartLoc[0], cartLoc[1] + 1)
                    nextChar = board[nextLoc[1]][nextLoc[0]]
                    if nextCarts.pop(nextLoc, None) is not None:
                        carts = nextCarts
                        break
                    if nextChar == "\\":
                        c = ">"
                    elif nextChar == "/":
                        c = "<"
                    elif nextChar == "+":
                        c, nextDir = intersectionTurn(c, nextDir)
                    nextCarts[nextLoc] = (c, nextDir)
            carts = nextCarts
        # printBoardWithCarts(board, carts)
    print(carts)