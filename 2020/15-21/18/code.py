import sys
import time
from anytree import AnyNode, RenderTree, PreOrderIter, PostOrderIter
from copy import deepcopy
import ast

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return line.strip()



class v(ast.NodeVisitor):

    def __init__(self):
        self.tokens = []
        self.result = -1
        self.lastop = None

    def f_continue(self, node):
        super(v, self).generic_visit(node)

    def visit_Add(self, node):
        self.tokens.append('+')
        self.lastop = "+"
        self.f_continue(node)

    def visit_BinOp(self, node):
        right = self.visit(node.right).value
        left = self.visit(node.left).value
        if type(node.op) is ast.Add:
            print(left + right)
        elif type(node.op) is ast.Mult:
            print(left * right)
        # self.visit(node.op)

    def visit_Div(self, node):
        self.tokens.append('/')
        self.f_continue(node)

    def visit_Expr(self, node):
        # print('visit_Expr')
        return self.f_continue(node)

    def visit_Mult(self, node):
        self.tokens.append('*')
        self.f_continue(node)

    def visit_Num(self, node):
        # if self.result == -1:
        #     self.result = node.n
        self.tokens.append(node.n)
        self.f_continue(node)
        print(node.n)

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

            if equation[-1] == "(":
                return parseEquation(equation[1:-1])
            else:
                idx = -1
                for i in range(len(equation)-1,1,-1):
                    if equation[i] == "(":
                        idx = i
                        break
                blob = equation[1:idx]
                if idx+2 >= len(equation):
                    print("UH OH")
                    sys.exit(1)
                op = equation[idx+2]
                rest = equation[idx+4:]
                return AnyNode(children=[parseEquation(blob), parseEquation(rest)], type="op", data=op)

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

def rrr(tree):
    if type(tree) is ast.Num:
        return tree.n
    elif type(tree) is ast.BinOp:
        left = rrr(tree.left)
        right = rrr(tree.right)
        op = tree.op
        if type(op) is ast.Add:
            return left + right
        elif type(op) is ast.Mult:
            return left * right
    elif type(tree) is ast.Expr:
        return rrr(tree.value)
    elif type(tree) is ast.Module:
        return rrr(tree.body[0])

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

    # visitor = v()
    # tree = ast.parse(equation)
    # print(ast.dump(tree))
    # print(rrr(tree))
    # return 0

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
