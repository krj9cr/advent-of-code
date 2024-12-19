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
    # print(towels)
    # print(patterns)

    print("num towels", len(towels))
    print("num patterns", len(patterns))

    # sort by length so we don't match on a single letter first (since it's greedy)
    towels.sort()
    towels.sort(key=lambda x: len(x), reverse=True)
    # print(towels)

    towels_dict = {}
    for k, g in groupby(towels, key=lambda x: x[0]):
        if towels_dict.get(k):
            towels_dict[k] += list(g)
        else:
            towels_dict[k] = list(g)
    # sort by longest to shortest
    for k in towels_dict:
        towels_dict[k].sort(key=lambda x: len(x), reverse=True)
    # print(towels_dict)

    memo = {}

    def has_match(pattern):
        if pattern == "":
            return True
        if memo.get(pattern) is not None:
            return memo[pattern]
        # print("checking", pattern)
        next_letter = pattern[0]
        if towels_dict.get(next_letter):
            towels = towels_dict[next_letter]
            for towel in towels:
                if pattern.startswith(towel):
                    if has_match(pattern[len(towel):]):
                        memo[pattern] = True
                        return True
        memo[pattern] = False
        return False

    total = 0
    for pattern in patterns:
        print("PATTERN", pattern)
        if has_match(pattern):
            print("  match")
            total += 1
        else:
            print("  no match")

    print("TOTAL", total)

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
