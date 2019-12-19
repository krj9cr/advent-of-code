import copy
import numpy as np
import math

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

    # count remaining asteroids
    count = 0
    for j in range(0, len(data)):
        for i in range(0, len(data[0])):
            if i >= 0 and i < len(data[0]) and j >= 0 and j < len(data):
                if (i,j) != (x,y) and data[j][i] == '#':
                    count += 1
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
def clockwiseangle_and_distance(point, origin, refvec=[0,1]):
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    return angle, lenvector

def part2(data):
    print(data)
    spot = part1(data)
    print("part1 spot", spot)
    asteroids = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            char = data[y][x]
            if char == '#' and (x,y) != spot:
                angle, l = clockwiseangle_and_distance((x, y), spot)
                asteroids.append((x,y,angle,l))
    asteroids = sorted(asteroids, key=lambda x: x[3])
    asteroids = sorted(asteroids, key=lambda x: -x[2])
    print(asteroids)
    wow = asteroids
    wow = [asteroids[0]]
    lastangle = asteroids[0][2]
    asteroids = asteroids[1:]
    # do loops around to do each angle once
    while len(wow) < 200:
        for asteroid in asteroids:
            if asteroid[2] == lastangle or asteroid in wow:
                continue
            else:
                wow.append(asteroid)
                lastangle = asteroid[2]
    print(wow)
    print(wow[198:201])
    asteroid = wow[199]
    print(asteroid)
    print("answer", (asteroid[0] * 100) + asteroid[1])


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
