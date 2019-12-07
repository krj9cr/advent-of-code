from itertools import permutations
import sys
import threading, time

locks = [ threading.Lock() for _ in range(0,5)]

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

def op3(inp, data, i):
    data[data[i+1]] = inp

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


def intcode(data, inputs):
    # print(data)
    ip = 0
    inputi = 0
    output = []
    while ip < len(data):
        # print(data)
        nextOp = data[ip]
        modes, op = parseOp(nextOp)
        if op == 1:
            # print("op 1")
            op1(modes, data, ip)
            ip += 4
        elif op == 2:
            # print("op 2")
            op2(modes, data, ip)
            ip += 4
        elif op == 3:
            # print("op 3")
            while inputs[inputi] is None:
                time.sleep(1)
            op3(inputs[inputi], data, ip)
            inputi += 1
            ip += 2
        elif op == 4:
            # print("op 4")
            output.append(op4(modes, data, ip))
            ip += 2
        elif op == 5:
            # print("op 5")
            ip = op5(modes, data, ip)
        elif op == 6:
            # print("op 6")
            ip = op6(modes, data, ip)
        elif op == 7:
            # print("op 7")
            op7(modes, data, ip)
            ip += 4
        elif op == 8:
            # print("op 8")
            op8(modes, data, ip)
            ip += 4
        elif op == 99:
            # print("exiting")
            break
        else:
            print("BAD OPCODE??")
            exit(1)
    return output


###########################
# part1
###########################


def part1(data):
    # Get all permutations
    phases = list(permutations([0,1,2,3,4]))

    largest = -sys.maxsize
    largestphase = []

    # Print the obtained permutations
    for phase in phases:
        ampout = 0
        for ampi in range(0, 5):
            ampout = intcode(data.copy(), [phase[ampi], ampout])[0]
        if ampout > largest:
            largest = ampout
            largestphase = phase
    print(largest, "with", largestphase)

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################

def ampintcode(data, phaseSetting, ampinputs, ampindex):
    ip = 0
    usedphase = False
    while ip < len(data):
        # print(data)
        nextOp = data[ip]
        modes, op = parseOp(nextOp)
        if op == 1:
            op1(modes, data, ip)
            ip += 4
        elif op == 2:
            op2(modes, data, ip)
            ip += 4
        elif op == 3:
            if usedphase:
                while True:
                    with locks[ampindex]:
                        wow = ampinputs[ampindex]
                    if wow is None:
                        time.sleep(1)
                    else:
                        break
                with locks[ampindex]:
                    op3(ampinputs[ampindex], data, ip)
                    ampinputs[ampindex] = None
            else:
                op3(phaseSetting, data, ip)
                usedphase = True
            ip += 2
        elif op == 4:
            idx = (ampindex+1)%5
            with locks[idx]:
                ampinputs[idx] = op4(modes, data, ip)
            time.sleep(2)
            ip += 2
        elif op == 5:
            ip = op5(modes, data, ip)
        elif op == 6:
            ip = op6(modes, data, ip)
        elif op == 7:
            op7(modes, data, ip)
            ip += 4
        elif op == 8:
            op8(modes, data, ip)
            ip += 4
        elif op == 99:
            break
        else:
            print("BAD OPCODE??")
            return

def part2(data):
    # Get all permutations
    phases = reversed(list(permutations([5,6,7,8,9])))

    largest = -sys.maxsize
    largestphase = []

    for phase in phases:
        print("phase:", phase)
        ampins  = [ None for _ in range(0,5) ]
        ampins[0] = 0
        threads = []
        for ampi in range(0, 5):
            t = threading.Thread(target=ampintcode, args=(data.copy(), phase[ampi], ampins, ampi))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()
        lastout = ampins[0]
        if lastout > largest:
            largest = lastout
            largestphase = phase
        print(largest, "with", largestphase)
    print(largest, "with", largestphase)

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
    # testpart1("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
    # testpart1("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
    # testpart1("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\n\nPART 2 TEST DATA")
    testpart2("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
    # testpart2("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")

    # print("\nPART 2 RESULT")
    # runpart2()
