from copy import deepcopy
import numpy as np
from lib.print import print_2d_grid
import time

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [ [ c for c in line.strip() ] for line in file ]

def countAdjSet(occupied, i , j):
    count = 0
    for i2, j2 in ((i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)):
        if (i2, j2) in occupied:
            count += 1
    return count

def doRound(data, occupied, rows, cols):
    newdata = [[ item for item in row ] for row in data]
    for j in range(rows):
        row = data[j]
        newrow = newdata[j]
        for i in range(cols):
            item = row[i]
            if item == ".": # quicker out
                continue
            numAdj = countAdjSet(occupied, i, j)
            if item == "L":
                if numAdj == 0:
                   newrow[i] = "#"
            elif item == "#":
                if numAdj >= 4:
                    newrow[i] = "L"
    return newdata

# assumes they are the same size
def compareGrids(data1, data2, rows, cols):
    for j in range(rows):
        row = data1[j]
        row2 = data2[j]
        for i in range(cols):
            item = row[i]
            item2 = row2[i]
            if item != item2:
                return False
    return True

def getOccupied(data, rows, cols):
    occupied = set()
    for j in range(rows):
        row = data[j]
        for i in range(cols):
            item = row[i]
            if item == "#":
                occupied.add(tuple([i,j]))
    return occupied

###########################
# part1
###########################
def part1(data):
    prev = data
    rows = len(data)
    cols = len(data[0])
    occupied = set()
    i = 0
    while True:
        # print("Round", i)
        newdata = doRound(prev, occupied, rows, cols)
        occupied = getOccupied(newdata, rows, cols)
        if compareGrids(prev, newdata, rows, cols):
            print(len(occupied))
            return
        prev = newdata
        i +=1

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################

def countVisible(data, x, y, h, w):
    count = 0
    # down
    count += goDirectionSet(data, [(x, y2) for y2 in range(y + 1, h, 1)])
    # up
    count += goDirectionSet(data, [(x, y2) for y2 in range(y - 1, -1, -1)])
    # left
    count += goDirectionSet(data, [(x2, y) for x2 in range(x - 1, -1, -1)])
    # right
    count += goDirectionSet(data, [(x2, y) for x2 in range(x + 1, w, 1)])
    # down right
    count += goDirectionSet(data, [(x2, y2) for (x2, y2) in zip(range(x + 1, w, 1), range(y + 1, h, 1))])
    # up right
    count += goDirectionSet(data, [(x2, y2) for (x2, y2) in zip(range(x - 1, -1, -1), range(y + 1, h, 1))])
    # down left
    count += goDirectionSet(data, [(x2, y2) for (x2, y2) in zip(range(x + 1, w, 1), range(y - 1, -1, -1))])
    # down left
    count += goDirectionSet(data, [(x2, y2) for (x2, y2) in zip(range(x - 1, -1, -1), range(y - 1, -1, -1))])

    return count

def goDirectionSet(data, points):
    for (i, j) in points:
        if data[j][i] == '#':
            return 1
        elif data[j][i] == "L":
            return 0
    return 0

def doRound2(data, rows, cols):
    newdata = [[ item for item in row ] for row in data]
    for j in range(rows):
        row = data[j]
        newrow = newdata[j]
        for i in range(cols):
            item = row[i]
            if item == ".": # quicker out
                continue
            numVisible = countVisible(data, i, j, rows, cols)
            if item == "L":
                if numVisible == 0:
                    newrow[i] = "#"
            elif item == "#":
                if numVisible >= 5:
                    newrow[i] = "L"
    return newdata

def part2(data):
    prev = data
    rows = len(data)
    cols = len(data[0])
    i = 0
    while True:
        # print("Round", i)
        newdata = doRound2(prev, rows, cols)
        if compareGrids(prev, newdata, rows, cols):
            print(len(getOccupied(newdata, rows, cols)))
            return
        prev = newdata
        i +=1

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
