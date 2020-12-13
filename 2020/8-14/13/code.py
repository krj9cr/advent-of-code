import time
import sys
from math import gcd # Python versions 3.5 and above
#from fractions import gcd # Python versions below 3.5
from functools import reduce # Python version 3.x

def lcm(denominators):
    return reduce(lambda a,b: a*b // gcd(a,b), denominators)


def valid_answer(n, mod, answer):
    return (n+answer)%mod == 0

# Source: https://github.com/kresimir-lukin/AdventOfCode2020/blob/main/helpers.py
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

# Source: https://github.com/kresimir-lukin/AdventOfCode2020/blob/main/helpers.py
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


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
    minbus = None
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

def findEarliest(buses, earliest):
    res = {}
    for b in buses:
        if b != 'x':
            b = int(b)
            find = closestMultiple(earliest, b)
            if find < earliest:
                find += b
            res[b] = find
    return res

def checkOrder(buses, f):
    start = f[int(buses[0])]
    for i in range(1, len(buses)):
        b = buses[i]
        if b != 'x':
            b = int(b)
            btime = f[b]
            if btime - start != i:
                return False
            # else:
            #     print(b, btime, start, i)
    return True

# Function to calculate
# the smallest multiple of x closest to n
def closestMultiple(n, x):
    if x > n:
        return x
    z = int(x / 2)
    n = n + z
    n = n - (n % x)
    return n

# def part2(data):
#     _, buses = data
#     buses = [ (int(buses[i]), int(buses[i])-i) for i in range(len(buses)) if buses[i] != "x" ]
#     offsets = [ b[1] for b in buses ]
#     buses = [ b[0] for b in buses]
#     print(buses, offsets)
#     print(chinese_remainder(buses, offsets))

def checkEarliest(buses, earliest):
    for busId, offset in buses:
        n = (earliest + offset) / busId
        if not n.is_integer():
            return False
    return True

def part2(data):
    _, buses = data
    buses = [ (int(buses[i]), i) for i in range(len(buses)) if buses[i] != "x"]
    print(buses)

    hh = max([ b[0] for b in buses ])
    hhoffset = None
    for busId, offset in buses:
        if busId == hh:
            hhoffset = offset

    start = closestMultiple(100000000000000, hh)-hhoffset
    # start = hh - hhoffset
    while True:
        # print("start", start) # printing this slows things down a lot
        if checkEarliest(buses, start):
            print("DONE", start)
            return
        start += hh

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
