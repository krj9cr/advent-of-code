import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from intcode import Intcode

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

def parseOp(op):
    s = str(op)
    numZerosAdd =  5 - len(s)
    zeros = ""
    for i in range(0,numZerosAdd):
        zeros += "0"
    s = zeros + s
    modes = s[0:3]
    op = s[3:]
    return [int(m) for m in reversed(modes)], int(op)

###########################
# part1
###########################
def part1(data):
    print(data)
    intcoder = Intcode(data, [1], debug=True)
    intcoder.run()
    print(intcoder.output)

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
    intcoder = Intcode(data, [2])
    intcoder.run()
    print(intcoder.output)

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
    # testpart1("109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99")
    # testpart1("1102,34915192,34915192,7,4,7,99,0")
    # testpart1("104,1125899906842624,99")

    print("\nPART 1 RESULT")
    runpart1()

    print("\nPART 2 RESULT")
    runpart2()
