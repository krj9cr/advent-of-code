import copy
import numpy as np

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
    return [char for char in line.strip()]

def printField(data,x,y):
    for j in range(0, len(data)):
        for i in range(0, len(data[0])):
            if (i,j) == (x,y):
                print('O',end='')
            else:
                print(data[j][i],end='')
        print()

def numAsteriodsDetected(data, x, y):
    w = len(data[0])
    h = len(data)
    # straight directions
    if y-2 >= 0:
        j = np.linspace(y,0,y+1)
        i = 0*j+x
        goDirection(data, i, j, x, y) # up
    if y+2 < h:
        j = np.linspace(y, h-1, h-y)
        i = 0*j+x
        goDirection(data, i, j, x, y) # down
    if x-2 >= 0:
        i = np.linspace(x,0,x+1)
        j = 0*i+y
        goDirection(data, i, j, x, y) #left
    if x+2 < w:
        i = np.linspace(x,w-1, w-x)
        j = 0*i+y
        goDirection(data, i, j, x, y) # right

    # main diagonals
    if y-2 >= 0 and x-2 >= 0:
        j = np.linspace(y,0,y+1)
        i = np.linspace(x,0,x+1)
        slopes = []
        for yslope in range(1, int(h/2)+1):
            for xslope in range(1, int(w/2)+1):
                slopes.append((xslope,yslope))
        for (xslope, yslope) in slopes:
            ys = j[::yslope]
            xs = i[::xslope]
            goDirection(data, xs, ys, x, y) # up left
    if y-2 >= 0 and x+2 < w:
        j = np.linspace(y,0,y+1)
        i = np.linspace(x, w-1, w-x)
        for yslope in range(1, int(h/2)+1):
            ys = j[::yslope]
            for xslope in range(1, int(w/2)+1):
                xs = i[::xslope]
                goDirection(data, xs, ys, x, y) # up right
    if y+2 < h and x-2 >= 0:
        j = np.linspace(y, h-1, h-y)
        i = np.linspace(x,0,x+1)
        for yslope in range(1, int(h/2)+1):
            ys = j[::yslope]
            for xslope in range(1, int(w/2)+1):
                xs = i[::xslope]
                goDirection(data, xs, ys, x, y) # down left
    if y+2 < h and x+2 < w:
        j = np.linspace(y, h-1, h-y)
        i = np.linspace(x, w-1, w-x)
        for yslope in range(1, int(h/2)+1):
            ys = j[::yslope]
            for xslope in range(1, int(w/2)+1):
                xs = i[::xslope]
                goDirection(data, xs, ys, x, y) # down right

    # printField(data,x,y)

    # count remaining asteroids
    count = 0
    for j in range(0, len(data)):
        for i in range(0, len(data[0])):
            if i >= 0 and i < len(data[0]) and j >= 0 and j < len(data):
                if (i,j) != (x,y) and data[j][i] == '#':
                    count += 1
    # print("count for",(x,y)," is",count)
    return count

def goDirection(data, x, y, startx, starty):
    seen = False
    points = [(int(i),int(j)) for (i,j) in list(zip(x,y))]
    if len(points) > 1:
        # print(points)
        for (i, j) in points:
            if (i,j) != (startx,starty):
                if i >= 0 and i < len(data[0]) and j >= 0 and j < len(data):
                    if data[j][i] == '#':
                        if seen:
                            data[j][i] = 'X'
                        else:
                            seen = True

