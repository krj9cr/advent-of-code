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
    print(lines)
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    # print(line)
    return [ int(l) for l in line.strip().split() ]

###########################
# part1
###########################
def part1(data):
    print(data)
    sum = 0
    for row in data:
        wow = np.array(row)
        sum += wow.max() - wow.min()
    print(sum)

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)
    sum = 0
    for row in data:
        size = len(row)
        found = False
        for i in range(0, size):
            a = row[i]
            for j in range(0, size):
                if i != j:
                    b = row[j]
                    if a % b == 0:
                        sum += int(a/b)
                        # print(a, b)
                        found = True
                        break
                    elif b % a == 0:
                        sum += int(b/a)
                        found = True
                        # print(a, b)
                        break
            if found:
                break
    print(sum)

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1(["5 1 9 5","7 5 3","2 4 6 8"])
    #
    # print("\nPART 1 RESULT")
    # runpart1()

    print("\n\nPART 2 TEST DATA")
    testpart2(["5 9 2 8","9 4 7 3","3 8 6 5"])

    print("\nPART 2 RESULT")
    runpart2()
