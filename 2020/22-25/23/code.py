import time
from copy import deepcopy
from collections import deque
from lib.linkedlist import Node, CircularLinkedList

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file][0]

def parseLine(line: str):
    return [ int(s) for s in line.strip() ]

def getLabelsAfterOne(cups):
    oneNode = cups.find(1)
    cups.head = oneNode
    l = []
    for node in cups:
        l.append(str(node.data))
    l.pop(0) # remove one
    return "".join(l)

def move2(cups, lenCups, currentCup):
    minCup = 1
    maxCup = lenCups

    cups.head = currentCup
    print("current cup:", currentCup)
    print("cups:", cups)
    # currentCup = cups.head
    pickup1 = currentCup.next
    pickup2 = pickup1.next
    pickup3 = pickup2.next

    pickupData = list(reversed([pickup1.data, pickup2.data, pickup3.data]))
    print("pickup:", pickupData)
    # destination cup: the cup with a label equal to the current cup's label minus one
    destinationCup = currentCup.data - 1
    # If this would select one of the cups that was just picked up,
    # the crab will keep subtracting one until it finds a cup that wasn't just picked up
    while destinationCup in pickupData:
        destinationCup -= 1
    # If at any point in this process the value goes below the lowest value on any cup's label,
    # it wraps around to the highest value on any cup's label instead
    if destinationCup < minCup:
        destinationCup = maxCup
    while destinationCup in pickupData:
        destinationCup -= 1
    print("desintation:", destinationCup)

    # move picked up cups after destination cup
    for i in range(len(pickupData)):
        cups.remove_node_with_data(pickupData[i])
        cups.add_after(destinationCup, Node(pickupData[i]))

    destinationNode = cups.find(destinationCup)
    currentCup = currentCup.next

    return cups, currentCup

###########################
# part1
###########################
def part1(data):
    numCups = len(data)

    cups = CircularLinkedList(data)
    print(cups)

    currentCup = cups.head
    numMoves = 100
    for i in range(numMoves):
        print("move ", i)
        cups, currentCup = move2(cups, numCups, currentCup)
        print()

    print("Final cups", cups)
    res = getLabelsAfterOne(cups)
    print("result", res)


    # cups = deque(data)
    #
    # currentCup = data[0]
    #
    # numMoves = 100
    # for i in range(numMoves):
    #     # print("move ", i)
    #     cups = move(cups, numCups)#, currentCup, numCups)
    #     # print()
    #
    # print("Final cups", cups)
    # res = getLabelsAfterOne(cups)
    # print("result", res)



def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def getTwoCupsAfterOne(indexes):
    idx = indexes[1]
    vals = []
    for cup in indexes:
        if indexes[cup] == idx + 1 or indexes[cup] == idx + 2:
            vals.append(cup)
    print("vals",vals)
    return vals[0] * vals[1]


def moveWithIndexes(cups, lenCups, indexes):
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

def part2(data):
    print(data)
    m = max(data)
    numCups = 1000000
    cups = deque(data[:] + [ i for i in range(m+1, numCups+1)])

    indexes = {}
    for i in range(numCups):
        indexes[cups[i]] = i

    currentCup = cups[0]

    # numMoves = 100
    numMoves = 10000000 # ten million
    for i in range(numMoves):
        cups = moveWithIndexes(cups, numCups, indexes)#, currentCup, numCups)

    print("Final cups", cups)
    res = getTwoCupsAfterOne(indexes)
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
