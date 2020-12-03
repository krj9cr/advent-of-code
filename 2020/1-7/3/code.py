

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseFile(path: str):
    with open(path, 'r') as file:
        return parseInput(file)

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return line.strip()

###########################
# part1
###########################
def part1(data):
    print(data)
    slope = (3,1)
    print(checkSlope(slope, data))


def checkSlope(slope, data):
    slopeRight, slopeDown = slope
    numRows = len(data)
    numCols = len(data[0])
    print(numRows, "x", numCols)
    currRow = 0
    currCol = 0
    numTrees = 0
    while currRow < numRows:
        # print(currRow, currCol)
        if data[currRow][currCol] == '#':
            numTrees += 1
        currRow += slopeDown
        currCol = (currCol + slopeRight) % numCols
    return numTrees

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):

    answers = (checkSlope((1,1), data), checkSlope((3,1), data), checkSlope((5,1), data), checkSlope((7,1), data), checkSlope((1,2), data))
    print(answers)

    result = 1
    for a in answers:
        result *= a
    print(result)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()


    print("\nPART 2 RESULT")
    runpart2()
