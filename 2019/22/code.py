

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
def part1(data, size):
    # print(data)

    deck = [ i for i in range(size) ]

    for instruction in data:
        if "deal into new stack" == instruction:
            deck = list(reversed(deck))
        elif "deal with increment" in instruction:
            increment = int(instruction.split(" ")[-1])
            newdeck = [0 for _ in range(size)]
            newi = 0
            for i in range(size):
                newdeck[newi] = deck[i]
                newi += increment
                newi = newi % size
            deck = newdeck
        elif "cut" in instruction:
            cut = int(instruction.split(" ")[-1])
            newdeck = deck[cut:] + deck[:cut]
            deck = newdeck
        # print(deck)
    if size > 2019:
        print("2019",deck.index(2019))

def testpart1(data, size):
    lines = parseInput(data)
    part1(lines, size)

def runpart1():
    part1(parseInputFile(), 10007)

###########################
# part2
###########################
def part2(data, size):
    # print(data)

    deck = [ i for i in range(size) ]

    for x in range(101741582076661):
        print(x)
        for instruction in data:
            if "deal into new stack" == instruction:
                deck = list(reversed(deck))
            elif "deal with increment" in instruction:
                increment = int(instruction.split(" ")[-1])
                newdeck = [0 for _ in range(size)]
                newi = 0
                for i in range(size):
                    newdeck[newi] = deck[i]
                    newi += increment
                    newi = newi % size
                deck = newdeck
            elif "cut" in instruction:
                cut = int(instruction.split(" ")[-1])
                newdeck = deck[cut:] + deck[:cut]
                deck = newdeck
            # print(deck)
    if size > 2020:
        print("2020:",deck.index(2020))


def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile(), 119315717514047)

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1(["deal into new stack"], 10)
    # testpart1(["cut 3"], 10)
    # testpart1(["cut -4"], 10)
    # testpart1(["deal with increment 3"], 10)
    #
    # testpart1(["deal with increment 7", "deal into new stack", "deal into new stack"], 10)
    #
    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
