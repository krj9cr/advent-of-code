import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            return [int(thing) for thing in line.split(" ")]

def part1():
    stones = parseInput(11)
    print(stones)

    steps = 25
    for step in range(steps):
        print("Step", step)
        newStones = []
        for stone in stones:
            if stone == 0:
                newStones.append(1)
                continue
            string = str(stone)
            if len(string) % 2 == 0:
                midpoint = len(string) // 2
                newStones.append(int(string[:midpoint]))
                newStones.append(int(string[midpoint:]))
                continue
            newStones.append(stone * 2024)
        stones = newStones
        print(stones)
    print(len(stones))


def part2():
    lines = parseInput(11)
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