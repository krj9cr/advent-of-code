from copy import deepcopy

# custom intcoder for today
class Intcode:
    def __init__(self, initial_state=None, intcode_input_callback=None, extra_mem=2000, debug=False, address=0):
        self.initial_state = initial_state
        self.intcode_input_callback = intcode_input_callback
        self.intcode_input_index = 0
        self.address = address

        self.state = self.initial_state[:]
        for _ in range(0, extra_mem):
            self.state.append(0)
        self.relativeBase = 0
        self.ip = 0
        self.output = []
        self.running = True
        self.debug = debug

    def parseOp(self, op):
        s = str(op)
        numZerosAdd = 5 - len(s)
        zeros = ""
        for i in range(0, numZerosAdd):
            zeros += "0"
        s = zeros + s
        modes = s[0:3]
        op = s[3:]
        return [int(m) for m in reversed(modes)], int(op)

    def getNextOp(self):
        # self.validateMem(self.ip)
        return self.parseOp(self.state[self.ip])

    def validateMem(self, mem):
        if mem > len(self.state) or mem < 0:
            print("BAD MEMORY LOCATION", mem)
            exit(1)

    def getArgs(self, modes, numArgs=3, write=False):
        args = []
        for i in range(0, numArgs):
            arg = self.ip + i + 1
            arg = self.state[arg]
            if i == 2 or write:
                if modes[i] == 2:
                    arg += self.relativeBase
            else:
                if modes[i] == 0:
                    arg = self.state[arg]
                elif modes[i] == 2:
                    arg = self.state[self.relativeBase + arg]
            args.append(arg)
        return args

    def op1(self, args):
        arg1, arg2, arg3 = args
        self.state[arg3] = arg1 + arg2
        self.ip += 4

    def op2(self, args):
        arg1, arg2, arg3 = args
        self.state[arg3] = arg1 * arg2
        self.ip += 4

    def op3(self, args):
        arg1 = args[0]
        if callable(self.intcode_input_callback):
            input_val = self.intcode_input_callback(self.intcode_input_index, self.address)
        else:
            input_val = self.intcode_input_callback[self.intcode_input_index]
        self.intcode_input_index += 1
        if self.debug:
            print("writing to", arg1, "value", input_val)
        self.state[arg1] = input_val
        self.ip += 2

    def op4(self, args):
        arg1 = args[0]
        self.output.append(arg1)
        self.ip += 2

    def op5(self, args):
        arg1, arg2 = args
        if arg1 != 0:
            self.ip = arg2
        else:
            self.ip += 3

    def op6(self, args):
        arg1, arg2 = args
        if arg1 == 0:
            self.ip = arg2
        else:
            self.ip += 3

    def op7(self, args):
        arg1, arg2, arg3 = args
        if arg1 < arg2:
            self.state[arg3] = 1
        else:
            self.state[arg3] = 0
        self.ip += 4

    def op8(self, args):
        arg1, arg2, arg3 = args
        if arg1 == arg2:
            self.state[arg3] = 1
        else:
            self.state[arg3] = 0
        self.ip += 4

    def op9(self, args):
        arg1 = args[0]
        self.relativeBase += arg1
        self.ip += 2

    def runOp(self, modes, op):
        if op == 99:
            self.running = False
            return
        if self.debug:
            print("ip", self.ip, "modes", modes, "op", op, "relativeBase", self.relativeBase)
        if op == 1:
            args = self.getArgs(modes, 3)
            self.op1(args)
        elif op == 2:
            args = self.getArgs(modes, 3)
            self.op2(args)
        elif op == 3:
            args = self.getArgs(modes, 1, write=True)
            self.op3(args)
        elif op == 4:
            args = self.getArgs(modes, 1)
            self.op4(args)
            if self.debug:
                print("intcode output", self.output)
        elif op == 5:
            args = self.getArgs(modes, 2)
            self.op5(args)
        elif op == 6:
            args = self.getArgs(modes, 2)
            self.op6(args)
        elif op == 7:
            args = self.getArgs(modes, 3)
            self.op7(args)
        elif op == 8:
            args = self.getArgs(modes, 3)
            self.op8(args)
        elif op == 9:
            args = self.getArgs(modes, 1)
            self.op9(args)
        else:
            print("BAD OPCODE:", op)
            exit(1)

    def step(self):
        if self.running:
            if self.debug:
                print("state",self.state)
            modes, op = self.getNextOp()
            self.runOp(modes, op)
        else:
            print("ERROR: tried to step after completing program")
            exit(1)

    def run(self):
        while self.running:
            self.step()



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
def part1(data):
    print(data)
    num_computers = 50
    packets = []

    # initialize inputs
    inputs = []
    for i in range(num_computers):
        inputs.append([i])

    def intcoder_callback(inpi, address):
        if inpi == 0:
            return address
        # check if there is a packet for it
        for packet in packets:
            if packet[0] == address:
                if packet[3] == 0:
                    packet[3] = 1
                    return packet[1]
                else:
                    val = packet[2]
                    packets.remove(packet)
                    return val
        return -1

    # initialize intcoders
    intcoders = []
    for i in range(num_computers):
        intcoders.append(Intcode(deepcopy(data), intcoder_callback, address=i))

    # packet queue
    while True:
        # check outputs
        for intcoder in intcoders:
            if len(intcoder.output) == 3:
                o = intcoder.output
                o.append(0)
                packets.append(o)
                intcoder.output = []
            intcoder.step()
        # check packets for end condition
        for packet in packets:
            if packet[0] == 255:
                print("answer",packet[2])
                exit(0)


def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)
    num_computers = 50
    packets = []
    nat = []
    natdelivered = []
    idlecount = 0

    # initialize inputs
    inputs = []
    for i in range(num_computers):
        inputs.append([i])

    def intcoder_callback(inpi, address):
        if inpi == 0:
            return address
        # check if there is a packet for it
        for packet in packets:
            if packet[0] == address:
                if packet[3] == 0:
                    packet[3] = 1
                    return packet[1]
                else:
                    val = packet[2]
                    packets.remove(packet)
                    return val
        return -1

    # initialize intcoders
    intcoders = []
    for i in range(num_computers):
        intcoders.append(Intcode(deepcopy(data), intcoder_callback, address=i))

    # packet queue
    while True:
        # check outputs
        for intcoder in intcoders:
            if len(intcoder.output) == 3:
                o = intcoder.output
                o.append(0)
                if o[0] == 255:
                    nat = deepcopy(o)
                else:
                    packets.append(o)
                intcoder.output = []
            intcoder.step()

        # check for idleness
        if len(packets) == 0:
            idlecount += 1
        if idlecount >= 2000:
            idlecount = 0
            # send last nat packet to address 0
            packet = deepcopy(nat)
            packet[0] = 0
            packets.append(packet)

            # check if we've sent this Y before
            if len(natdelivered) > 0 and packet[2] == natdelivered[-1]:
                print(natdelivered)
                print("answer", packet[2])
                exit(0)
            else:
                natdelivered.append(packet[2])

# 22134 too high

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
