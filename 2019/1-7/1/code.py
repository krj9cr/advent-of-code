

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
    sum = 0
    for num in data:
        sum += mass(num)
    print(sum)

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

def mass(num):
    m = int((num / 3)) - 2
    # print("mass:", m)
    return m

def fuel(num):
    m = mass(num)
    if m > 0:
        return num + fuel(m)
    else:
        return num

###########################
# part2
###########################
def part2(data):
    sum = 0
    for num in data:
        sum += fuel(mass(num))
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
    # testpart1(["12"])
    # testpart1(["100756"])

    # print("\nPART 1 RESULT")
    # runpart1()
    #
    # print("\n\nPART 2 TEST DATA")
    # testpart2(["14"])
    # testpart2(["1969"])
    # testpart2(["100756"])

    print("\nPART 2 RESULT")
    runpart2()
