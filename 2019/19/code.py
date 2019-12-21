import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from intcode import Intcode

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [ int(num) for num in [ line.split(",") for line in file ][0] ]

def parseInput(lines):
    return [ int(line) for line in str(lines).split(",") ]

def parseLine(line: str):
    return line.strip()

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item,end='')
        print()

###########################
# part1
###########################
def part1(data):
    print(data)

    grid = []
    size = 50
    for j in range(size):
        row = []
        for i in range(size):
            row.append(".")
        grid.append(row)

    intcode_input = [0, 0]
    i = j = 0

    intcoder = Intcode(data, intcode_input, debug=False)
    while intcoder.running:
        # check for outputs
        if len(intcoder.output) >= 1:
            if intcoder.output[0] == 1:
                grid[j][i] = "#"
            intcoder.output = []
            # change inputs, too
            i += 1
            if i == size:
                i = 0
                j += 1
                if j == size:
                    break
            intcode_input = [i, j]
        intcoder.step()
    printGrid(grid)
    count = 0
    for row in grid:
        for item in row:
            if item == "#":
                count += 1

    print("count",count)

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    print("PART 1 TEST DATA")
    # testpart1("1111")
    # testpart1("1234")

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    # print("\nPART 2 RESULT")
    # runpart2()
