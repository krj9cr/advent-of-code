import time
from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file][0]

def parseLine(line: str):
    return [ int(s) for s in line.strip() ]

def getLabelsAfterOne(cups):
    idx = cups.index(1)
    after = cups[idx+1:]
    before = cups[:idx]
    l = after + before
    return "".join([ str(i) for i in l ])

def move(cups):
    minCup = min(cups)

    # print("cups:", cups)
    currentCup = cups[0]
    pickup = cups[1:4]
    # print("pickup:" ,pickup)
    newCups = cups[4:]

    # destination cup: the cup with a label equal to the current cup's label minus one
    destinationCup = currentCup - 1
    # If this would select one of the cups that was just picked up,
    # the crab will keep subtracting one until it finds a cup that wasn't just picked up
    while destinationCup in pickup:
        destinationCup -= 1
    # If at any point in this process the value goes below the lowest value on any cup's label,
    # it wraps around to the highest value on any cup's label instead
    if destinationCup < minCup:
        destinationCup = max(newCups)
    # print("desination:",destinationCup)

    destinationIdx = newCups.index(destinationCup)
    for i in range(len(pickup)):
        newCups.insert(destinationIdx+i+1, pickup[i])

    newCups.append(currentCup)

    # print("newcups", newCups)
    return newCups

###########################
# part1
###########################
def part1(data):
    cups = deepcopy(data)

    numMoves = 100
    for i in range(numMoves):
        print("move ", i)
        cups = move(cups)
        print()

    print("Final cups", cups)
    res = getLabelsAfterOne(cups)
    print("result", res)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def getTwoCupsAfterOne(cups):
    idx = cups.index(1)
    one = cups[idx+1]
    two = cups[idx+2]
    print(one, "and", two)
    return one * two

def part2(data):
    print(data)
    m = max(data)
    cups = data[:] + [ i for i in range(m+1, 1000000+1)]

    numMoves = 10
    for i in range(numMoves):
        # print("move ", i)
        cups = move(cups)
        # print()

    print("Final cups", cups)
    res = getTwoCupsAfterOne(cups)
    print("result", res)

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
