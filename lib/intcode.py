
# convert a list of integers to an ascii string,
# inserting newlines as necessary
# effectively taking intcode output and printing it nicely
def intcodeOutputToAscii(output: list[int]):
    grid = []
    row = []
    for a in output:
        if a == 10 and len(row) > 0:
            grid.append(row[:])
            row = []
        else:
            row.append(str(chr(a)))
    return grid

# convert an ascii string to a list of integers
# effectively for the intcode to consume as input
def asciiToIntcodeInput(astr: str):
    result = []
    for s in astr:
        for char in s:
            result.append(ord(char))
    # add final newline if necessary
    if result[-1] != 10:
        result.append(10)
    return result

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
