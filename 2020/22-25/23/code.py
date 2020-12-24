import time
from copy import deepcopy
from collections import deque

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file][0]

def parseLine(line: str):
    return [ int(s) for s in line.strip() ]

def getLabelsAfterOne(cups):
    cups = list(cups)
    idx = cups.index(1)
    after = cups[idx+1:]
    before = cups[:idx]
    l = after + before
    return "".join([ str(i) for i in l ])

def move(cups, lenCups):
    minCup = 1
    maxCup = lenCups

    # print("cups:", cups)
    currentCup = cups.popleft()
    pickup = [cups.popleft(), cups.popleft(), cups.popleft()]

    # destination cup: the cup with a label equal to the current cup's label minus one
    destinationCup = currentCup - 1
    # If this would select one of the cups that was just picked up,
    # the crab will keep subtracting one until it finds a cup that wasn't just picked up
    while destinationCup in pickup:
        destinationCup -= 1
    # If at any point in this process the value goes below the lowest value on any cup's label,
    # it wraps around to the highest value on any cup's label instead
    if destinationCup < minCup:
        destinationCup = maxCup

    try:
        destinationIdx = cups.index(destinationCup)
    except:
        destinationCup = max(cups)
        destinationIdx = cups.index(destinationCup)
        pass

    for i in range(len(pickup)):
        cups.insert(destinationIdx+i+1, pickup[i])

    cups.append(currentCup)

    return cups

###########################
# part1
###########################
def part1(data):
    # cups = deepcopy(data)
    #
    # numMoves = 100
    # for i in range(numMoves):
    #     print("move ", i)
    #     cups = move(cups)
    #     print()
    #
    # print("Final cups", cups)
    # res = getLabelsAfterOne(cups)
    # print("result", res)
    numCups = len(data)
    cups = deque(data)

    currentCup = data[0]

    numMoves = 100
    for i in range(numMoves):
        # print("move ", i)
        cups = move(cups, numCups)#, currentCup, numCups)
        # print()

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


def moveWithIndexes(cups, currentCup, cupsLen):
    minCup = 1
    maxCup = cupsLen-1 #1000000

    print("cups:", cups)
    currentCupIdx = cups[currentCup]
    pickup = [cups[currentCupIdx+1], cups[currentCupIdx+2], cups[currentCupIdx+3]]
    nextCurrentCup = cups[currentCupIdx+4]
    print("pickup:" ,pickup)
    # newCups = cups[4:]

    # destination cup: the cup with a label equal to the current cup's label minus one
    destinationCup = currentCup - 1
    # If this would select one of the cups that was just picked up,
    # the crab will keep subtracting one until it finds a cup that wasn't just picked up
    while destinationCup in pickup:
        destinationCup -= 1
    # If at any point in this process the value goes below the lowest value on any cup's label,
    # it wraps around to the highest value on any cup's label instead
    if destinationCup < minCup:
        destinationCup = maxCup
    print("desination:",destinationCup)

    # find index of destination
    destinationIdx = cups[destinationCup]
    for i in range(len(pickup)):
        cups[pickup[i]] = destinationIdx + i + 1
    # for everything after, update their places

    print("cups", cups)
    return cups, nextCurrentCup

def part2(data):
    print(data)
    m = max(data)
    numCups = len(data)
    cups = deque(data[:] + [ i for i in range(m+1, 1000000+1)])

    currentCup = data[0]

    numMoves = 100
    for i in range(numMoves):
        # print("move ", i)
        cups = move(cups, numCups)#, currentCup, numCups)
        # print()

    print("Final cups", cups)
    res = getLabelsAfterOne(cups)
    print("result", res)


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

    print("\nPART 1 RESULT")
    runpart1()

    # print("\nPART 2 RESULT")
    # runpart2()
