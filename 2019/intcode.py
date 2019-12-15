
class Intcode:
    def __init__(self, initial_state=None, intcode_input=None, extra_mem=2000, debug=False):
        self.initial_state = initial_state
        self.intcode_input = intcode_input

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

    def getNextParams(self, modes, arg1write=False):
        # self.validateMem(self.ip + 3)
        arg1 = self.ip + 1
        arg2 = self.ip + 2
        arg3 = self.ip + 3

        arg1 = self.state[arg1]
        arg2 = self.state[arg2]
        arg3 = self.state[arg3]

        # adjust arg1
        if arg1write:
            if modes[0] == 0:
                arg1 = self.state[arg1]
            elif modes[0] == 2:
                arg1 += self.relativeBase
        else:
            if modes[0] == 0:
                # self.validateMem(arg1)
                arg1 = self.state[arg1]
            elif modes[0] == 2:
                mem = self.relativeBase + arg1
                # self.validateMem(mem)
                arg1 = self.state[mem]

        # adjust arg2
        if modes[1] == 0:
            # self.validateMem(arg2)
            arg2 = self.state[arg2]
        elif modes[1] == 2:
            mem = self.relativeBase + arg2
            # self.validateMem(mem)
            arg2 = self.state[mem]

        # adjust arg3, assume we are writing to this location
        # if modes[2] == 0:
        #     # self.validateMem(arg3)
        #     arg3 = self.state[arg3]
        if modes[2] == 2:
            arg3 += self.relativeBase
            # self.validateMem(arg3)
        return arg1, arg2, arg3

    def op1(self, args):
        arg1, arg2, arg3 = args
        self.state[arg3] = arg1 + arg2
        self.ip += 4

    def op2(self, args):
        arg1, arg2, arg3 = args
        self.state[arg3] = arg1 * arg2
        self.ip += 4

    def op3(self, modes, args):
        # arg1 = self.ip + 1
        # if modes[0] == 0:
        #     arg1 = self.state[arg1]
        # elif modes[0] == 2:
        #     arg1 += self.relativeBase
        arg1 = args[0]
        if self.debug:
            print("writing to",arg1, "value",self.intcode_input[-1])
        self.state[arg1] = self.intcode_input[-1]
        self.ip += 2

    def op4(self, args):
        arg1, arg2, arg3 = args
        self.output.append(arg1)
        self.ip += 2

    def op5(self, args):
        arg1, arg2, arg3 = args
        if arg1 != 0:
            self.ip = arg2
        else:
            self.ip += 3

    def op6(self, args):
        arg1, arg2, arg3 = args
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
        arg1, arg2, arg3 = args
        self.relativeBase += arg1
        self.ip += 2

    def step(self):
        if self.running:
            if self.debug:
                print("state",self.state)
            modes, op = self.getNextOp()
            if op == 99:
                self.running = False
                return
            args = self.getNextParams(modes)
            if op == 3:
                args = self.getNextParams(modes, arg1write=True)
            if self.debug:
                print("ip",self.ip,"modes",modes,"op",op, "args",args,"relativeBase", self.relativeBase)
            if op == 1:
                self.op1(args)
            elif op == 2:
                self.op2(args)
            elif op == 3:
                if self.debug:
                    print("using input", self.intcode_input[-1])
                self.op3(modes,args)
            elif op == 4:
                self.op4(args)
                if self.debug:
                    print("intcode output", self.output)
            elif op == 5:
                self.op5(args)
            elif op == 6:
                self.op6(args)
            elif op == 7:
                self.op7(args)
            elif op == 8:
                self.op8(args)
            elif op == 9:
                self.op9(args)
            else:
                print("BAD OPCODE:",op)
                exit(1)
        else:
            print("ERROR: tried to step after completing program")
            exit(1)

    def run(self):
        while self.running:
            self.step()
