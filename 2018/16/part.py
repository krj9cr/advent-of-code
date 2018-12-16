# addr (add register) stores into register C the result of adding register A and register B.
def addr(registers, instr):
    valA = registers[instr[1]]
    valB = registers[instr[2]]
    registers[instr[3]] = valA + valB
    return registers

# addi (add immediate) stores into register C the result of adding register A and value B.
def addi(registers, instr):
    valA = registers[instr[1]]
    valB = instr[2]
    registers[instr[3]] = valA + valB
    return registers

# mulr (multiply register) stores into register C the result of multiplying register A and register B.
def mulr(registers, instr):
    valA = registers[instr[1]]
    valB = registers[instr[2]]
    registers[instr[3]] = valA * valB
    return registers

# muli (multiply immediate) stores into register C the result of multiplying register A and value B.
def muli(registers, instr):
    valA = registers[instr[1]]
    valB = instr[2]
    registers[instr[3]] = valA * valB
    return registers

# banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
def banr(registers, instr):
    valA = registers[instr[1]]
    valB = registers[instr[2]]
    registers[instr[3]] = valA & valB
    return registers

# bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
def bani(registers, instr):
    valA = registers[instr[1]]
    valB = instr[2]
    registers[instr[3]] = valA & valB
    return registers

# borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
def borr(registers, instr):
    valA = registers[instr[1]]
    valB = registers[instr[2]]
    registers[instr[3]] = valA | valB
    return registers

# bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
def bori(registers, instr):
    valA = registers[instr[1]]
    valB = instr[2]
    registers[instr[3]] = valA | valB
    return registers

# setr (set register) copies the contents of register A into register C. (Input B is ignored.)
def setr(registers, instr):
    valA = registers[instr[1]]
    registers[instr[3]] = valA
    return registers

# seti (set immediate) stores value A into register C. (Input B is ignored.)
def seti(registers, instr):
    valA = instr[1]
    registers[instr[3]] = valA
    return registers

# gtir (greater-than immediate/register)
# sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
def gtir(registers, instr):
    valA = instr[1]
    valB = registers[instr[2]]
    if valA > valB:
        registers[instr[3]] = 1
    else:
        registers[instr[3]] = 0
    return registers

# gtri (greater-than register/immediate)
# sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
def gtri(registers, instr):
    valA = registers[instr[1]]
    valB = instr[2]
    if valA > valB:
        registers[instr[3]] = 1
    else:
        registers[instr[3]] = 0
    return registers

# gtrr (greater-than register/register)
# sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
def gtrr(registers, instr):
    valA = registers[instr[1]]
    valB = registers[instr[2]]
    if valA > valB:
        registers[instr[3]] = 1
    else:
        registers[instr[3]] = 0
    return registers

# eqir (equal immediate/register)
# sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
def eqir(registers, instr):
    valA = instr[1]
    valB = registers[instr[2]]
    if valA == valB:
        registers[instr[3]] = 1
    else:
        registers[instr[3]] = 0
    return registers

# eqri (equal register/immediate)
# sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
def eqri(registers, instr):
    valA = registers[instr[1]]
    valB = instr[2]
    if valA == valB:
        registers[instr[3]] = 1
    else:
        registers[instr[3]] = 0
    return registers

# eqrr (equal register/register)
# sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
def eqrr(registers, instr):
    valA = registers[instr[1]]
    valB = registers[instr[2]]
    if valA == valB:
        registers[instr[3]] = 1
    else:
        registers[instr[3]] = 0
    return registers


def parseInput(path: str):
    sets = []
    nextSet = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if "Before: " in line:
                line = line.replace("Before: ", "").replace("[", "").replace("]", "").split(",")
                nextSet = [[int(l) for l in line]]
            elif "After: " in line:
                line = line.replace("After: ", "").replace("[", "").replace("]", "").split(",")
                nextSet.append([int(l) for l in line])
                sets.append(nextSet)
            else:
                line = line.split(" ")
                nextSet.append([int(l) for l in line])
    return sets


def parseProgram(path: str):
    instructions = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            line = line.split(" ")
            instructions.append([int(l) for l in line])
    return instructions


def part1(path: str):
    operations = ["addr", "addi", "mulr", "muli",
                  "banr", "bani", "borr", "bori",
                  "setr", "seti", "gtir", "gtri",
                  "gtrr", "eqir", "eqri", "eqrr",]

    instructionSets = parseInput(path)
    print(instructionSets)

    counts = []
    # for each example of instructionSets
    for instructionSet in instructionSets:
        count = 0
        before = instructionSet[0]
        instruction = instructionSet[1]
        after = instructionSet[2]
        # try each function
        for op in operations:
            actual = globals()[op](before.copy(), instruction)
            if actual == after:
                count += 1
        counts.append(count)
    print(counts)
    answer = 0
    for count in counts:
        if count >= 3:
            answer += 1
    print("part1:", answer)


def part2(path1: str, path2: str):
    operations = ["addr", "addi", "mulr", "muli",
                  "banr", "bani", "borr", "bori",
                  "setr", "seti", "gtir", "gtri",
                  "gtrr", "eqir", "eqri", "eqrr"]

    instructionSets = parseInput(path1)

    counts = []
    opCodes = {}
    for i in range(0, len(operations)):
        opCodes[i] = set()

    # for each example of instructionSets
    for instructionSet in instructionSets:
        count = 0
        before = instructionSet[0]
        instruction = instructionSet[1]
        after = instructionSet[2]
        # try each function
        for op in operations:
            actual = globals()[op](before.copy(), instruction)
            if actual == after:
                opCodes[instruction[0]].add(op)
        counts.append(count)

    # figure out each opcode
    codeLookup = {}
    while opCodes:
        for i in range(0, len(operations)):
            if opCodes.get(i) is not None:
                if len(opCodes[i]) == 1:
                    operation = opCodes[i].pop()
                    codeLookup[i] = operation
                    for j in range(0, len(operations)):
                        if i != j:
                            if opCodes.get(j) is not None:
                                if operation in opCodes[j]:
                                    opCodes[j].remove(operation)

                    del opCodes[i]
    print(codeLookup)

    # execute program
    registers = [0, 0, 0, 0]
    program = parseProgram(path2)
    # print(program)
    for instruction in program:
        opCode = instruction[0]
        functionName = codeLookup[opCode]
        registers = globals()[functionName](registers, instruction)
    print("part2:", registers)
