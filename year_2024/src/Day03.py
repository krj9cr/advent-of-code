import time
import re

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)
        return lines

def part1():
    lines = parseInput(3)
    total = 0
    for line in lines:
        matches = re.finditer(r"mul\(([0-9]{0,3}),([0-9]{0,3})\)", line)
        print(line)
        for match in matches:
            # print(str(match))
            first = int(match.group(1))
            second = int(match.group(2))
            # print(first, second)
            total += (first * second)
    print(total)

def part2():
    lines = parseInput(3)
    total = 0
    do = True
    for line in lines:
        matches = re.finditer(r"mul\(([0-9]{0,3}),([0-9]{0,3})\)|do\(\)|don't\(\)", line)
        print(line)
        for match in matches:
            print(match.group())
            try:
                first = int(match.group(1))
                second = int(match.group(2))
                if do:
                    print("adding", first, second)
                    total += (first * second)
            except:
                # it's a do/don't
                if match.group() == "do()":
                    do = True
                    print("DO")
                else:
                    do = False
                    print("DONT")
            # print(first, second)
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
