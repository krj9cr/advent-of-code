import time
from collections import Counter

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

def transformStone(stone):
    if stone == 0:
        return [1]
    string = str(stone)
    if len(string) % 2 == 0:
        midpoint = len(string) // 2
        return [int(string[:midpoint]), int(string[midpoint:])]
    return [stone * 2024]

def runSim(stones, steps=25):
    for step in range(steps):
        newStones = []
        for stone in stones:
            newStones += transformStone(stone)
        stones = newStones
    return stones

def part2():
    stones = parseInput(11)
    print(stones)
    seen = {}
    total = 0

    for main_stone in stones:
        print("LOOKING AT", main_stone)
        main_total = 0
        # do initial 25 steps for the number
        stones_25 = runSim([main_stone])
        total_25 = len(stones_25)
        seen[main_stone] = (total_25, stones_25)

        # for every item in the list, compute their lists and how long they are (once) after 25 runs
        total_50 = 0
        stones_50 = []
        for stone in stones_25:
            if stone in seen:
                stones_50 += seen[stone][1]
                total_50 += seen[stone][0]
                continue
            else:
                newStones = runSim([stone])
                newStonesSize = len(newStones)
                seen[stone] = (newStonesSize, newStones)
                total_50 += newStonesSize
                stones_50 += newStones
                # print("computing", stone, "size", newStonesSize)
        print("unique stones:", len(seen))
        print("Total 50:", total_50)

        # now we're at 50, so last time
        for stone in stones_50:
            if stone in seen:
                main_total += seen[stone][0]
                continue
            else:
                newStones = runSim([stone])
                newStonesSize = len(newStones)
                seen[stone] = (newStonesSize, newStones)
                main_total += newStonesSize
                # print("computing", stone, "size", newStonesSize)
        print("unique stones:", len(seen))
        print("total size for", main_stone, ":", main_total)
        print()
        total += main_total
    print("Overall total:", total)

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
