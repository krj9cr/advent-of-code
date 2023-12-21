import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        startPos = None
        rocks = set()
        j = 0
        for line in file:
            line = line.strip()
            for i in range(len(line)):
                char = line[i]
                if char == "#":
                    rocks.add((i, j))
                elif char == "S":
                    startPos = (i, j)
            j += 1
        return startPos, rocks

def part1():
    startPos, rocks = parseInput(21)
    print(startPos, rocks)

    num_steps = 64

    elf_locations = {startPos}
    for step in range(num_steps):
        elf_locations2 = set()
        for loc in elf_locations:
            x, y = loc
            for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                nextPos = (x2, y2)
                if nextPos not in rocks:
                    elf_locations2.add(nextPos)
        elf_locations = elf_locations2
        print(elf_locations)
    print(len(elf_locations))

def part2():
    startPos, rocks = parseInput(21)
    print(startPos, rocks)

    num_steps = 6

    elf_locations = {startPos}
    for step in range(num_steps):
        elf_locations2 = set()
        for loc in elf_locations:
            x, y = loc
            for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                nextPos = (x2, y2)
                if nextPos not in rocks:
                    elf_locations2.add(nextPos)
        elf_locations = elf_locations2
        print(elf_locations)
    print(len(elf_locations))

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
