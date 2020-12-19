import sys
import time
from anytree import AnyNode, RenderTree, PreOrderIter
from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return line.strip()

def idxOfEndParen(equation):
    stack = []
    for i in range(len(equation)):
        char = equation[i]
        if char == ")":
            stack.append(char)
        elif char == "(":
            stack.pop()
        if len(stack) == 0:
            return i

def parseEquation(equation):
    print(equation)
    if len(equation) == 0:
        return None
    char = equation[0]
    if len(equation) == 1:
        if char.isdigit():
            return AnyNode(type="num", data=int(char))
        else:
            print("HUH")
            sys.exit(1)
    else:
        if char.isdigit():
            num = int(char)
            op = equation[2]
            rest = equation[4:]
            return AnyNode(children=[AnyNode(type="num", data=num), parseEquation(rest)], type="op", data=op)
        elif char == ")":
            # find matching end paren
            idx = idxOfEndParen(equation)
            blob = equation[1:idx]
            rest = equation[idx+1:]
            n = None
            if len(rest) > 2 and (rest[1] == "*" or rest[1] == "+"):
                n = AnyNode(children=[parseEquation(blob), parseEquation(rest[3:])], type="op", data=rest[1])
                print("blob, rest",blob, rest)
            else:
                n = parseEquation(blob)
            return n

def solveEquation(root):
    if root.__getattribute__("type") == "num":
        return root.__getattribute__("data")
    else:
        op = root.__getattribute__("data")
        left = solveEquation(root.children[0])
        right = solveEquation(root.children[1])
        if op == "*":
            return left * right
        elif op == "+":
            return left + right
    print("BADNESS")
    sys.exit(1)

def doEquation(equation):
    # parse
    leaf = parseEquation(equation[::-1])
    root = deepcopy(leaf)
    while root.parent is not None:
        root = root.parent
    print(RenderTree(root))

    # iter to solve
    order = [node for node in PreOrderIter(root)]
    print(order)
    # solve
    return solveEquation(root)

###########################
# part1
###########################
def part1(data):
    print(data)
    result = 0
    for equation in data:
        val = doEquation(equation)
        print(equation, "=", val)
        result += val
    print("sum", result)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def part2(data):
    print(data)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\nPART 2 RESULT")
    # runpart2()
