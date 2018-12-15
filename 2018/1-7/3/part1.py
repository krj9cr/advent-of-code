import sys

if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " <input>"
    exit(1)

input = sys.argv[1]


def parseUgly(str):
    split = str.strip().split(" ")
    id = split[0].strip("#")
    right, top = split[2].strip(":").split(",")
    width, height = split[3].split("x")
    tuple = [id, right, top, width, height]
    return map(lambda x: int(x), tuple)

def printBoard(board):
    for i in range(0, boardHeight):
        for j in range(0, boardWidth):
            print board[i][j],
        print ""

with open(input, 'r') as file:
    lines = {}
    maxRight = 0
    maxTop = 0
    maxWidth = 0
    maxHeight = 0
    # parse file
    for line in file:
        # parse each line
        # example: #1 @ 1,3: 4x4
        parsedLine = parseUgly(line)
        # find max sizes
        if parsedLine[1] > maxRight:
            maxRight = parsedLine[1]
        if parsedLine[2] > maxTop:
            maxTop = parsedLine[2]
        if parsedLine[3] > maxWidth:
            maxWidth = parsedLine[3]
        if parsedLine[4] > maxHeight:
            maxHeight = parsedLine[4]
        lines[parsedLine[0]] = parsedLine[1:]
    # print lines

    # Init board
    boardWidth = maxRight + maxWidth
    boardHeight = maxTop + maxHeight
    print boardWidth, boardHeight
    board = []
    for i in range(0, boardHeight):
        row = []
        for j in range(0, boardWidth):
            row.append(0)
        board.append(row)

    # Add data to board
    for line in lines.values():
        startj = line[0]
        starti = line[1]
        # assuming we don't start out of bounds
        for i in range(0, line[3]):  # height - by row first
            for j in range(0, line[2]):  # width - by column next
                newi= i + starti
                newj = j + startj
                # increment by 1
                board[i+starti][j+startj] += 1

    # printBoard(board)

    # Count board values > 2
    count = 0
    for i in range(0, boardHeight):
        for j in range(0, boardWidth):
            if board[i][j] >= 2:
                count += 1

    print count
