import time
import numpy as np
import math

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    l = line.strip()
    return l[0], int(l[1:])

def manhattan(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1])

###########################
# part1
###########################
def part1(data):
    print(data)
    x = 0
    y = 0
    curr_dir = 90
    for action, amount in data:
        if action == "N":
            y += amount
        elif action == "S":
            y -= amount
        elif action == "E":
            x += amount
        elif action == "W":
            x -= amount
        elif action == "L":
            curr_dir -= amount
            curr_dir %= 360
        elif action == "R":
            curr_dir += amount
            curr_dir %= 360
        elif action == "F":
            if curr_dir == 0:
                y += amount
            elif curr_dir == 180:
                y -= amount
            elif curr_dir == 90:
                x += amount
            elif curr_dir == 270:
                x -= amount
        else:
            print("unknown action")
            return
        print(action, amount, "at", x,y, "facing", curr_dir)
    print(manhattan((0,0), (x,y)))

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return round(x), round(y)

def rotate(x ,y, degrees):
    rho, phi = cart2pol(x, y)
    pdegrees = phi * (180.0/math.pi)
    pdegrees += degrees
    newphi = pdegrees * (math.pi/180.0)
    return pol2cart(rho, newphi)

def part2(data):
    print(data)
    x = 0
    y = 0
    wx = 10
    wy = 1
    for action, amount in data:
        if action == "N":
            wy += amount
        elif action == "S":
            wy -= amount
        elif action == "E":
            wx += amount
        elif action == "W":
            wx -= amount
        elif action == "L":
            wx, wy = rotate(wx, wy, amount)
        elif action == "R":
            wx, wy = rotate(wx, wy, -amount)
        elif action == "F":
            x += (amount * wx)
            y += (amount * wy)
        else:
            print("unknown action")
            return
        print(action, amount, "ship at", x,y, "waypoint at ", wx,wy)
    print(manhattan((0,0), (x,y)))

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
