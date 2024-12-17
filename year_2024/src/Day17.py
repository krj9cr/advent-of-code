import sys
import time
import re
import math

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        registers = {}
        program = []
        for line in file:
            line = line.strip()
            match = re.match(r"Register ([A-Z]): ([-0-9]+)", line)
            if match:
                registers[match.group(1)] = int(match.group(2))
            elif "Program" in line:
                linestrip = line.strip("Program: ")
                program = [int(char) for char in linestrip.split(",")]
        return registers, program

def combo_operand(operand, registers):
    if 0 <= operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    elif operand == 7:
        print("OH NO")
        sys.exit(1)
    else:
        print("HUH...")
        sys.exit(1)

# opcode 0
def adv(operand, registers):
    numerator = registers["A"]
    denominator = math.pow(2, combo_operand(operand, registers))
    answer = numerator // denominator
    registers["A"] = int(answer)

# opcode 1
def bxl(operand, registers):
    answer = registers["B"] ^ operand
    registers["B"] = answer

# opcode 2
def bst(operand, registers):
    answer = combo_operand(operand, registers) % 8
    registers["B"] = answer

# opcode 3
def jnz(operand, registers):
    a = registers["A"]
    if a == 0:
        return
    else:
        # set the instruction pointer, and the pointer does not increase by 2 after this
        return operand

# opcode 4
def bxc(operand, registers):
    answer = registers["B"] ^ registers["C"]
    registers["B"] = answer

# opcode 5
def out(operand, registers):
    answer = combo_operand(operand, registers) % 8
    # output this answer
    return answer

# opcode 6
def bdv(operand, registers):
    numerator = registers["A"]
    denominator = math.pow(2, combo_operand(operand, registers))
    answer = numerator // denominator
    registers["B"] = int(answer)

# opcode 7
def cdv(operand, registers):
    numerator = registers["A"]
    denominator = math.pow(2, combo_operand(operand, registers))
    answer = numerator // denominator
    registers["C"] = int(answer)

opcodes = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv
}

def part1():
    registers, program = parseInput(17)
    print(registers)
    print(program)

    ip = 0
    output = []
    while ip < len(program) - 1:
        opcode = program[ip]
        operand = program[ip+1]
        result = opcodes[opcode](operand, registers)
        # jump, resets instruction pointer
        if opcode == 3:
            if result is not None:
                ip = result
                # do not increase ip by 2
                continue
        # save output
        elif opcode == 5:
            if result is not None:
                output.append(result)
        ip += 2

    print(','.join([str(o) for o in output]))


def part2():
    registers, program = parseInput(17)

    input_str = ','.join([str(o) for o in program])
    input_size = len(program)
    print("input", input_str)

    a = 0
    while True:
        registers["A"] = a
        registers["B"] = 0
        registers["C"] = 0

        # run program
        ip = 0
        output = []
        longer_output = False
        while ip < len(program) - 1:
            opcode = program[ip]
            operand = program[ip+1]
            result = opcodes[opcode](operand, registers)
            # jump, resets instruction pointer
            if opcode == 3:
                if result is not None:
                    ip = result
                    # do not increase ip by 2
                    continue
            # save output
            elif opcode == 5:
                if result is not None:
                    output.append(result)
                    if len(output) > input_size:
                        longer_output = True
                        print("Longer output", ','.join([str(o) for o in output]))
                        break
            ip += 2

        if longer_output:
            break
        output_str = ','.join([str(o) for o in output])
        if input_str == output_str:
            break
        print("A:", a, "    ", output_str)

        a += 1

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
