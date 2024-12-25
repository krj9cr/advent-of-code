import copy
import itertools
import time
import networkx as nx
import matplotlib.pyplot as plt
import pydot
import scipy

class Gate:
    def __init__(self, input1, input2, op, output, gid):
        self.gid = gid
        self.input1 = input1
        self.input2 = input2
        self.op = op
        self.output = output

    def __str__(self):
        return f"{self.gid}: {self.input1} {self.op} {self.input2} -> {self.output}"

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
        gid = 0
        for line in file:
            line = line.strip()
            if line == "":
                parsing_gates = True
                continue
            if parsing_gates:
                linesplit = line.split(" -> ")
                first = linesplit[0].split(" ")
                output_wire = linesplit[1]
                gates.append(Gate(first[0], first[2], first[1], output_wire, gid))
                gid += 1
            else:
                linesplit = line.split(": ")
                wire = linesplit[0]
                value = int(linesplit[1])
                wires[wire] = value
        return wires, gates

def run_gates(gates, wires):
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

def get_register_bits(prefix, wires):
    bits = ""
    for z in range(46):
        register = f'{prefix}{z:02}'
        try:
            value = wires[register]
        except:
            break
        bits += str(value)
    # print(bits)
    return bits[::-1]

def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(str(int(n % b)))
        n //= b
    return digits[::-1]

def part1():
    initial_wires, gates = parseInput(24)

    wires = copy.deepcopy(initial_wires)
    print(wires)

    # have all the gates run
    run_gates(gates, wires)

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

def switch_gates(gate1, gate2):
    new_gate1 = copy.deepcopy(gate1)
    new_gate2 = copy.deepcopy(gate2)
    new_gate1.output = gate2.output
    new_gate2.output = gate1.output
    return new_gate1, new_gate2

def process_group_combo(first_pair, second_pair, gates, wires):
    new_gates = list(switch_gates(first_pair[0], first_pair[1])) + list(
        switch_gates(second_pair[0], second_pair[1]))
    tmp_gates = copy.deepcopy(gates)
    for new_gate in new_gates:
        tmp_gates[new_gate.gid] = new_gate
    run_gates(tmp_gates, wires)
    z_bits = get_register_bits("z", wires)
    return z_bits

def part2():
    initial_wires, gates = parseInput(24)
    wires = copy.deepcopy(initial_wires)
    for gate in gates:
        print(gate)
    print("num gates", len(gates))

    '''
    222 gates, choose 8 is big number
    then out of those, 3 possible pairings, so big number * 3
    '''

    # get all the x and y wires to check em out
    x_bits = get_register_bits("x", wires)
    x_value = int(x_bits, 2)
    print("X", x_bits, x_value)

    y_bits = get_register_bits("y", wires)
    y_value = int(y_bits, 2)
    print("Y", y_bits, y_value)

    desired_result = x_value + y_value
    desired_bits = ''.join(numberToBase(desired_result, 2))
    print("O", desired_bits, desired_result)

    # have all the gates run
    run_gates(gates, wires)

    # get all the z outputs
    z_bits = get_register_bits("z", wires)

    # which z's are wrong?
    if len(z_bits) < len(desired_bits):
        z_bits = "0" + z_bits
    print("Z", z_bits, int(z_bits, 2))

    # make a graph I GUESS ugh
    nodes = set()
    edges = set()

    G = nx.DiGraph()
    for gate in gates:
        nodes.add(gate.input1)
        nodes.add(gate.input2)
        nodes.add(gate.output)
        edges.add((gate.input1, gate.output))
        edges.add((gate.input2, gate.output))
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(G)

    # levels = nx.trophic_levels(G)
    # for key in levels:
    #     if key.startswith('z'):
    #         levels[key] = 5
    #     else:
    #         levels[key] = int(levels[key])
    # print(levels)
    # nx.set_node_attributes(G, levels, "level")

    my_pos = {}
    for i in range(45):
        x_name = f"x{i:02}"
        y_name = f"y{i:02}"
        my_pos[x_name] = [i, 50]
        my_pos[y_name] = [i + 0.5, 48]
        # find whatever nodes are output of dis
        for gate in gates:
            child = False
            if (gate.input1 == x_name and gate.input2 == y_name) or (gate.input2 == x_name and gate.input1 == y_name):
                my_pos[gate.output] = [i, 40]
                # need to "recurse" on this output.. how many outputs does it have?
                for gate2 in gates:
                    if gate2 == gate:
                        continue
                    # gate is a top-level thing wow, gate2 is below it
                    if gate.output == gate2.input1 or gate.output == gate2.input2:
                        my_pos[gate2.output] = [i, 30]
                        # check again
                        for gate3 in gates:
                            if gate3 == gate2 or gate3 == gate:
                                continue
                            if gate2.output == gate3.input1 or gate2.output == gate3.input2:
                                my_pos[gate3.output] = [i, 20]
                                # check AGAIN
                                for gate4 in gates:
                                    if gate4 == gate3 or gate4 == gate2 or gate4 == gate:
                                        continue
                                    if gate3.output == gate4.input1 or gate3.output == gate4.input2:
                                        my_pos[gate4.output] = [i, 10]
    # move all the z's to the bottom
    for i in range(46):
        node_name = f"z{i:02}"
        my_pos[node_name] = [i, 0]
        # find some stuff that outputs to this wire
        # for gate in gates:
        #     if gate.output == node_name:
        #         if gate.input1 not in my_pos:
        #             my_pos[gate.input1] = [i, 10]
        #         if gate.input2 not in my_pos:
        #             my_pos[gate.input2] = [i, 10]
    # make sure we got all the nodes
    for node in nodes:
        if node not in my_pos:
            print(node, "not in pos")
            my_pos[node] = [25, 25]
    plt.figure()
    nx.draw(G, my_pos, with_labels=True, node_size=100, font_size=10)
    plt.show()

    sus_nodes = ['y44', 'tgs', 'fsh', 'csg', 'wnn', ]


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
