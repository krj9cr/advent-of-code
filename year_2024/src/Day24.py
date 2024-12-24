import copy
import time

class Gate:
    def __init__(self, input1, input2, op, output):
        self.input1 = input1
        self.input2 = input2
        self.op = op
        self.output = output

    def __str__(self):
        return f"{self.input1} {self.op} {self.input2} -> {self.output}"

    def do_op(self, wires):
        if wires.get(self.input1) is None or wires.get(self.input2) is None:
            return False
        a = wires[self.input1]
        b = wires[self.input2]
        output = 0
        if self.op == 'AND':
            if a == 1 and b == 1:
                output = 1
        elif self.op == 'OR':
            if a == 1 or b == 1:
                output = 1
        elif self.op == 'XOR':
            if a != b:
                output = 1
        wires[self.output] = output
        return True

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        wires = {}
        gates = []
        parsing_gates = False
        for line in file:
            line = line.strip()
            if line == "":
                parsing_gates = True
                continue
            if parsing_gates:
                linesplit = line.split(" -> ")
                first = linesplit[0].split(" ")
                output_wire = linesplit[1]
                gates.append(Gate(first[0], first[2], first[1], output_wire))
            else:
                linesplit = line.split(": ")
                wire = linesplit[0]
                value = int(linesplit[1])
                wires[wire] = value
        return wires, gates

def part1():
    initial_wires, gates = parseInput(24)

    wires = copy.deepcopy(initial_wires)
    print(wires)

    # have the gates run
    # TODO: keep going until they all actually run
    seen_gates = set()
    num_gates = len(gates)
    num_processed_gates = 0
    while num_processed_gates < num_gates:
        for i in range(num_gates):
            gate = gates[i]
            if i in seen_gates:
                continue
            processed = gate.do_op(wires)
            if processed:
                seen_gates.add(i)
                num_processed_gates += 1
                print(wires)

    # get all the z outputs
    max_z = 45  # for my input
    # max_z = 12     # example 2
    # max_z = 2     # example 1
    bits = ""
    for z in range(max_z, -1, -1):
        z_output = f'z{z:02}'
        bits += str(wires[z_output])
    print(bits)
    print(int(bits, 2))

def part2():
    lines = parseInput(24)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
