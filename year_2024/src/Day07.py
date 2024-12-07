import copy
import itertools
import time
from itertools import combinations_with_replacement

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            linesplit = line.split(": ")
            answer = int(linesplit[0])
            nums = linesplit[1]
            numssplit = nums.split(" ")
            lines.append((answer, [int(n) for n in numssplit]))
        return lines

def part1():
    equations = parseInput(7)
    print(equations)

    total = 0
    for (answer, nums) in equations:
        print(answer, nums)

        for comb in itertools.product(["+", "*"], repeat=len(nums)-1):
            print(comb)
            comb = list(comb)
            # evaluate
            agg = nums[0]
            for i in range(1, len(nums)):
                n = nums[i]
                op = comb.pop()
                if op == "+":
                    agg = agg + n
                else:
                    agg = agg * n
                print(agg)
            if answer == agg:
                print("YAY")
                total += answer
                break

    print(total)

def part2():
    equations = parseInput(7)
    print(equations)

    total = 0
    for (answer, nums) in equations:
        print(answer, nums)

        for comb in itertools.product(["+", "*", "||"], repeat=len(nums)-1):
            # print(comb)
            comb = list(comb)
            agg = nums[0]
            for i in range(1, len(nums)):
                n = nums[i]
                op = comb.pop()
                if op == "+":
                    agg = agg + n
                elif op == "*":
                    agg = agg * n
                else:
                    agg = int(str(agg) + str(n))
                if agg > answer:
                    break
            if answer == agg:
                # print("YAY")
                total += answer
                break

    print(total)

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
