

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
def part1(data, size, cardIdx=2019):
    # print(data)
    for instruction in data:
        if "deal into new stack" == instruction:
            cardIdx = (-cardIdx - 1) % size
        elif "deal with increment" in instruction:
            increment = int(instruction.split(" ")[-1])
            cardIdx = (cardIdx * increment) % size
        elif "cut" in instruction:
            cut = int(instruction.split(" ")[-1])
            cardIdx = (cardIdx - cut) % size
    print("2019",cardIdx)

def testpart1(data, size):
    lines = parseInput(data)
    part1(lines, size)

def runpart1():
    part1(parseInputFile(), 10007)

###########################
# part2
###########################
# Fermat's little theorem gives a simple inv:
def inv(a, n): return pow(a, n-2, n)

# https://en.wikipedia.org/wiki/Linear_congruential_generator
def part2(data, size, cardIdx=2020, numShuffles=101741582076661):
    # print(data)
    a, b = 1, 0
    for instruction in data:
        if "deal into new stack" == instruction:
            la, lb = -1, -1
        elif "deal with increment" in instruction:
            la, lb = int(instruction.split(" ")[-1]), 0
        elif "cut" in instruction:
            la, lb = 1, -int(instruction.split(" ")[-1])
        # la * (a * x + b) + lb == la * a * x + la*b + lb
        # The `% n` doesn't change the result, but keeps the numbers small.
        a = (la * a) % size
        b = (la * b + lb) % size

    Ma = pow(a, numShuffles, size)
    Mb = (b * (Ma - 1) * inv(a - 1, size)) % size

    # This computes "where does year_2020 end up", but I want "what is at year_2020".
    # print((Ma * c + Mb) % n)

    # So need to invert (year_2020 - MB) * inv(Ma)
    print("location of year_2020",((cardIdx - Mb) * inv(Ma, size)) % size)


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

    print("\nPART 2 RESULT")
    runpart2()
