from random import randint
from copy import deepcopy
from lib.intcode import Intcode

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [ int(num) for num in [ line.split(",") for line in file ][0] ]

def parseFile(path: str):
    with open(path, 'r') as file:
        return parseInput(file)

def parseInput(lines):
    return [ int(line) for line in str(lines).split(",") ]

def parseLine(line: str):
    return line.strip()

###########################
# part1
###########################
def part1(data):
    print(data)
    data[1] = 12
    data[2] = 2

    intcoder = Intcode(data)
    intcoder.run()

    print("answer",intcoder.state[0])

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())


###########################
# part2
###########################
def part2(origData):
    print(origData)

    goal = 19690720
    guess = 0
    while guess != goal:
        data = deepcopy(origData)
        data[1] = randint(0, 100)
        data[2] = randint(0, 100)

        intcoder = Intcode(data)
        intcoder.run()

        guess = intcoder.state[0]
        print(guess)
    print("answer", data[1] * 100 + data[2])

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    print("PART 1 TEST DATA")
#     testpart1("1,0,0,0,99")
#     testpart1("1,1,1,4,99,5,6,0,99")

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
