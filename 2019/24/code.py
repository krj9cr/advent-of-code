from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return [char for char in line.strip()]

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

def countAdjType(board, x, y, target="#"):
    count = 0
    for x2, y2 in ((x, y-1), (x-1, y), (x+1, y), (x, y+1)):
        if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] == target:
            count += 1
    return count

def oneMinute(board):
    nextBoard = deepcopy(board)
    for y in range(0,len(board)):
        row = board[y]
        for x in range(0, len(row)):
            item = row[x]
            # bug
            if item == "#":
                numBugs = countAdjType(board,x,y)
                if numBugs != 1:
                    nextBoard[y][x] = "."
            elif item == ".":
                numBugs = countAdjType(board,x,y)
                if numBugs == 1 or numBugs == 2:
                    nextBoard[y][x] = "#"
    return nextBoard

def calcBio(board):
    total = 0
    for y in range(0,len(board)):
        row = board[y]
        for x in range(0, len(row)):
            item = row[x]
            if item == "#":
                pow = 2 ** (x + (len(row)*y))
                print("adding",x,y,"as",pow)
                total += pow
    return total


###########################
# part1
###########################
def part1(board):
    printGrid(board)
    prevBoards = [deepcopy(board)]
    numIters = 1
    while True:
        board = oneMinute(board)
        # check previous boards
        for prevBoard in prevBoards:
            if board == prevBoard:
                print("SAME")
                printGrid(board)
                print("answer:",calcBio(board))
                exit(0)
        print(numIters)
        numIters += 1
        printGrid(board)
        print("")
        prevBoards.append(deepcopy(board))

# 2097128 too low
# 18401265 answer for someone else...
# 32573535
# 36802530 too high
# 65147070 too high

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\nPART 2 RESULT")
    # runpart2()
