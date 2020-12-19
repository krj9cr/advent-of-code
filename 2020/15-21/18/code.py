import sys
import time
from anytree import AnyNode, RenderTree, PreOrderIter
from copy import deepcopy
import re

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


def solveAdd(add):
    res = 0
    for char in add.split(" "):
        if char.isdigit():
            res += int(char)
    return str(res) + " "

def solveMult(mult):
    res = 1
    for char in mult.split(" "):
        if char.isdigit():
            res *= int(char)
    return str(res) + " "

def doAdds(e):
    newe = deepcopy(e)
    # do obvious adds
    adds = re.findall("[0-9]+\s*(?:\+\s*[0-9]+\s*)+", e)
    while len(adds) > 0:
        for add in adds:
            newe = newe.replace(add, solveAdd(add))
        adds = re.findall("[0-9]+\s*(?:\+\s*[0-9]+\s*)+", newe)
        newe = doSingleParens(newe)
    return newe

def doSingleParens(e):
    newe = deepcopy(e)
    simplify = re.findall("\(\s*[0-9]+\s*\)", newe)
    for s in simplify:
        newe = newe.replace(s, s[1:-1])
    return newe

def doMultParen(e):
    newe = deepcopy(e)
    # do mults
    mults = re.findall("\([0-9]+\s*(?:\*\s*[0-9]+\s*)+\)", newe)
    while len(mults) > 0:
        for mult in mults:
            # print(mult, solveMult(mult[1:-1]))
            newe = newe.replace(mult, solveMult(mult[1:-1]))
        newe = doSingleParens(newe)
        mults = re.findall("\([0-9]+\s*(?:\*\s*[0-9]+\s*)+\)", newe)
    print(newe)
    newe = doAdds(newe)
    return newe

def doMultsOnce(e):
    newe = deepcopy(e)
    # do mults
    mults = re.findall("[0-9]+\s*\*\s*[0-9]+", newe)
    if len(mults) > 0:
        newe = newe.replace(mults[0], solveMult(mults[0]))
    newe = doSingleParens(newe)
    return newe


def blarg(e):
    newe = deepcopy(e)

    while "+" in newe:
        newe = doAdds(newe)
        print(newe)

        newe = doMultParen(newe)
        print(newe)

        newe = doSingleParens(newe)
        print(newe)


    # val = doEquation(newe)
    while "*" in newe:
        newe = doMultsOnce(newe)
        print(newe)

    return int(newe)

###########################
# part2
###########################
def part2(data):
    print(data)
    result = 0
    for equation in data:
        val = blarg(equation)
        print(equation, "=", val)
        result += val
    print("sum", result)

# 285736436889034 too low
# 381107030035248 too high
# 381107030035788 too high

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
