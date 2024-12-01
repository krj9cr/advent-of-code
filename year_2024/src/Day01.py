import time
from collections import Counter

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    list1 = []
    list2 = []
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        for line in lines:
            line = line.split(" ")
            # print(line)
            item1 = int(line[0])
            list1.append(item1)
            item2 = int(line[-1])
            list2.append(item2)
        return list1, list2

def part1():
    list1, list2 = parseInput(1)

    list1.sort()
    list2.sort()

    total = 0
    for i in range(0, len(list1)):
        # print(list1[i], list2[i])
        diff = abs(list1[i]-list2[i])
        # print("diff", diff)
        total += diff
    print("total", total)

def part2():
    list1, list2 = parseInput(1)

    counts = Counter(list2)
    # print(counts)

    total = 0
    for i in range(0, len(list1)):
        # print(list1[i], list2[i])
        count = counts.get(list1[i])
        if count:
            # print("count", count)
            total += list1[i] * count
    print("total", total)

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
