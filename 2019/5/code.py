from random import randint

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

def op1(modes, data, i):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    data[data[i+3]] = arg1 + arg2

def op2(modes, data, i):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    data[data[i+3]] = arg1 * arg2

def op3(input, data, i):
    data[data[i+1]] = input

def op4(modes, data, i):
    arg = data[i+1]
    if modes[0] == 0:
        arg = data[arg]
    return arg

def op5(modes, data, i):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    if arg1 != 0:
        return arg2
    else:
        return i+3

def op6(modes, data, i):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    if arg1 == 0:
        return arg2
    else:
        return i+3

def op7(modes, data, i):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    if arg1 < arg2:
        data[data[i+3]] = 1
    else:
        data[data[i+3]] = 0

def op8(modes, data, i):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    if arg1 == arg2:
        data[data[i+3]] = 1
    else:
        data[data[i+3]] = 0

def part1(data, input):
    print(data)
    i = 0
    output = []
    while i < len(data):
        nextOp = data[i]
        modes, op = parseOp(nextOp)
        if op == 1:
            print("op 1")
            op1(modes, data, i)
            i += 4
        elif op == 2:
            print("op 2")
            op2(modes, data, i)
            i += 4
        elif op == 3:
            print("op 3")
            op3(input, data, i)
            print(data)
            i += 2
        elif op == 4:
            print("op 4")
            output.append(op4(modes, data, i))
            i += 2
        elif op == 99:
            print("exiting")
            break
    print("output: ", output)

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
    i = 0
    output = []
    while i < len(data):
        print(data)
        nextOp = data[i]
        modes, op = parseOp(nextOp)
        if op == 1:
            print("op 1")
            op1(modes, data, i)
            i += 4
        elif op == 2:
            print("op 2")
            op2(modes, data, i)
            i += 4
        elif op == 3:
            print("op 3")
            op3(input, data, i)
            i += 2
        elif op == 4:
            print("op 4")
            output.append(op4(modes, data, i))
            i += 2
        elif op == 5:
            print("op 5")
            i = op5(modes, data, i)
        elif op == 6:
            print("op 6")
            i = op6(modes, data, i)
        elif op == 7:
            print("op 7")
            op7(modes, data, i)
            i += 4
        elif op == 8:
            print("op 8")
            op8(modes, data, i)
            i += 4
        elif op == 99:
            print("exiting")
            break
        else:
            print("BAD OPCODE??")
            exit(1)
    print("output: ", output)

def testpart2(data, input):
    lines = parseInput(data)
    part2(lines, input)

def runpart2():
    part2(parseInputFile(), 5)

###########################
# run
###########################
if __name__ == '__main__':
    print("PART 1 TEST DATA")
    # testpart1("3,0,4,0,99")
#     testpart1("1,1,1,4,99,5,6,0,99")

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", 8)

    print("\nPART 2 RESULT")
    runpart2()
