import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip().split(',') for line in file]
        newlines = []
        for pair in lines:
            newpair = []
            for r in pair:
                nums = r.split('-')
                newpair.append( [ int(n) for n in nums])
            newlines.append(newpair)
        return newlines

# returns true if the first fully contains the second
def fullyContains(min1, max1, min2, max2):
    return min2 >= min1 and max2 <= max1

def part1():
    pairs = parseInput(4)
    # print(pairs)
    count = 0
    for pair in pairs:
        # print(pair)
        if fullyContains(pair[0][0], pair[0][1], pair[1][0], pair[1][1]) or \
            fullyContains(pair[1][0], pair[1][1], pair[0][0], pair[0][1]):
            # print("fully contains")
            count += 1
    print(count)

def overlap(min1, max1, min2, max2):
    return (min1 <= max2) and (max1 >= min2)

def part2():
    pairs = parseInput(4)
    # print(pairs)
    count = 0
    for pair in pairs:
        # print(pair)
        if overlap(pair[0][0], pair[0][1], pair[1][0], pair[1][1]) or \
            overlap(pair[1][0], pair[1][1], pair[0][0], pair[0][1]):
            # print("overlaps")
            count += 1
    print(count)

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
