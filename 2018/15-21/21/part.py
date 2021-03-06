# noop
def noop(registers, instr):
    return registers

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


def parseProgram(path: str):
    instructions = []
    with open(path, 'r') as file:
        ip = int(file.readline().split(" ")[1]);
        for line in file:
            line = line.strip()
            line = line.split(" ")
            instructions.append([line[0], int(line[1]), int(line[2]), int(line[3])])
    return ip, instructions

# part1 completed by inspection
# print out registers and instructions for each instruction,
# use the first number that is compared against in the exit check
# (the value of the register being compared to in the first eqrr operation)

# at the point where it checks to exit (eqrr operation),
# print out the register we're comparing against until that number is no longer repeated
# the answer is the last number that is printed
def part2(path: str):
    ip, program = parseProgram(path)
    boundRegister = ip

    reg0 = 0
    seenr1 = []
    registers = [reg0, 0, 0, 0, 0, 0]
    ip = registers[boundRegister]
    while ip < len(program):
        instruction = program[ip]
        registers[boundRegister] = ip
        op = instruction[0]
        if op == "eqrr":
            if registers[1] not in seenr1:
                seenr1.append(registers[1])
                print(seenr1[-1])
        registers = globals()[op](registers, instruction)
        ip = registers[boundRegister]
        ip += 1
