import time
from itertools import groupby
import re

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        towels = []
        patterns = []
        doing_patterns = False
        for line in file:
            line = line.strip()
            if line == "":
                doing_patterns = True
                continue
            if doing_patterns:
                patterns.append(line)
            else:
                towels = line.split(", ")
        return towels, patterns

def part1():
    towels, patterns = parseInput(19)
    print(towels)
    print(patterns)

    print(len(towels))
    print(len(patterns))

    # sort by length so we don't match on a single letter first (since it's greedy)
    towels.sort()
    towels.sort(key=lambda x: len(x), reverse=True)
    print(towels)

    # towels_dict = {}
    # for k, g in groupby(towels, key=lambda x: x[0]):
    #     if towels_dict.get(k):
    #         towels_dict[k] += list(g)
    #     else:
    #         towels_dict[k] = list(g)
    # # sort by longest to shortest
    # for k in towels_dict:
    #     towels_dict[k].sort(key=lambda x: len(x), reverse=True)
    # print(towels_dict)

    # generate regex
    reg = "("
    for towel in towels:
        reg += towel + "|"
    reg += ")*"
    print(reg)
    reg = re.compile(reg)

    # try to match each pattern
    total = 0
    for pattern in patterns:
        match = re.match(reg, pattern)
        # print(match)
        if match.group(0) == pattern:
            # print(pattern, "match")
            total += 1
        else:
            print(pattern, "no match")
    print("TOTAL", total)

# 295 too low

def part2():
    lines = parseInput(19)
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
