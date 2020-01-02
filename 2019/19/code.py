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
    i = j = 10
    points = []

    while True:
        # zig zag down the bottom line
        print("inputs",i,j)
        # in this problem, the intcoder only runs once for each input
        intcoder = Intcode(deepcopy(data), [i, j], debug=False)
        intcoder.run()
        print("output",intcoder.output)
        # down if it's a spot, right if not
        if intcoder.output[0] == 1:
            points.append((i,j))
            # if it's a spot, check the upper right corner
            x = i + 99
            y = j - 99
            if y >= 0:
                print("checking upper corner",x,y)
                intcoder = Intcode(deepcopy(data), [x, y], debug=False)
                intcoder.run()
                if intcoder.output[0] == 1:
                    # we good
                    points.append((x,y))
                    # drawPoints(points)
                    # take the upper left corner
                    # x * 10000 + y
                    points.append((i,y))
                    print("answer:",i*10000 + y)

                    exit(0)
            # go down
            j += 1
        else:
            # go right
            i += 1

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
