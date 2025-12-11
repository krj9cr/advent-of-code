import time, os
import numpy as np

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip().split()
            lines.append(line)
        array = np.array(lines)
        rotated = np.rot90(array, k=-1)
        rev = []
        for line in rotated:
            rev.append(list(reversed(line)))
        return rev

def part1():
    lines = parseInput()
    # print(lines)

    total = 0
    for line in lines:
        op = line[-1]
        acc = 0
        if op == "*":
            acc = 1
        for num in line[:-1]:
            if op == "*":
                # print("mult", num)
                acc *= int(num)
            else:
                # print("add", num)
                acc += int(num)
        # print("acc", acc)
        total += acc
    print("total", total)

def parseInput2():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip('\n')
            lines.append(list(line))
        return lines

def part2():
    lines = parseInput2()
    # print(lines)

    # for line in lines:
    #     print(line)

    longest = 0
    # take the longest line length
    for line in lines:
        l = len(line)
        if l > longest:
            longest = l
    # print("longest", longest)

    for line in lines:
        for i in range(longest-len(line)):
            line.append(" ")

    # for line in lines:
    #     print(line)

    array = np.array(lines)
    rotated = np.rot90(array, k=1)
    # print(rotated)

    nums = []
    for line in rotated:
        nums.append(''.join(line).strip())

    # print(nums)

    # split on empty rows, so they are grouped
    res = []
    start = 0
    for i, v in enumerate(nums):
        if v == '':
            res.append(nums[start:i])
            start = i + 1
    if start < len(nums):
        res.append(nums[start:])

    # print(res)

    total = 0
    for group in res:
        op = group[-1][-1]
        group[-1] = group[-1][:-1]
        # print(group, op)
        acc = 0
        if op == "*":
            acc = 1
        for s in group:
            num = int(s)
            if op == "*":
                acc *= num
            else:
                acc += num
        # print(acc)
        total += acc

    print("total", total)





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
