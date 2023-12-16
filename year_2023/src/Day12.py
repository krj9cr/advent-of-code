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

def getNumChars(springs, findChar="#"):
    count = 0
    for char in springs:
        if char == findChar:
            count += 1
    return count

# used for filtering combinations of springs with a given arrangement
# does a few basic checks to see if the springs don't match the arrangement at all
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

# checks that springs 100% matches an arrangement
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

# convert springs+arrangement to a string to use in cache
def hashSpringsArrangement(springs, arrangement):
    return springs + " " + ",".join([str(i) for i in arrangement])

# checks if the first group of springs is valid, so that we can "pop" it off
def firstArrangementValid(springs, arrangement):
    if len(arrangement) < 1:
        return False
    firstArr = arrangement[0]
    if len(springs) < firstArr:
        return False
    try:
        firstDot = springs.index(".")
        group = springs[:firstDot]
        return group == firstArr * "#"
    except ValueError:
        # no dots, so the whole thing needs to satisfy?
        return springs == firstArr * "#"

# does some work to replace a "?" with a char
# and decides how to proceed
# also do caching
def getNextSpringsToTry(questionMarkIdx, springs, arrangement, char="#"):
    springs2 = springs[:questionMarkIdx] + char + springs[questionMarkIdx + 1:]
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
    return a2

# return (number of solutions, count of recursion, springs (so that we can print them with processes later lol))
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
        a2 = getNextSpringsToTry(questionMarkIdx, springs, arrangement, char="#")
        a3 = getNextSpringsToTry(questionMarkIdx, springs, arrangement, char=".")
        return a2[0] + a3[0], a2[1] + a3[1], springs
    except ValueError:
        # no question marks means we're done
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
