
###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseInput(lines):
    return [ int(line) for line in str(lines).split(",") ]

def parseLine(line: str):
    policy = line.strip().split(":")
    pw = policy[1].strip()
    policy3 = policy[0].split("-")
    policyMin = int(policy3[0])
    policy4 = policy3[1].split(" ")
    policyMax = int(policy4[0])
    letter = policy4[1].strip()
    return policyMin, policyMax, letter, pw


###########################
# part1
###########################
def part1(data):
    print(data)
    count = 0
    for policyMin, policyMax, letter, pw in data:
        letterCount = pw.count(letter)
        if letterCount >= policyMin and letterCount <= policyMax:
            count += 1
    print(count)


def runpart1():
    part1(parseInputFile())


###########################
# part2
###########################
def part2(data):
    print(data)
    count = 0
    for policyMin, policyMax, letter, pw in data:
        if pw[policyMin-1] == letter and pw[policyMax-1] != letter:
            print(policyMin, policyMax, letter, pw)
            count += 1
        elif pw[policyMin-1] != letter and pw[policyMax-1] == letter:
            print(policyMin, policyMax, letter, pw)
            count +=1
    print(count)


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
