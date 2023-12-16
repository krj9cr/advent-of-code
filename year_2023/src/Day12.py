import time
import copy
from multiprocessing import Pool

class SpringGroup:
    def __init__(self, springs, arrangement):
        self.springs = springs
        self.arrangement = arrangement

    def __str__(self):
        return self.springs + " " + str(self.arrangement)

    def unfold(self):
        c = copy.deepcopy(self.springs)
        for i in range(4):
            self.springs += "?" + c
        # print(self.springs)
        c = copy.deepcopy(self.arrangement)
        for i in range(4):
            self.arrangement += c
        # print(self.arrangement)
        return self

def getNumChars(springs, findChar="#"):
    count = 0
    for char in springs:
        if char == findChar:
            count += 1
    return count

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        springGroups = []
        for line in file:
            parts = line.strip().split(" ")
            springs = parts[0]
            parts2 = parts[1].split(",")
            arrangement = [int(c) for c in parts2]
            springGroups.append(SpringGroup(springs, arrangement))
        return springGroups

def partialSatisfiesArrangement(springs, arrangement):
    groups = []
    groupId = 0
    currentGroup = ""
    partial = True
    for char in springs:
        if char == "?":
            return partial
        if char == "#":
            currentGroup += char
        else:
            if currentGroup != "":
                groups.append(len(currentGroup))
                # fail fast if a group doesn't match
                if groupId >= len(arrangement) or arrangement[groupId] != len(currentGroup):
                    # print(springs, self.arrangement, groups)
                    return False
                groupId += 1
                currentGroup = ""
    if currentGroup != "":
        groups.append(len(currentGroup))
    if len(groups) > len(arrangement):
        return False
    # if there are more "#" than the sum of arrangement
    if getNumChars(springs, "#") > sum(arrangement):
        return False
    return True

def satisfiesArrangement(springs, arrangement):
    groups = []
    groupId = 0
    currentGroup = ""
    for char in springs:
        if char == "#":
            currentGroup += char
        else:
            if currentGroup != "":
                groups.append(len(currentGroup))
                # fail fast if a group doesn't match
                if groupId >= len(arrangement) or arrangement[groupId] != len(currentGroup):
                    # print(springs, self.arrangement, groups)
                    return False
                groupId += 1
                currentGroup = ""
    if currentGroup != "":
        groups.append(len(currentGroup))
    return groups == arrangement

def hashSpringsArrangement(springs, arrangement):
    return springs + " " + ",".join([str(i) for i in arrangement])

def firstArrangementValid(springs, arrangement):
    if len(arrangement) < 0:
        print("UH OH")
        return False
    firstArr = arrangement[0]
    if len(springs) < firstArr:
        return False
    try:
        firstDot = springs.index(".")
        group = springs[:firstDot]
        return group == firstArr * "#"
    except:
        # no dots, so the whole thing needs to satisfy?
        return springs == firstArr * "#"

# return (number of solutions, count of recursion)
def solve(springs, arrangement):
    hashed = hashSpringsArrangement(springs, arrangement)
    # print(hashed)
    if hashed in cache:
        # print("cache hit", hashed,  "--->", cache[hashed])
        return cache[hashed], 0, springs
    # find the next question mark
    try:
        questionMarkIdx = springs.index("?")
        # try both "." and "#" and recurse
        springs2 = springs[:questionMarkIdx] + "#" + springs[questionMarkIdx + 1:]
        springs2 = springs2.strip(".")
        hashed2 = hashSpringsArrangement(springs2, arrangement)
        a2 = 0, 0
        if firstArrangementValid(springs2, arrangement):
            firstArr = arrangement[0]
            springs2 = springs2[firstArr:]
            arrangement2 = arrangement[1:]
            if partialSatisfiesArrangement(springs2, arrangement2):
                a2 = solve(springs2, arrangement2)
                cache[hashSpringsArrangement(springs2, arrangement2)] = a2[0]
        else:
            # see if this makes anything valid for the first group in arrangement
            if partialSatisfiesArrangement(springs2, arrangement):
                a2 = solve(springs2, arrangement)
                cache[hashed2] = a2[0]

        springs3 = springs[:questionMarkIdx] + "." + springs[questionMarkIdx + 1:]
        springs3 = springs3.strip(".")
        hashed3 = hashSpringsArrangement(springs3, arrangement)
        a3 = 0, 0
        if firstArrangementValid(springs3, arrangement):
            firstArr = arrangement[0]
            springs3 = springs3[firstArr:]
            arrangement3 = arrangement[1:]
            if partialSatisfiesArrangement(springs3, arrangement3):
                a3 = solve(springs3, arrangement3)
                cache[hashSpringsArrangement(springs3, arrangement3)] = a3[0]
        else:
            # see if this makes anything valid for the first group in arrangement
            if partialSatisfiesArrangement(springs3, arrangement):
                a3 = solve(springs3, arrangement)
                cache[hashed3] = a3[0]
        if hashed3 not in cache:
            cache[hashed3] = 0

        return a2[0] + a3[0], a2[1] + a3[1], springs
    except:
        # we're done
        if satisfiesArrangement(springs, arrangement):
            cache[hashed] = 1
            return 1, 1, springs
        else:
            cache[hashed] = 0
            return 0, 1, springs

# global cache for memoization
cache = {}

def part1():
    springGroups = parseInput(12)

    pool = Pool()
    processes = []

    answer = 0
    for group in springGroups:
        # print("starting", group, group.numUnknownSprings, "; totalPossible: ", math.pow(2, group.numUnknownSprings))
        processes.append(pool.apply_async(solve, args=[group.springs, group.arrangement]))

    for process in processes:
        a, totalChecked, group = process.get()
        # print("finished", group, "; answer:", a, "; totalChecked:", totalChecked)
        answer += a
    print(answer)

def part2():
    springGroups = parseInput(12)

    pool = Pool()
    processes = []

    answer = 0
    for group in springGroups:
        # print(group)
        group.unfold()
        # print("starting", group, group.numUnknownSprings, "; totalPossible: ", math.pow(2, group.numUnknownSprings))
        processes.append(pool.apply_async(solve, args=[group.springs, group.arrangement]))

    for process in processes:
        a, totalChecked, group = process.get()
        # print("finished", group, "; answer:", a, "; totalChecked:", totalChecked)
        answer += a
    print(answer)

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
