import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

def part1():
    lines = parseInput(1)
    nums = []
    for line in lines:
        numStr = ""
        for char in line:
            if char.isdecimal():
                numStr += char
        num = int(numStr[0] + numStr[-1])
        nums.append(num)
    print(sum(nums))

def part2():
    lines = parseInput(1)
    nums = []

    for line in lines:
        print(line)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)
