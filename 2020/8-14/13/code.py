import time
import sys
from math import gcd # Python versions 3.5 and above
from functools import reduce # Python version 3.x
import signal

interrupted = False

def signal_handler(signum, frame):
    global interrupted
    interrupted = True

signal.signal(signal.SIGINT, signal_handler)

def lcm(denominators):
    return reduce(lambda a,b: a*b // gcd(a,b), denominators)

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        lines = [parseLine(line) for line in file]
        return int(lines[0]), lines[1].split(",")

def parseLine(line: str):
    return line.strip()

###########################
# part1
###########################
def part1(data):
    print(data)
    earliest, buses = data
    buses = [ int(b) for b in buses if b != "x"]
    print(buses)

    mindiff = sys.maxsize
    for b in buses:
        find = 0
        while find < earliest:
            find += b
        diff = find - earliest
        if diff < mindiff:
            print(diff, b)
            mindiff = diff
            minbus = b
            print(diff*b)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################

# Function to calculate
# the smallest multiple of x closest to n
def closestMultiple(n, x):
    if x > n:
        return x
    z = int(x / 2)
    n = n + z
    n = n - (n % x)
    return n

def checkEarliest(buses, earliest):
    l = []
    for busId, offset in buses:
        if (earliest + offset) % busId != 0:
            return False, l
        else:
            l.append(busId)
    return True, l

def part2(data):
    _, buses = data
    buses = [ (int(buses[i]), i) for i in range(len(buses)) if buses[i] != "x"]
    buses.sort(reverse=True)
    print(buses)

    hh = max([ b[0] for b in buses ])
    hhoffset = None
    for busId, offset in buses:
        if busId == hh:
            hhoffset = offset

    start = closestMultiple(100000000000000, hh)-hhoffset
    while True:
        if interrupted:
            print(start)
            sys.exit()
        # print("start", start) # printing this slows things down a lot
        done, solved = checkEarliest(buses, start)
        # print(solved)
        if done:
            print("DONE", start)
            return
        prod = 1
        for s in solved:
            prod *= s
        start += prod

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
