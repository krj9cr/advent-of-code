

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
    return line.strip()

###########################
# part1
###########################
def part1():
    start = 128392
    end = 643281
    count = 0
    for i in range(start,end+1):
        count += testNum(i)
    print(count)

def testIncrease(s):
    prev = s[0]
    sp = s[1:]
    for char in sp:
        if int(char) < int(prev):
            return False
        else:
            prev = char
    return True

def testDouble(s):
    prev = s[0]
    sp = s[1:]
    for char in sp:
        if prev == char:
            return True
        else:
            prev = char
    return False

def testNum(i):
    s = str(i)
    if len(s) == 6 and testIncrease(s) and testDouble(s):
        return 1
    return 0

def runpart1():
    part1()

###########################
# part2
###########################
def testPairs(s):
    # print(s)
    if len(s) == 0 or len(s) == 1:
        return False
    if len(s) == 2:
        if s[0] == s[1]:
            return True
    if s[0] == s[1]:
        if s[0] != s[2]:
            return True
        else:
            if len(s) == 3:
                return False
            # find the next different thing
            for i in range(3, len(s)):
                if s[i] != s[0]:
                    return testPairs(s[i:])
            return False
    else:
        return testPairs(s[1:])

def testNum2(i):
    s = str(i)
    if len(s) == 6 and testIncrease(s) and testPairs(s):
        print(i)
        return 1
    return 0

def part2():
    start = 128392
    end = 643281
    count = 0
    for i in range(start,end+1):
        count += testNum2(i)
    print(count)

def runpart2():
    part2()


###########################
# run
###########################
if __name__ == '__main__':
#     print("PART 1 TEST DATA")
#     print(testNum(111111))
#     print(testNum(223450))
#     print(testNum(123789))

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # print(testNum2(111223))
    # print(testNum2(122234))
    # print(testNum2(123334))
    # print(testNum2(123344))
    # print(testNum2(123444))

    # print(testNum2(111122))
    # print(testNum2(111123))
    # print(testNum2(128899))

    # print("\nPART 2 RESULT")
    # runpart2()
