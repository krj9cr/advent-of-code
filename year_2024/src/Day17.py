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

    # A:  25184372085147      2,0,5,5,0,2,5,5,7,5,1,4,1,6,4   len: 15
    # A:  29184372134691      1,0,5,5,4,4,2,1,4,2,1,4,3,0,5   len: 15
    # A:  33000000047777      3,6,3,4,3,0,0,0,4,6,6,5,3,3,0   len: 15
    # A:  35184371436132      0,5,1,4,6,1,2,0,0,0,0,0,0,0,0   len: 15
    # everything becomes zero right before the next digit is appended
    # A:  35184372088831      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   len: 15
    # A:  35184372084882      6,2,4,7,0,0,0,0,0,0,0,0,0,0,0   len: 15
    # A:  35184372088832      0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,1 len: 16
    # A:  40000000013320      0,3,5,0,1,0,1,1,5,0,4,4,5,0,1,1 len: 16
    # A:  50000000021238      5,1,7,3,0,1,0,0,3,5,5,3,0,0,3,1 len: 16
    # A:  60000000031623      0,6,1,2,3,2,1,0,5,3,0,6,4,6,6,1 len: 16
    # A:  70000000111611      4,0,0,1,0,4,4,5,4,4,5,0,5,0,0,1 len: 16
    # A:  80000000034386      0,4,1,7,2,1,4,7,4,1,5,0,5,3,2,2 len: 16
    # A:  90000000046774      5,5,0,1,4,0,6,4,4,6,5,6,2,1,6,2 len: 16
    # A: 100000000028810      6,1,4,2,1,0,1,3,6,1,5,4,0,0,5,2 len: 16
    # A: 110000000038833      7,5,1,0,0,4,0,0,1,5,6,4,4,1,1,3 len: 16
    # A: 150000000120000      1,5,6,6,2,1,1,4,1,2,7,5,5,2,3,4 len: 16
    # A: 200000000100000      5,6,2,3,6,1,2,0,4,4,7,4,1,5,6,4 len: 16
    # A: 220000000100000      5,6,2,1,2,5,5,1,2,0,0,3,3,3,3,5 len: 16
    # A: 240000000100000      5,6,2,7,0,7,5,5,0,5,2,1,0,2,5,5 len: 16
    # A: 245000000100000      5,6,0,5,2,4,1,0,7,4,1,4,6,2,0,5 len: 16
    # A: 246200000140000      5,7,7,3,0,2,5,3,0,7,1,0,1,0,0,5 len: 16
    # A: 246290500150000      5,1,3,2,1,3,0,1,6,0,0,0,0,0,0,5 len: 16
    # A: 246290600110000      7,5,1,2,7,5,1,2,0,0,0,0,0,0,0,5 len: 16
    # A: 246290601000000      0,7,2,1,3,7,5,1,0,0,0,0,0,0,0,5 len: 16
    # A: 246290604500000      0,4,1,2,5,3,0,0,0,0,0,0,0,0,0,5 len: 16
    # A: 246290604621823      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5 len: 16
    # last digit is zero after increasing from 1-5
    # A: 246290604621824      0,0,0,0,0,0,0,0,0,0,0,0,4,3,0,0 len: 16
    # A: 250000000133621      0,1,0,6,3,0,5,4,7,0,1,0,0,5,0,0 len: 16
    # A: 260000000100724      2,1,4,0,7,7,6,2,0,1,0,0,0,3,0,0 len: 16
    # A: 264000000146687      0,0,4,1,1,0,1,0,0,4,6,6,5,3,3,0 len: 16
    # A: 264000000144028      7,6,4,4,1,0,1,0,0,4,6,6,5,3,3,0 len: 16
    # A: 264350000156771      5,5,0,3,7,5,5,1,0,3,0,5,5,3,3,0 len: 16
    # A: 264430000197099      5,2,0,5,1,0,1,4,6,6,2,0,0,3,3,0 len: 16
    # A: 264432500189951      0,0,1,0,4,4,0,6,2,0,0,0,0,3,3,0 len: 16
    # A: 264400000195517      2,0,1,6,4,1,4,6,1,6,6,3,0,3,3,0 len: 16
    # A: 264432000186853      4,3,0,7,3,5,7,4,0,4,0,0,0,3,3,0 len: 16
    # A: 264432540228851      4,1,4,1,1,4,7,2,0,0,0,0,0,3,3,0 len: 16
    # A: 264432548038365      2,6,2,5,3,0,4,0,0,0,4,0,6,6,3,0 len: 16
    # A: 264450000204086      5,5,4,2,1,4,6,6,0,6,4,0,6,6,3,0 len: 16
    # A: 264500000193854      1,0,2,1,0,2,1,0,2,5,1,0,6,6,3,0 len: 16
    # A: 264600000202162      7,5,5,6,0,2,4,7,2,0,2,6,2,6,3,0 len: 16
    # A: 265000000154857      2,2,0,5,1,0,0,5,1,3,0,6,6,5,3,0 len: 16
    # A: 264480000127119      0,1,4,5,6,5,2,5,5,4,1,4,6,6,3,0 len: 16
    # A: 265000000000000      0,4,4,5,6,0,0,5,1,3,0,6,6,5,3,0 len: 16
    # A: 265000000145113      2,6,2,5,3,0,0,5,1,3,0,6,6,5,3,0 len: 16
    # A: 265398000000000      0,7,4,1,1,0,4,5,2,1,3,1,5,5,3,0 len: 16
    # A: 265398900130000      1,2,3,2,5,0,4,6,0,0,3,1,5,5,3,0 len: 16
    # A: 265398917880000      1,6,5,1,0,1,1,1,2,0,4,1,5,5,3,0 len: 16
    # A: 265398934460000      4,5,4,1,4,1,6,1,5,0,4,1,5,5,3,0 len: 16
    # ran everything in between 265398900130000 and 265398943330000
    # A: 265398943330000      5,4,0,0,4,4,0,6,5,0,4,1,5,5,3,0 len: 16
    # 265398943330000 TOO LOW LET'S GOOOO
    # A: 265398972840000      0,6,6,3,0,0,0,2,3,0,4,1,5,5,3,0 len: 16
    # A: 265398972850000      6,5,2,0,1,6,1,7,3,0,4,1,5,5,3,0 len: 16
    # A: 265399000000000      4,1,3,0,5,3,0,0,4,0,4,1,5,5,3,0 len: 16
    # A: 265399000189125      4,2,1,0,6,0,2,1,4,0,4,1,5,5,3,0 len: 16
    # A: 265399006640000      7,5,1,6,0,0,2,1,4,0,4,1,5,5,3,0 len: 16
    # A: 265399019120000      3,1,5,2,3,4,3,3,5,0,4,1,5,5,3,0 len: 16
    # A: 265399033620000      4,4,3,0,5,1,0,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265399033630000      2,5,2,5,3,0,0,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265399033640000      0,5,2,4,4,0,0,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265399033650000      6,1,6,6,2,0,0,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265399033660000      4,5,1,1,4,4,3,1,0,0,4,1,5,5,3,0 len: 16
    # A: 265399044850000      2,3,4,2,1,0,5,1,0,0,4,1,5,5,3,0 len: 16
    # A: 265399053390000      1,5,0,5,2,6,2,0,2,1,4,1,5,5,3,0 len: 16
    # ran everything in between 265398943330000 and 265399067600000
    # A: 265399067600000      1,1,6,5,1,7,0,0,5,1,4,1,5,5,3,0 len: 16
    # not everything in between was checked for the below rows
    # A: 265399167600000      3,1,5,5,3,0,5,0,0,1,4,1,5,5,3,0 len: 16
    # A: 265399267600000      5,1,6,6,2,1,4,1,0,3,4,1,5,5,3,0 len: 16
    # A: 265399268430000      1,5,0,6,4,3,0,1,0,3,4,1,5,5,3,0 len: 16
    # A: 265399278430000      6,5,7,4,1,6,6,6,0,3,4,1,5,5,3,0 len: 16
    # A: 265399285160000      0,6,0,5,6,0,0,1,5,3,4,1,5,5,3,0 len: 16
    # checking everything after
    # A: 265399294570000      4,4,1,0,4,0,1,0,5,3,4,1,5,5,3,0 len: 16
    # A: 265399302190000      7,5,1,3,0,0,3,3,0,3,4,1,5,5,3,0 len: 16
    # A: 265399304610000      1,2,3,6,5,5,6,7,0,3,4,1,5,5,3,0 len: 16
    # A: 265399307590000      2,1,4,1,2,0,7,0,0,3,4,1,5,5,3,0 len: 16
    # A: 265399307600000      1,0,2,4,6,5,2,0,0,3,4,1,5,5,3,0 len: 16
    # A: 265399353390000      7,5,1,4,5,2,3,2,2,1,4,1,5,5,3,0 len: 16
    # A: 265399398690000      1,6,0,5,1,7,6,0,7,1,4,1,5,5,3,0 len: 16
    # A: 265399413700000      3,2,5,1,0,6,4,1,2,1,4,1,5,5,3,0 len: 16
    # skipping
    # A: 265399513700000      5,6,0,5,6,4,0,2,1,0,4,1,5,5,3,0 len: 16
    # A: 265399585000000      4,2,5,4,5,6,0,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265399585210000      5,4,5,0,0,0,0,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265399585220000      3,2,5,2,2,0,4,2,2,4,4,1,5,5,3,0 len: 16
    # A: 265399585500000      6,1,6,0,5,0,1,2,2,4,4,1,5,5,3,0 len: 16
    # A: 265399585700000      1,6,5,3,0,1,1,2,2,4,4,1,5,5,3,0 len: 16
    # A: 265399593700000      5,6,3,4,0,3,4,4,2,4,4,1,5,5,3,0 len: 16
    # A: 265399613700000      7,2,1,6,1,4,1,6,5,4,4,1,5,5,3,0 len: 16
    # A: 265399999410000      6,5,2,0,2,2,1,4,2,0,4,1,5,5,3,0 len: 16
    # 265399999410000 TOO LOW
    # A: 265400000181991      0,7,6,4,0,0,1,4,2,0,4,1,5,5,3,0 len: 16

    # A: 265400027400000      6,1,2,1,2,5,5,2,0,0,4,1,5,5,3,0 len: 16
    # A: 265401027400000      2,4,4,6,4,1,2,0,2,0,4,1,5,5,3,0 len: 16
    # A: 265401028000000      2,6,0,7,4,1,0,0,2,0,4,1,5,5,3,0 len: 16
    # A: 265401028100000      7,2,1,0,3,1,7,7,1,0,4,1,5,5,3,0 len: 16
    # A: 265401033600000      0,3,5,5,0,3,0,5,1,0,4,1,5,5,3,0 len: 16
    # A: 265401060000000      2,0,4,7,4,0,6,0,0,0,4,1,5,5,3,0 len: 16
    # A: 265401061600000      6,2,1,0,1,0,0,0,0,0,4,1,5,5,3,0 len: 16
    # 265401061600000 TOO LOW OMG
    a = 265401061600000
    # ran 265401061600000 through to the below
    # A: 265401067870000      6,5,7,7,6,0,0,2,3,0,5,1,5,5,3,0 len: 16

    # A: 265401061610000      4,0,0,1,1,0,0,0,3,0,5,1,5,5,3,0 len: 16
    # A: 265401070000000      7,5,1,3,1,2,0,4,3,0,5,1,5,5,3,0 len: 16
    # A: 265401100000000      6,6,1,6,2,2,6,2,6,0,5,1,5,5,3,0 len: 16
    # A: 265401200000000      0,7,5,1,4,0,0,0,3,1,5,1,5,5,3,0 len: 16
    # A: 265402027400000      6,6,6,6,6,5,0,5,7,0,5,1,5,5,3,0 len: 16
    # A: 265405027400000      2,6,4,7,2,4,6,5,1,6,7,3,5,5,3,0 len: 16
    # A: 265410027400000      6,2,6,0,1,1,7,0,5,1,1,3,5,5,3,0 len: 16
    # A: 265405000260000      3,2,5,5,1,5,5,5,1,6,7,3,5,5,3,0 len: 16
    # A: 265410000260000      7,2,1,4,1,6,3,5,6,1,1,3,5,5,3,0 len: 16
    # A: 265420000250000      1,2,3,0,5,7,0,5,3,2,0,7,5,5,3,0 len: 16
    # A: 265450000190000      4,5,4,4,6,0,2,0,0,7,0,5,5,5,3,0 len: 16
    # A: 270000000330237      2,0,0,2,1,0,5,4,5,4,0,5,4,5,2,0 len: 16
    # zeros are starting to appear at the end
    # A: 275000000369828      0,6,0,5,2,1,0,1,6,6,0,1,7,2,1,0 len: 16
    # A: 280000000108883      6,3,4,6,7,5,3,0,6,2,7,6,5,2,0,0 len: 16
    # A: 280100000150688      1,6,4,0,1,4,6,5,2,4,0,0,5,2,0,0 len: 16
    # A: 280100006460000      4,5,6,2,0,4,6,5,2,4,0,0,5,2,0,0 len: 16
    # A: 280100100270000      7,5,1,0,5,2,1,0,5,3,0,0,5,2,0,0 len: 16
    # A: 280102100250000      3,7,5,5,5,0,3,2,0,3,5,6,1,2,0,0 len: 16
    # A: 281000000175046      5,6,0,2,2,1,5,4,4,6,4,7,6,0,0,0 len: 16
    # A: 281400000330000      2,3,0,7,4,1,7,0,3,6,7,0,1,0,0,0 len: 16
    # A: 281440000550000      0,1,3,2,3,4,5,4,6,4,0,4,0,0,0,0 len: 16
    # A: 281500000175046      longer output

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
        # print("A:", a, "    ", output_str, "len:", len(output))
        if a % 10000 == 0:
            print("A:", a, "    ", output_str, "len:", len(output))


        a += 1

    print("A:", a, "    ", output_str, "len:", len(output))

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
