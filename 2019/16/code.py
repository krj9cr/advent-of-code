from copy import deepcopy
import numpy as np

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file][0]

def parseInput(lines):
    return parseLine(lines)

def parseLine(line: str):
    return [int(char) for char in line.strip()]

basePattern = [0, 1, 0, -1]

# assume the two provided lists are the same len
def phaseRow(inputDigits, patternDigits):
    if len(inputDigits) != len(patternDigits):
        print("ERROR: provided input digits and pattern digits are not the same length")
        print("input digits", inputDigits)
        print("pattern digits", patternDigits)
        exit(1)
    total = 0
    for (inp, pat) in list(zip(inputDigits, patternDigits)):
        total += (inp * pat)
    return abs(total) % 10

###########################
# part1
###########################
def part1(data, phases=100):
    print(data)
    size = len(data)
    print("size",size)
    patterns = []
    for outi in range(size):
        repeatedDigits = list(np.repeat(basePattern, outi+1))
        diff = (size + 1) - len(repeatedDigits)
        if diff > 0:
            for d in range(diff):
                repeatedDigits.append(repeatedDigits[d])
        patterns.append(repeatedDigits[1:size + 1])
    print(len(patterns))
    currDigits = deepcopy(data)
    for phasei in range(phases):
        nextDigits = []
        for outi in range(size):
            nextDigits.append(phaseRow(currDigits, patterns[outi]))
        currDigits = deepcopy(nextDigits)
    print("final digits:")
    [print(item,end='') for item in currDigits[0:8]]
    print()

def testpart1(data, phases=100):
    lines = parseInput(data)
    part1(lines, phases)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data, phases=100):
    print(data)
    messageoffset = int(''.join([str(num) for num in data[:7]]))
    data = data * 10000
    size = len(data)
    print("size",size)
    patterns = []
    for outi in range(size):
        repeatedDigits = list(np.repeat(basePattern, outi+1))
        diff = (size + 1) - len(repeatedDigits)
        if diff > 0:
            for d in range(diff):
                repeatedDigits.append(repeatedDigits[d])
        patterns.append(repeatedDigits[1:size + 1])
    print(len(patterns))
    currDigits = deepcopy(data)
    for phasei in range(phases):
        nextDigits = []
        for outi in range(size):
            nextDigits.append(phaseRow(currDigits, patterns[outi]))
        currDigits = deepcopy(nextDigits)
        print('phase', phasei)
    message = currDigits[messageoffset+1:messageoffset+8+1]
    print("message:",message)

def testpart2(data, phases=100):
    lines = parseInput(data)
    part2(lines,phases)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1("12345678",4)
    # testpart1("80871224585914546619083218645595")
    # testpart1("19617804207202209144916044189917")
    # testpart1("69317163492948606335995924319873")
    #
    # print("\nPART 1 RESULT")
    # runpart1()

    print("\n\nPART 2 TEST DATA")
    testpart2("03036732577212944063491565474664")
    testpart2("02935109699940807407585447034323")
    testpart2("03081770884921959731165446850517")

    # print("\nPART 2 RESULT")
    # runpart2()
