
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

def op1(modes, data, i, relativeBase):
    arg1 = data[i+1]
    arg2 = data[i+2]
    mem = data[i+3]
    if modes[0] == 0:
        arg1 = data[arg1]
    elif modes[0] == 2:
        arg1 = data[relativeBase+arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    elif modes[1] == 2:
        arg2 = data[relativeBase+arg2]
    if modes[2] == 2:
        mem += relativeBase
    data[mem] = arg1 + arg2

def op2(modes, data, i, relativeBase):
    arg1 = data[i+1]
    arg2 = data[i+2]
    mem = data[i+3]
    if modes[0] == 0:
        arg1 = data[arg1]
    elif modes[0] == 2:
        arg1 = data[relativeBase+arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    elif modes[1] == 2:
        arg2 = data[relativeBase+arg2]
    if modes[2] == 2:
        mem += relativeBase
    data[mem] = arg1 * arg2

def op3(modes, inp, data, i, relativeBase):
    arg = data[i+1]
    if modes[0] == 0:
        arg = data[arg]
    elif modes[0] == 2:
        arg += relativeBase
    data[arg] = inp

def op4(modes, data, i, relativeBase):
    arg = data[i+1]
    if modes[0] == 0:
        arg = data[arg]
    elif modes[0] == 2:
        arg = data[relativeBase+arg]
    return arg

def op5(modes, data, i, relativeBase):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    elif modes[0] == 2:
        arg1 = data[relativeBase+arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    elif modes[1] == 2:
        arg2 = data[relativeBase+arg2]
    if arg1 != 0:
        return arg2
    else:
        return i+3

def op6(modes, data, i, relativeBase):
    arg1 = data[i+1]
    arg2 = data[i+2]
    if modes[0] == 0:
        arg1 = data[arg1]
    elif modes[0] == 2:
        arg1 = data[relativeBase+arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    elif modes[1] == 2:
        arg2 = data[relativeBase+arg2]
    if arg1 == 0:
        return arg2
    else:
        return i+3

def op7(modes, data, i, relativeBase):
    arg1 = data[i+1]
    arg2 = data[i+2]
    mem  = data[i+3]
    if modes[0] == 0:
        arg1 = data[arg1]
    elif modes[0] == 2:
        arg1 = data[relativeBase+arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    elif modes[1] == 2:
        arg2 = data[relativeBase+arg2]
    if modes[2] == 2:
        mem += relativeBase
    if arg1 < arg2:
        data[mem] = 1
    else:
        data[mem] = 0

def op8(modes, data, i, relativeBase):
    arg1 = data[i+1]
    arg2 = data[i+2]
    mem  = data[i+3]
    if modes[0] == 0:
        arg1 = data[arg1]
    elif modes[0] == 2:
        arg1 = data[relativeBase+arg1]
    if modes[1] == 0:
        arg2 = data[arg2]
    elif modes[1] == 2:
        arg2 = data[relativeBase+arg2]
    if modes[2] == 2:
        mem += relativeBase
    if arg1 == arg2:
        data[mem] = 1
    else:
        data[mem] = 0

def op9(modes, data, i, relativeBase):
    arg = data[i+1]
    if modes[0] == 0:
        arg = data[arg]
    elif modes[0] == 2:
        arg = data[relativeBase+arg]
    return relativeBase + arg

def intcode(data, input, relativeBase):
    ip = 0
    output = []
    while ip < len(data):
        # print(data)
        # print("relativeBase:",relativeBase)
        nextOp = data[ip]
        modes, op = parseOp(nextOp)
        if op == 1:
            op1(modes, data, ip, relativeBase)
            ip += 4
        elif op == 2:
            op2(modes, data, ip, relativeBase)
            ip += 4
        elif op == 3:
            op3(modes, input, data, ip, relativeBase)
            ip += 2
        elif op == 4:
            output.append(op4(modes, data, ip, relativeBase))
            ip += 2
        elif op == 5:
            ip = op5(modes, data, ip, relativeBase)
        elif op == 6:
            ip = op6(modes, data, ip, relativeBase)
        elif op == 7:
            op7(modes, data, ip, relativeBase)
            ip += 4
        elif op == 8:
            op8(modes, data, ip, relativeBase)
            ip += 4
        elif op == 9:
            relativeBase = op9(modes, data, ip, relativeBase)
            ip += 2
        elif op == 99:
            break
        else:
            print("BAD OPCODE:",op)
            exit(1)
    return output


###########################
# part1
###########################
def part1(data):
    for _ in range(0, 1000):
        data.append(0)
    print("output",intcode(data, 1, 0))

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    for _ in range(0, 1000):
        data.append(0)
    print("output",intcode(data, 2, 0))

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

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
