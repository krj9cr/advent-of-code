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
            nums_comb = copy.deepcopy(nums)
            # evaluate da rest?
            while len(nums_comb) > 1:
                op = comb.pop()
                if op == "+":
                    nums_comb[0:2] = [nums_comb[0] + nums_comb[1]]
                elif op == "*":
                    nums_comb[0:2] = [nums_comb[0] * nums_comb[1]]
                else:
                    nums_comb[0:2] = [int(str(nums_comb[0]) + str(nums_comb[1]))]
                # print(nums_comb)
            if answer == nums_comb[0]:
                print("YAY")
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
