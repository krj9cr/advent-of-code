
###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        file_input = file.read()
        print(file_input)
        return parseInput(file_input)

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
    print(data)
    sum = 0
    size = len(data)
    for i, d in enumerate(data):
        if data[i] == data[(i+1)%size]:
            sum += data[i]
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
    size = len(data)
    for i, d in enumerate(data):
        ahead = int(size/2)
        # print(ahead)
        j = (i + ahead) % size
        # print(i, j)
        if data[i] == data[j]:
            sum += data[i]
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
    # testpart1("1122")
    # testpart1("1111")
    # testpart1("1234")
    # testpart1("91212129")
    #
    # print("\nPART 1 RESULT")
    # runpart1()

    print("\n\nPART 2 TEST DATA")
    testpart2("1212")
    testpart2("1221")
    testpart2("123425")
    testpart2("123123")
    testpart2("12131415")


    print("\nPART 2 RESULT")
    runpart2()
