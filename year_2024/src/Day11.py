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

# 0 will always become the same thing after some number of steps?
# 0 -> 19778 in 25 steps
# other common numbers probably repeat, too
def part2():
    stones = parseInput(11)
    print(stones)

    # Most common numbers: 4, 8, 0, 2, 6
    zero_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 4, 6: 7, 7: 14, 8: 16, 9: 20, 10: 39, 11: 62, 12: 81, 13: 110, 14: 200, 15: 328, 16: 418, 17: 667, 18: 1059, 19: 1546, 20: 2377, 21: 3572, 22: 5602, 23: 8268, 24: 12343, 25: 19778}
    seven_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 8, 7: 11, 8: 22, 9: 32, 10: 52, 11: 72, 12: 106, 13: 168, 14: 242, 15: 413, 16: 602, 17: 832, 18: 1369, 19: 2065, 20: 3165, 21: 4762, 22: 6994, 23: 11170, 24: 16509, 25: 25071}
    four_sizes = {1: 1, 2: 2, 3: 4, 4: 4, 5: 4, 6: 8, 7: 16, 8: 27, 9: 30, 10: 47, 11: 82, 12: 115, 13: 195, 14: 269, 15: 390, 16: 637, 17: 951, 18: 1541, 19: 2182, 20: 3204, 21: 5280, 22: 7721, 23: 11820, 24: 17957, 25: 26669}
    eight_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 7, 6: 7, 7: 11, 8: 22, 9: 31, 10: 48, 11: 69, 12: 103, 13: 161, 14: 239, 15: 393, 16: 578, 17: 812, 18: 1322, 19: 2011, 20: 3034, 21: 4580, 22: 6798, 23: 10738, 24: 16018, 25: 24212}
    two_sizes = {1: 1, 2: 2, 3: 4, 4: 4, 5: 6, 6: 12, 7: 16, 8: 19, 9: 30, 10: 57, 11: 92, 12: 111, 13: 181, 14: 295, 15: 414, 16: 661, 17: 977, 18: 1501, 19: 2270, 20: 3381, 21: 5463, 22: 7921, 23: 11819, 24: 18712, 25: 27842}
    six_sizes = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 8, 7: 11, 8: 22, 9: 32, 10: 54, 11: 68, 12: 103, 13: 183, 14: 250, 15: 401, 16: 600, 17: 871, 18: 1431, 19: 2033, 20: 3193, 21: 4917, 22: 7052, 23: 11371, 24: 16815, 25: 25469}
    sizes = {0: zero_sizes, 7: seven_sizes, 4: four_sizes, 8: eight_sizes, 2: two_sizes, 6: six_sizes}

    steps = 25
    for step in range(steps):
        print("Step", step)
        newStones = []
        for stone in stones:
            newStones += transformStone(stone)
        stones = newStones
        # print(stones)
        size = len(stones)
        sizes[step+1] = size
        print(size)
    print(sizes)
    print(stones)

    # OPTION 1
    # for every item in the list, compute their lists and how long they are (once)
    # ... somehow try to count

    # OPTION 2
    # extrapolate length of list to 75 with math lmao

    # for count, elem in sorted(((stones.count(e), e) for e in set(stones)), reverse=True):
    #     print('%s (%d)' % (elem, count))
    # remove all da zeroes?
    removed_zeroes = 0
    newStones = []
    for stone in stones:
        if stone != 0:
            newStones.append(stone)
            removed_zeroes += 1
    stones = newStones
    print(stones)
    print("removed ", removed_zeroes, "Zeros")
    # starting with just 0, we have 18457 zeroes after 25 steps

    # add up counts and keep going?
    steps = 25
    for step in range(steps):
        print("Step", step)
        newStones = []
        for stone in stones:
            newStones += transformStone(stone)
        stones = newStones
        # print(stones)
        size = len(stones)
        sizes[step+1] = size
        print(size)
    print(sizes)
    # after removing zeros, after another 25 steps, we have XX items
    # add 18457 * (zero size after 25)
    # that's our size for 50


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