###########################
# part1
###########################
def part1(data):
    # print(data)
    maxx = len(data[0])
    maxy = len(data)
    bestNum = 0
    bestPos = (0,0)
    for y in range(0, maxy):
        for x in range(0, maxx):
            if data[y][x] == '#':
                numAsteroids = numAsteriodsDetected(copy.deepcopy(data), x, y)
                # print(x,y, numAsteroids)
                if numAsteroids > bestNum:
                    bestNum = numAsteroids
                    bestPos = (x, y)
    print("Best is", bestPos, "with", bestNum, "other asteroids detected")
    return bestPos

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def goDirection2(data, x, y, startx, starty, count):
    points = [(int(i),int(j)) for (i,j) in list(zip(x,y))]
    if len(points) > 1:
        for (i, j) in points:
            if (i,j) != (startx,starty):
                if i >= 0 and i < len(data[0]) and j >= 0 and j < len(data):
                    if data[j][i] == '#':
                        data[j][i] = count
                        count += 1
                        print(i,j,count)
                        if count == 200:
                            print("200!!!", (i,j))
                            exit(0)
                        return count
    return count

def rotation(data, x, y, count):
    w = len(data[0])
    h = len(data)

    slopes = []
    # for xslope in range(1, w):
    #     for yslope in range(h, 0, -1):
    #         slopes.append((xslope, yslope))

    for yslope in range(1, h):
        for xslope in range(1, w):
            slopes.append((xslope, yslope))

    if y - 2 >= 0:
        j = np.linspace(y, 0, y + 1)
        i = 0 * j + x
        count = goDirection2(data, i, j, x, y, count)  # up
    if y - 2 >= 0 and x + 2 < w:
        j = np.linspace(y, 0, y + 1)
        i = np.linspace(x, w - 1, w - x)
        slopes = sorted(slopes, key=lambda k: np.arctan2(k[0], k[1]))
        print("slopes:", slopes)
        for (xslope, yslope) in slopes:
            ys = j[::yslope]
            xs = i[::xslope]
            count = goDirection2(data, xs, ys, x, y, count)  # up right
    if x + 2 < w:
        i = np.linspace(x, w - 1, w - x)
        j = 0 * i + y
        count = goDirection2(data, i, j, x, y, count)  # right
    if y + 2 < h and x + 2 < w:
        j = np.linspace(y, h - 1, h - y)
        i = np.linspace(x, w - 1, w - x)
        slopes = sorted(slopes, key=lambda k: np.arctan2(k[0], k[1]))
        print("slopes:", slopes)
        for (xslope, yslope) in slopes:
            ys = j[::yslope]
            xs = i[::xslope]
            count = goDirection2(data, xs, ys, x, y, count)  # down right
    if y + 2 < h:
        j = np.linspace(y, h - 1, h - y)
        i = 0 * j + x
        count = goDirection2(data, i, j, x, y, count)  # down
    if y + 2 < h and x - 2 >= 0:
        j = np.linspace(y, h - 1, h - y)
        i = np.linspace(x, 0, x + 1)
        slopes = sorted(slopes, key=lambda k: np.arctan2(k[0], k[1]))
        print("slopes:", slopes)
        for (xslope, yslope) in slopes:
            ys = j[::yslope]
            xs = i[::xslope]
            count = goDirection2(data, xs, ys, x, y, count)  # down left
    if x - 2 >= 0:
        i = np.linspace(x, 0, x + 1)
        j = 0 * i + y
        count = goDirection2(data, i, j, x, y, count)  # left
    if y - 2 >= 0 and x - 2 >= 0:
        j = np.linspace(y, 0, y + 1)
        i = np.linspace(x, 0, x + 1)
        slopes = sorted(slopes, key=lambda k: np.arctan2(k[0], k[1]))
        print("slopes:", slopes)
        for (xslope, yslope) in slopes:
            ys = j[::yslope]
            xs = i[::xslope]
            count = goDirection2(data, xs, ys, x, y, count)  # up left
    printField(data, x, y)
    return count

def part2(data):
    bestPos = part1(data)
    count = 1

    while True:
        count = rotation(data, bestPos[0], bestPos[1], count)
        printField(data,bestPos[0],bestPos[1])

def runpart2():
    part2(parseInputFile())

# 1600 TOO LOW
# 1709 too high

###########################
# run
###########################
if __name__ == '__main__':
    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
