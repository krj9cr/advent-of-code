from lib.intcode import Intcode

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [ int(num) for num in [ line.split(",") for line in file ][0] ]

def parseInput(lines):
    return [ int(line) for line in str(lines).split(",") ]

def parseLine(line: str):
    return line.strip()

def asciiToGrid(ascii):
    grid = []
    row = []
    for a in ascii:
        if a == 10 and len(row) > 0:
            grid.append(row[:])
            row = []
        else:
            row.append(str(chr(a)))
    return grid

def printGrid(grid):
    for row in grid:
        for item in row:
            print(item,end="")
        print()

def asciiToIntcodeInput(astr):
    result = []
    for s in astr:
        for char in s:
            result.append(ord(char))
    # add final newline if necessary
    if result[-1] != 10:
        result.append(10)
    return result

###########################
# part1
###########################
def part1(data):
    asciiInput = ""

    # GOAL: if not (A or B or C) and D then jump

    # J if A is ground
    asciiInput += "NOT A J\n"
    # T if B is ground
    asciiInput += "NOT B T\n"
    # J if A or B is ground
    asciiInput += "OR T J\n"

    # T if C is ground
    asciiInput += "NOT C T\n"
    # J if (A or B or C) is ground
    asciiInput += "OR T J\n"

    # J if (A or B or C) and D is ground
    asciiInput += "AND D J\n"

    # final command
    asciiInput += "WALK\n"

    intcode_input = asciiToIntcodeInput(asciiInput)
    intcoder = Intcode(data, intcode_input)
    intcoder.run()

    # check intocder output
    if len(intcoder.output) > 0:
        if intcoder.output[-1] > 127:
            print("hull damage:", intcoder.output[-1])
        else:
            print("droid fell")
            printGrid(asciiToGrid(intcoder.output))
            print()
    else:
        print("ERROR: no intcoder output??")

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):

    asciiInput = ""

    # PART 1
    # if not (A or B or C) and D then jump
    # J if A is ground
    asciiInput += "NOT A J\n"
    # T if B is ground
    asciiInput += "NOT B T\n"

    # J if A or B is ground
    asciiInput += "OR T J\n"
    # T if C is ground
    asciiInput += "NOT C T\n"
    # J if (A or B or C) is ground
    asciiInput += "OR T J\n"

    # J if (A or B or C) and D is ground
    asciiInput += "AND D J\n"

    # PART 2
    # jump if D and (H or EI or EF)
    #         D and (H or (E and (I or F)))
    # set T = I, T OR F, T AND E, T OR H
    asciiInput += "NOT I T\n"
    asciiInput += "NOT I T\n"
    asciiInput += "OR F T\n"
    asciiInput += "AND E T\n"
    asciiInput += "OR H T\n"
    # huh....
    asciiInput += "OR E T\n"
    asciiInput += "OR H T\n"
    asciiInput += "AND T J\n"

    # final command
    # asciiInput += "WALK\n"
    asciiInput += "RUN\n"

    intcode_input = asciiToIntcodeInput(asciiInput)
    intcoder = Intcode(data, intcode_input)
    intcoder.run()

    # check intocder output
    if len(intcoder.output) > 0:
        if intcoder.output[-1] > 127:
            print("hull damage:", intcoder.output[-1])
        else:
            print("droid fell")
            printGrid(asciiToGrid(intcoder.output))
            print()
    else:
        print("ERROR: no intcoder output??")

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    print("\nPART 2 RESULT")
    runpart2()
