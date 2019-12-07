from random import seed
from random import randint

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
    i = 0
    while i < len(data):
        nextOp = data[i]
        if nextOp == 1:
            data[data[i+3]] = data[data[i+1]] + data[data[i+2]]
            print("op 1")
        elif nextOp == 2:
            data[data[i+3]] = data[data[i+1]] * data[data[i+2]]
            print("op 2")
        elif nextOp == 99:
            print("exiting")
            break
        i += 4

    print(data)

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())


###########################
# part2
###########################
def part2(data):

    print(len(data))
    print(data)
    origData = data.copy()

    goal = 19690720
    guess = 0
    while guess != goal:
        data[1] = randint(0, 120) #data.index(63)
        data[2] = randint(0, 120)
        i = 0
        while i < len(data):
            nextOp = data[i]
            if nextOp == 1:
                data[data[i+3]] = data[data[i+1]] + data[data[i+2]]
    #             print("op 1")
            elif nextOp == 2:
                data[data[i+3]] = data[data[i+1]] * data[data[i+2]]
    #             print("op 2")
            elif nextOp == 99:
                print("exiting")
                break
            i += 4
#         print(data)
#         guessIndex += 1
        guess = data[0]
        print(data)
        data = origData.copy()
        print(data)
    print(data)

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    print("PART 1 TEST DATA")
#     testpart1("1,0,0,0,99")
#     testpart1("1,1,1,4,99,5,6,0,99")

#     print("\nPART 1 RESULT")
#     runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
