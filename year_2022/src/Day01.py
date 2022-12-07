import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        groups = []
        currGroup = 0
        for line in lines:
            if line == "":
                groups.append(currGroup)
                currGroup = 0
            else:
                currGroup += int(line)
        return groups

def part1():
    lines = parseInput(1)
    print(max(lines))

def part2():
    lines = parseInput(1)
    print(sum(sorted(lines,reverse=True)[0:3]))

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
