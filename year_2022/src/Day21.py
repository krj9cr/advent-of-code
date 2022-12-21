import re
import time
from sympy import symbols, solve, sympify

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        monkeys = {}
        lines = [line.strip() for line in file]
        for line in lines:
            split = line.split(": ")
            monkeys[split[0]] = split[1]
        return monkeys

def fill_equation(monkeys, node):
    n = monkeys[node]
    if n.isnumeric():
        return n
    else:
        split = re.split(' \+ | \* | / | - ', n)
        print(split)
        left = fill_equation(monkeys, split[0])
        right = fill_equation(monkeys, split[1])
        n = n.replace(split[0], f"({left})")
        n = n.replace(split[1], f"({right})")
        return n

def part1():
    monkeys = parseInput(21)
    print(monkeys)

    root = fill_equation(monkeys, 'root')
    print(root)
    print(eval(root))


def fill_equation2(monkeys, node):
    n = monkeys[node]
    if node == 'humn':
        return node
    if n.isnumeric():
        return n
    else:
        split = re.split(' \+ | \* | / | - | = ', n)
        print(split)
        left = fill_equation2(monkeys, split[0])
        right = fill_equation2(monkeys, split[1])
        n = n.replace(split[0], f"({left})")
        n = n.replace(split[1], f"({right})")
        return n

def part2():
    monkeys = parseInput(21)
    print(monkeys)

    monkeys['root'] = monkeys['root'].replace('+', '=')

    root = fill_equation2(monkeys, 'root')

    sympy_eq = sympify("Eq(" + root.replace("=", ",") + ")")
    print(solve(sympy_eq))

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
