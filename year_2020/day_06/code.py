

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        # read lines
        rawlines = [line.strip() for line in file]

        # batch them into lists separated by empty line
        batchedlines = []
        currBatch = []
        for line in rawlines:
            if line != '':
                currBatch.append(line)
            else:
                batchedlines.append(currBatch)
                currBatch = []
        return batchedlines

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
def part1(data):
    print(data)
    result = 0
    for group in data:
        questions = {}
        if len(group) == 1:
            result += len(group[0])
            print(result)
            continue
        else:
            for person in group:
                for letter in person:
                    questions[letter] = 1
            result += len(questions)
        print(result)


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
    result = 0
    for group in data:
        questions = {}
        if len(group) == 1:
            result += len(group[0])
            print(result)
            continue
        else:
            for person in group:
                for letter in person:
                    if questions.get(letter) is not None:
                        questions[letter] = questions[letter] + 1
                    else:
                        questions[letter] = 1
            for q in questions:
                if questions[q] == len(group):
                    result += 1
            # print(questions)
        print(result)

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
    # testpart1("1111")
    # testpart1("1234")

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
