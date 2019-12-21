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

def asciiToGrid(ascii):
    grid = []
    row = []
    for a in ascii:
        if a == 10 and len(row) > 0:
            grid.append(row[:])
            row = []
        else:
            row.append(str(chr(a)))
    return grid

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item,end="")
        print()

def findIntersections(grid):
    intersections = []
    print("len grid",len(grid))
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                isIntersection = True
                for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                    if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                        if grid[y2][x2] != "#":
                            isIntersection = False
                            break
                    else:
                        isIntersection = False
                if isIntersection:
                    intersections.append((x, y))
    return intersections


###########################
# part1
###########################
def part1(data):
    print(data)

    intcode_input = []
    intcoder = Intcode(data, intcode_input, extra_mem=10000, debug=False)
    intcoder.run()
    output = intcoder.output
    print(output)
    grid = asciiToGrid(output)
    printGrid(grid)
    intersections = findIntersections(grid)
    print("intersections:",intersections)
    total = 0
    for (x, y) in intersections:
        total += x * y
    print("total", total)

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

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    # print("\nPART 2 RESULT")
    # runpart2()