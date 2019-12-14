
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
    for _ in range(0, 1000):
        data.append(0)
    output = intcode(data, 0, 0)
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
    for _ in range(0, 1000):
        data.append(0)
    data[0] = 2
    output = intcode(data, 0, 0)
    # omg....

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

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    # print("\nPART 2 RESULT")
    # runpart2()
