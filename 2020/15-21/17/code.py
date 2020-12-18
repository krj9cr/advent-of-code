import time
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
    return [c for c in line.strip()]

def printLayers3d(layers):
    for i in sorted(layers.keys()):
        print("Layer",i)
        print_2d_grid(layers[i])

def printLayers4d(fourth):
    for w in sorted(fourth.keys()):
        layers = fourth[w]
        for z in sorted(layers.keys()):
            print("z=",z,", w=",w)
            print_2d_grid(layers[z])

def countBugs2d(layer):
    total = 0
    for row in layer:
        for item in row:
            if item == "#":
                total += 1
    return total

def countBugs3d(layers):
    total = 0
    for i in layers:
        total += countBugs2d(layers[i])
    return total

def findAdj3d(x, y, z):
    adjacent = []

    for x2 in (x, x-1, x+1):
        for y2 in (y, y-1,y+1):
            for z2 in (z, z-1, z+1):
                if (x2,y2,z2) != (x,y,z):
                    adjacent.append(tuple([x2, y2, z2]))
    return adjacent

def countAdjType3d(layers, x, y, z):
    adjacent = findAdj3d(x, y, z)
    count = 0
    for x2, y2, z2 in adjacent:
        try:
            if layers[z2][y2][x2] == "#":
                count += 1
        except Exception:
            pass
    return count


def findAdj4d(x, y, z, w):
    adjacent = []

    for x2 in (x, x-1, x+1):
        for y2 in (y, y-1,y+1):
            for z2 in (z, z-1, z+1):
                for w2 in (w, w-1, w+1):
                    if (x2,y2,z2,w2) != (x,y,z,w):
                        adjacent.append(tuple([x2, y2, z2, w2]))
    return adjacent

def countAdjType4d(layers, x, y, z, w):
    adjacent = findAdj4d(x, y, z, w)
    count = 0
    for x2, y2, z2, w2 in adjacent:
        try:
        # if w2 == -2:
        #     print(x,y,z,w)
        #     print(adjacent)
        # fourth = layers[w2]
        # third = fourth[z2]
        # second = third[y2]
        # first = second[x2]
            if layers[w2][z2][y2][x2] == "#":
                count += 1
        except Exception:
            pass
    return count

def oneMinute3d(layers):
    nextLayers = {}
    for i in layers:
        board = layers[i]
        nextBoard = deepcopy(board)
        for y in range(0,len(board)):
            row = board[y]
            for x in range(0, len(row)):
                item = row[x]
                # bug
                if item == "#":
                    numBugs = countAdjType3d(layers,x,y,i)
                    if numBugs == 2 or numBugs == 3:
                        nextBoard[y][x] = "#"
                    else:
                        nextBoard[y][x] = "."
                else:
                    numBugs = countAdjType3d(layers,x,y,i)
                    if numBugs == 3:
                        nextBoard[y][x] = "#"
                    else:
                        nextBoard[y][x] = "."
        nextLayers[i] = nextBoard
    return nextLayers

def padLayers3d(layers):
    # pad layers
    for z in layers:
        board = layers[z]
        layers[z] = padBoard2d(layers[z])

def padBoard2d(board):
    return np.pad(board, [1, 1], mode='constant', constant_values='.')

def getEmptyLayer2d(w, h):
    board = []
    for y in range(w):
        row = []
        for x in range(h):
            row.append(".")
        board.append(row)
    return board

def getEmptyLayer3d(w,h):
    layers = {
        -1: getEmptyLayer2d(h, w),
        0: getEmptyLayer2d(h, w),
        1: getEmptyLayer2d(h, w),
    }
    return layers

###########################
# part1
###########################
def part1(data):
    print(data)

    # keep track of layers in a dict
    # initialize with layer 0, and an empty top and bottom layer
    layers = {
        -1: getEmptyLayer2d(len(data), len(data[0])),
        0: deepcopy(data),
        1: getEmptyLayer2d(len(data), len(data[0])),
    }
    padLayers3d(layers)
    printLayers3d(layers)

    # pass time
    for t in range(1, 7):
        # pass a minute
        layers = oneMinute3d(layers)

        sortedLayers = sorted(layers.keys())

        # if the lowest layer has a bug, add another empty layer on bottom
        lowestLayer = sortedLayers[0]
        lowestCount = countBugs2d(layers[lowestLayer])
        if lowestCount > 0:
            layers[lowestLayer-1] = getEmptyLayer2d(len(layers[lowestLayer]), len(layers[lowestLayer][0]))

        # if the highest layer has a bug, add another empty layer on top
        highestLayer = sortedLayers[-1]
        highestCount = countBugs2d(layers[highestLayer])
        if highestCount > 0:
            layers[highestLayer+1] = getEmptyLayer2d(len(layers[highestLayer]), len(layers[highestLayer][0]))

        padLayers3d(layers)

        print("Time",t)
        printLayers3d(layers)

    # count the number of bugs in all layers
    totalBugs = 0
    for i in layers:
        totalBugs += countBugs2d(layers[i])
    print("Total bugs:",totalBugs)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def part2(data):
    print(data)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\nPART 2 RESULT")
    # runpart2()
