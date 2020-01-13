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

###########################
# part1
###########################
def part1(data, input):
    print(data)
    intcoder = Intcode(data, [input],debug=True)
    intcoder.run()
    print(intcoder.output[-1])

def testpart1(data):
    lines = parseInput(data)
    part1(lines, 1)

def runpart1():
    part1(parseInputFile(), 1)


###########################
# part2
###########################
def part2(data, input):
    print(data)
    intcoder = Intcode(data, [input])
    intcoder.run()
    print(intcoder.output[0])

def testpart2(data, input):
    lines = parseInput(data)
    part2(lines, input)

def runpart2():
    part2(parseInputFile(), 5)

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1("3,0,4,0,99")
    # testpart1("1,1,1,4,99,5,6,0,99")

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", 8)

    print("\nPART 2 RESULT")
    runpart2()
