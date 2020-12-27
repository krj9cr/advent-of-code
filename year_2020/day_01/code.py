import time

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
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return int(line.strip())

###########################
# part1
###########################
def part1(data):
    for num1 in data:
        for num2 in data:
            if num1 != num2 and num1 + num2 == 2020:
                print("num1: ", num1, "num2: ", num2, "answer: ", num1*num2)
                return

def runpart1():
    part1(parseInputFile())


###########################
# part2
###########################
def part2(data):
    for num1 in data:
        for num2 in data:
            for num3 in data:
                if num1 != num2 and num2 != num3 and num1 != num3 and num1 + num2 + num3 == 2020:
                    print("num1: ", num1, "num2: ", num2, "num3: ", num3, "answer: ", num1*num2*num3)
                    return


def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
