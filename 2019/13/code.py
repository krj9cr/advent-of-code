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

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

###########################
# part1
###########################
def part1(data):
    print(data)
    intcoder = Intcode(data, [0])
    intcoder.run()
    output = intcoder.output
    output = chunkIt(output, len(output)/3)
    numBlocks = 0
    for tile in output:
        if tile[2] == 2:
             numBlocks +=1
    print(numBlocks)

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
    data[0] = 2
    inputs = []
    intcoder = Intcode(data, inputs)
    score = 0
    # possible inputs
    outputs = []
    ballPos = 0
    padPos = 0
    while intcoder.running:
        # check for outputs
        if len(intcoder.output) >= 3:
            # print("output",intcoder.output)
            o1, o2, o3 = intcoder.output
            if o3 == 4:
                ballPos = o1
                print("ballPos",ballPos,o2)
                # provide next input
                nextinput = 0
                sign = padPos - ballPos
                if sign > 0:
                    nextinput = -1
                elif sign < 0:
                    nextinput = 1
                inputs.append(nextinput)
                print("nextinput",nextinput)
            if o3 == 3:
                padPos = o1
                print("padPos",padPos,o2)
                # provide next input
                nextinput = 0
                sign = padPos - ballPos
                if sign > 0:
                    nextinput = -1
                elif sign < 0:
                    nextinput = 1
                inputs.append(nextinput)
                print("nextinput",nextinput)
            if o1 == -1 and o2 == 0:
                score = o3
            outputs.append(intcoder.output)
            intcoder.output = []
        intcoder.step()
    print("score",score)

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
