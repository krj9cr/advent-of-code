import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from intcode import Intcode

from copy import deepcopy

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

def drawPoints(points):
    size = 0
    for x, y in points:
        size = max(size, x, y)
    for j in range(size):
        for i in range(size):
            if (i,j) in points:
                print("#",end="")
            else:
                print(".",end="")
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

    for j in range(size):
        for i in range(size):
            print("inputs",i,j)
            # in this problem, the intcoder only runs once for each input
            intcoder = Intcode(deepcopy(data), [i, j], debug=False)
            intcoder.run()
            print("output",intcoder.output)
            if intcoder.output[0] == 1:
                grid[j][i] = "#"

    printGrid(grid)
    count = 0
    for row in grid:
        for item in row:
            if item == "#":
                count += 1

    print("count",count)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)

    points = []
    size = 50

    x = y = 1
    upperslope = 1.7
    lowerslope = 2

    first = last = 0

    for k in range(size):
        x2 = list(range(int(x*upperslope), int(x*lowerslope)+1))
        # y2 = list(range(int(y*upperslope), int(y*lowerslope)+1))
        j = y
        for i in x2:
            print("inputs",i,j)
            # in this problem, the intcoder only runs once for each input
            intcoder = Intcode(deepcopy(data), [i, j], debug=False)
            intcoder.run()
            if intcoder.output[0] == 1:
                points.append((i,j))
        x +=1
        y +=1

    drawPoints(points)
    print("points",points)
    print("count",len(points))

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
