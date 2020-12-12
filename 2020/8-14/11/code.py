from copy import deepcopy
from lib.print import print_2d_grid
import numpy as np

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return [ char for char in line.strip() ]


def countAdj(data, i , j):
    item = data[i][j]
    count = 0
    for i2, j2 in ((i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)):
        if 0 <= i2 < len(data) and 0 <= j2 < len(data[0]):
            newitem = data[i2][j2]
            if newitem == "#":
                count += 1
    return count

def doRound(data):
    newdata = deepcopy(data)
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            item = row[j]
            if item == "L":
                if countAdj(data, i, j) == 0:
                    newdata[i][j] = "#"
            elif item == "#":
                if countAdj(data, i, j) >= 4:
                    newdata[i][j] = "L"
    return newdata

# assumes they are the same size
def compareGrids(data1, data2):
    for i in range(len(data1)):
        row = data1[i]
        row2 = data2[i]
        for j in range(len(row)):
            item = row[j]
            item2 = row2[j]
            if item != item2:
                return False
    return True

def countOccupied(data):
    count = 0
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            item = row[j]
            if item == "#":
                count += 1
    return count

###########################
# part1
###########################
def part1(data):
    print_2d_grid(data)
    prev = deepcopy(data)
    i = 0
    while True:
        print("Round", i)
        newdata = doRound(prev)
        if compareGrids(prev, newdata):
            result = countOccupied(newdata)
            print(result)
            return
        prev = deepcopy(newdata)
        i +=1

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################

def countVisible(data, i, j):
    return numAsteriodsDetected(data, i, j)


def numAsteriodsDetected(data, x, y):
    h = len(data[0])
    w = len(data)
    count = 0
    # straight directions
    if y-1 >= 0:
        j = np.linspace(y,0,y+1)
        i = 0*j+x
        count += goDirection(data, i, j, x, y) # up
    if y+1 < h:
        j = np.linspace(y, h-1, h-y)
        i = 0*j+x
        count += goDirection(data, i, j, x, y) # down
    if x-1 >= 0:
        i = np.linspace(x,0,x+1)
        j = 0*i+y
        count += goDirection(data, i, j, x, y) #left
    if x+1 < w:
        i = np.linspace(x,w-1, w-x)
        j = 0*i+y
        count += goDirection(data, i, j, x, y) # right

    # main diagonals
    if y-1 >= 0 and x-1 >= 0:
        j = np.linspace(y,0,y+1)
        i = np.linspace(x,0,x+1)
        slopes = []
        for yslope in range(1, 2):
            for xslope in range(1, 2):
                slopes.append((xslope,yslope))
        for (xslope, yslope) in slopes:
            ys = j[::yslope]
            xs = i[::xslope]
            count += goDirection(data, xs, ys, x, y) # up left
    if y-1 >= 0 and x+1 < w:
        j = np.linspace(y,0,y+1)
        i = np.linspace(x, w-1, w-x)
        for yslope in range(1, 2):
            ys = j[::yslope]
            for xslope in range(1, 2):
                xs = i[::xslope]
                count += goDirection(data, xs, ys, x, y) # up right
    if y+1 < h and x-1 >= 0:
        j = np.linspace(y, h-1, h-y)
        i = np.linspace(x,0,x+1)
        for yslope in range(1, 2):
            ys = j[::yslope]
            for xslope in range(1, 2):
                xs = i[::xslope]
                count += goDirection(data, xs, ys, x, y) # down left
    if y+1 < h and x+1 < w:
        j = np.linspace(y, h-1, h-y)
        i = np.linspace(x, w-1, w-x)
        for yslope in range(1, 2):
            ys = j[::yslope]
            for xslope in range(1, 2):
                xs = i[::xslope]
                count += goDirection(data, xs, ys, x, y) # down right
    return count

def goDirection(data, x, y, startx, starty):
    points = [(int(i),int(j)) for (i,j) in list(zip(x,y))]
    # print(points)
    for (i, j) in points:
        if (i,j) != (startx,starty):
            if 0 <= i < len(data) and 0 <= j < len(data[0]):
                if data[i][j] == '#':
                    return 1
                elif data[i][j] == "L":
                    return 0
    return 0

def doRound2(data):
    newdata = deepcopy(data)
    for i in range(len(data)):
        row = data[i]
        for j in range(len(row)):
            # print(i,j)
            item = row[j]
            if item == "L":
                if countVisible(data, i, j) == 0:
                    newdata[i][j] = "#"
            elif item == "#":
                if countVisible(data, i, j) >= 5:
                    newdata[i][j] = "L"
    return newdata


def part2(data):
    # print_2d_grid(data)
    prev = deepcopy(data)
    i = 0
    # while i < 1:
    while True:
        print("Round", i)
        newdata = doRound2(prev)
        # print_2d_grid(newdata)
        if compareGrids(prev, newdata):
            result = countOccupied(newdata)
            print(result)
            return
        prev = deepcopy(newdata)
        i +=1
    # print(len(data[0]),len(data))

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
