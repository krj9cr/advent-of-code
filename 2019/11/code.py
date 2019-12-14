import sys, threading, time

# colorlock = threading.Lock()
# outputlock = threading.Lock()
runninglock = threading.Lock()
# color = 1
# output = []
running = True
# 0 = running state
# 1 = input
# 2 = output
locks  = [ threading.Lock() for _ in range(0,2)]


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

def ampintcode(data, phaseSetting, ampinputs, ampindex, relativeBase):
    ip = 0
    usedphase = False
    while ip < len(data):
        # print(data)
        nextOp = data[ip]
        modes, op = parseOp(nextOp)
        if op == 1:
            op1(modes, data, ip, relativeBase)
            ip += 4
        elif op == 2:
            op2(modes, data, ip, relativeBase)
            ip += 4
        elif op == 3:
            if usedphase:
                while True:
                    with locks[ampindex]:
                        wow = ampinputs[ampindex]
                    if wow is None:
                        print("incode waiting...")
                        time.sleep(1)
                    else:
                        break
                with locks[ampindex]:
                    op3(modes, ampinputs[ampindex], data, ip, relativeBase)
                    ampinputs[ampindex] = None
            else:
                op3(modes, phaseSetting, data, ip, relativeBase)
                usedphase = True
            ip += 2
        elif op == 4:
            idx = (ampindex+1)
            with locks[idx]:
                ampinputs[idx] = op4(modes, data, ip, relativeBase)
            time.sleep(2)
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
            with runninglock:
                running = False
                print("ROBOT DONE")
            return
        else:
            print("BAD OPCODE????", modes, op)
            print("IP: ",ip)
            print("data:",data)
            exit(1)

# def intcode(data, relativeBase, mem):
#     working = False
#     outp = 2
#     ip = 0
#     while ip < len(data):
#         nextOp = data[ip]
#         modes, op = parseOp(nextOp)
#         if op == 1:
#             op1(modes, data, ip, relativeBase)
#             ip += 4
#         elif op == 2:
#             op2(modes, data, ip, relativeBase)
#             ip += 4
#         elif op == 3:
#             while True:
#                 with locks[1]:
#                     wow = mem[1]
#                 if wow is None:
#                     time.sleep(1)
#                     # print("intcode waiting...")
#                 else:
#                     break
#             with locks[1]:
#                 print("intcode processing input: ", mem)
#                 op3(modes, mem[1], data, ip, relativeBase)
#                 mem[1] = None
#                 working = True
#             ip += 2
#         elif op == 4:
#             o = op4(modes, data, ip, relativeBase)
#             if working:
#                 with locks[2]:
#                     mem[outp] = o
#                 if outp == 2:
#                     outp = 3
#                 else:
#                     outp = 2
#                     print("intcode output: ", mem)
#                     working = False
#             else:
#                 print("trying to output while not processing input")
#             # while True:
#             #     with locks[2]:
#             #         wow = mem[outp]
#             #     if wow is not None:
#             #         time.sleep(1)
#             #     else:
#             #         mem[outp] = o
#             #         if outp == 2:
#             #             outp = 3
#             #         else:
#             #             outp = 2
#             #             print("intcode output: ", mem)
#             #         break
#             ip += 2
#         elif op == 5:
#             ip = op5(modes, data, ip, relativeBase)
#         elif op == 6:
#             ip = op6(modes, data, ip, relativeBase)
#         elif op == 7:
#             op7(modes, data, ip, relativeBase)
#             ip += 4
#         elif op == 8:
#             op8(modes, data, ip, relativeBase)
#             ip += 4
#         elif op == 9:
#             relativeBase = op9(modes, data, ip, relativeBase)
#             ip += 2
#         elif op == 99:
#             with locks[0]:
#                 mem[0] = False
#             return
#         else:
#             print("BAD OPCODE:",op)
#             with locks[0]:
#                 mem[0] = False
#             exit(1)
#     return True


###########################
# part1
###########################
def turnRobot(robotdir, newdir):
    if robotdir == "up":
        if newdir == 0:
            return "left"
        else:
            return "right"
    elif robotdir == "left":
        if newdir == 0:
            return "down"
        else:
            return "up"
    elif robotdir == "right":
        if newdir == 0:
            return "up"
        else:
            return "down"
    else:
        if newdir == 0:
            return "right"
        else:
            return "left"

def moveRobot(loc, robotdir, newdir):
    newrobotdir = turnRobot(robotdir, newdir)
    if newrobotdir == "up":
        return loc[0], loc[1]-1, newrobotdir
    elif newrobotdir == "left":
        return loc[0]-1, loc[1], newrobotdir
    elif newrobotdir == "right":
        return loc[0]+1, loc[1], newrobotdir
    else:
        return loc[0], loc[1]+1, newrobotdir

def controlRobot(ampins):
    panels = {}
    loc = (0,0)
    robotdir = "up"
    outp = 0
    outputs = [None, None]
    while True:
        # grab next output
        with locks[1]:
            if ampins[1] is not None:
                outputs[outp] = ampins[1]
                ampins[1] = None
                if outp == 0:
                    outp = 1
                else:
                    outp = 0
                    print()
                    print("using outputs:",outputs)
                    # get output
                    paintColor = outputs[0]
                    newdir = outputs[1]

                    # paint the current spot
                    panels[loc] = paintColor
                    print("painted ", loc, " ", paintColor)
                    print("panels", panels)

                    # move the robot
                    loc1, loc2, robotdir = moveRobot(loc, robotdir, newdir)
                    loc = (loc1, loc2)
                    print("robot now at:", loc, robotdir)

                    with locks[0]:
                        # set the color for the new spot
                        if panels.get(loc) is not None:
                            ampins[0] = panels[loc]
                        else:
                            ampins[0] = 0 # black by default
                        print("after moving: ", ampins)
        with runninglock:
            if not running:
                print("FINAL panels", panels)
                print(len(panels.keys()))
                return
        time.sleep(2)

def part1(data):
    print(data)
    for _ in range(0, 2000):
        data.append(0)
    # output = []
    relativeBase = 0
    # running = True
    # mem = [True, 0, None, None]

    ampins = [None for _ in range(0, 2)]

    # start robot
    # color = 1 # black by default
    t1 = threading.Thread(target=ampintcode, args=(data.copy(), 0, ampins, 0, relativeBase))
    t2 = threading.Thread(target=controlRobot, args=(ampins,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()



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

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    # print("\nPART 2 RESULT")
    # runpart2()
