import time, os
import itertools

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
            line = line.strip()
            lines.append([int(i) for i in line])
        return lines

def findJoltage(bank):
    # exclude the last number to find the max
    firstMax = 0
    firstIndex = -1
    for index, value in enumerate(bank[:-1]):
        if value > firstMax:
            firstMax = value
            firstIndex = index
    # find the next max that's not the first index
    secondMax = 0
    for index, value in enumerate(bank[firstIndex+1:]):
        if value > secondMax:
            secondMax = value
    # combine the numbers
    s = str(firstMax) + str(secondMax)
    return int(s)

def part1():
    lines = parseInput()
    # print(lines)
    total = 0
    for bank in lines:
        joltage = findJoltage(bank)
        # print(joltage)
        total += joltage
    print(total)


def findMax(bank):
    return max(bank)

def findJoltage2(bank, l=11):
    # print("processing", bank, "l=", l)
    if l == 0:
        return str(max(bank))
    # exclude the last number to find the max
    firstMax = 0
    firstIndex = -1
    # print("checking:", bank[:-l])
    for index, value in enumerate(bank[:-l]):
        if value > firstMax:
            firstMax = value
            firstIndex = index
    # print("max", firstMax, "at", firstIndex)
    return str(firstMax) + findJoltage2(bank[firstIndex+1:], l-1)

def part2():
    lines = parseInput()
    # print(lines)
    total = 0
    for bank in lines:
        joltage = findJoltage2(bank)
        # print(joltage)
        total += int(joltage)
    print(total)


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
