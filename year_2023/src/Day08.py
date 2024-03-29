import time
from math import gcd

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return self.value + " = " + "(" + self.left + ", " + self.right + ")"

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        i = 0
        directions = ""
        nodes = {}
        for line in file:
            line = line.strip()
            if i == 0:
                directions = line
            elif i > 1:
                s1 = line.split(" = ")
                value = s1[0]
                s2 = s1[1].strip("(").strip(")").split(", ")
                left = s2[0]
                right = s2[1]
                nodes[value] = Node(value, left, right)
            i += 1
        return directions, nodes

def part1():
    directions, nodes = parseInput(8)
    # print(directions)
    # for node in nodes:
    #     print(nodes[node])

    curr_node = nodes["AAA"]
    i = 0
    steps = 0
    while True:
        # print(curr_node)
        if curr_node.value == "ZZZ":
            break
        if i >= len(directions):
            i = 0
        next_direction = directions[i]
        # print("going", next_direction)
        if next_direction == "L":
            curr_node = nodes[curr_node.left]
        else:
            curr_node = nodes[curr_node.right]
        i += 1
        steps += 1
    print("steps", steps)

def stepNode(node_value, nodes, directions):
    curr_node = nodes[node_value]
    i = 0
    steps = 0
    while True:
        # print(curr_node)
        if curr_node.value[-1] == "Z":
            break
        if i >= len(directions):
            i = 0
        next_direction = directions[i]
        # print("going", next_direction)
        if next_direction == "L":
            curr_node = nodes[curr_node.left]
        else:
            curr_node = nodes[curr_node.right]
        i += 1
        steps += 1
    # print("steps", steps)
    return steps

def part2():
    directions, nodes = parseInput(8)

    # find every node that ends with A
    curr_nodes = []
    for node in nodes:
        if node[-1] == "A":
            curr_nodes.append(nodes[node])

    steps = []
    for curr_node in curr_nodes:
        s = stepNode(curr_node.value, nodes, directions)
        # print(curr_node, "steps:", s)
        steps.append(s)

    # lcm: https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
    lcm = 1
    for i in steps:
        lcm = lcm * i // gcd(lcm, i)
    print(lcm)


if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
