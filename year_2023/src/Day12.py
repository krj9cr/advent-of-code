import itertools
import math
import time
import copy
from multiprocessing import Pool

# a portion of a SpringGroup
class CharGroup:
    def __init__(self, string, index):
        self.string = string
        self.index = index

    def __str__(self):
        return self.string + " idx: " + str(self.index)

def getNumChars(springs, findChar="#"):
    count = 0
    for char in springs:
        if char == findChar:
            count += 1
    return count

def checkFirstGroup(springs, num):
    if len(springs) == 0:
        print("WEIRD CASE?")
        return "", 0
    currentGroup = ""
    # get the first group of "#"
    for i in range(len(springs)):
        char = springs[i]
        if char == "?":
            if currentGroup == "":
                return "", 0
            else:
                if len(currentGroup) == num:
                    return currentGroup + "?", i
        if char == ".":
            if currentGroup == "":
                continue
            else:
                break
        if char == "#":
            currentGroup += char
    if len(currentGroup) == num:
        return currentGroup, i
    return "", 0

cache = {}

class SpringGroup:
    def __init__(self, springs, arrangement):
        self.springs = springs
        self.arrangement = arrangement
        self.numKnownSprings = getNumChars(self.springs)
        self.totalSprings = sum(self.arrangement)
        self.numUnknownSprings = getNumChars(self.springs, "?")

    def __str__(self):
        return self.springs + " " + str(self.arrangement)

    # recurse and prune better
    def solve(self, springs):
        # print(springs)
        # find the next ?
        questionMarkIdx = None
        for i in range(len(springs)):
            char = springs[i]
            if char == "?":
                questionMarkIdx = i
                break
        # if no question marks, we're done
        if questionMarkIdx is None:
            if self.satisfiesArrangement(springs):
                return 1, 1, self.springs
            else:
                return 0, 1, self.springs
        # try both "." and "#" and recurse
        else:
            springs2 = springs[:questionMarkIdx] + "#" + springs[questionMarkIdx + 1:]
            if self.partialSatisfiesArrangement(springs2):
                a2 = self.solve(springs2)
            else:
                a2 = 0, 0
            springs3 = springs[:questionMarkIdx] + "." + springs[questionMarkIdx + 1:]
            if self.partialSatisfiesArrangement(springs3):
                a3 = self.solve(springs3)
            else:
                a3 = 0, 0
            return a2[0] + a3[0], a2[1] + a3[1], self.springs

    # recurse and memoize
    def solve2(self, springs):
        # print(springs)
        # if no more arrangements?
        # if len(self.arrangement) <= 0:
        #     return 0, 1, self.springs
        # find the next ?
        questionMarkIdx = None
        for i in range(len(springs)):
            char = springs[i]
            if char == "?":
                questionMarkIdx = i
                break
        # if no question marks, we're done
        if questionMarkIdx is None:
            if self.satisfiesArrangement(springs):
                cache[SpringGroup(springs, self.arrangement)] = (1, 1, self.springs)
                return 1, 1, self.springs
            else:
                cache[SpringGroup(springs, self.arrangement)] = (0, 1, self.springs)
                return 0, 1, self.springs
        # try both "." and "#" and recurse
        else:
            springs2 = springs[:questionMarkIdx] + "#" + springs[questionMarkIdx + 1:]
            if self.partialSatisfiesArrangement(springs2):
                # check if we can remove any "arrangements"
                num = self.arrangement[0]
                s, sidx = checkFirstGroup(springs2, num)
                if s != "":
                    springs2 = springs2[sidx + 1:].strip(".")
                    newSpringGroup = SpringGroup(springs2, self.arrangement[1:])
                    print(newSpringGroup)
                    if newSpringGroup in cache:
                        a2 = cache[newSpringGroup]
                        print("cache hit", newSpringGroup, a2)
                    else:
                        a2 = newSpringGroup.solve2(springs2)
                        cache[newSpringGroup] = a2
                else:
                    a2 = self.solve2(springs2)
                    cache[SpringGroup(springs2, self.arrangement)] = a2
            else:
                a2 = 0, 0
                cache[SpringGroup(springs2, self.arrangement)] = a2

            springs3 = springs[:questionMarkIdx] + "." + springs[questionMarkIdx + 1:]
            if self.partialSatisfiesArrangement(springs2):
                s, sidx = checkFirstGroup(springs2, num)
                if s != "":
                    springs3 = springs3[sidx+1:].strip(".")
                    newSpringGroup = SpringGroup(springs3, self.arrangement[1:])
                    print(newSpringGroup)
                    if newSpringGroup in cache:
                        a3 = cache[newSpringGroup]
                        print("cache hit", newSpringGroup, a3)
                    else:
                        a3 = newSpringGroup.solve2(springs3)
                        cache[newSpringGroup] = a3
                else:
                    a3 = self.solve2(springs3)
                    cache[SpringGroup(springs3, self.arrangement)] = a3
            else:
                a3 = 0, 0
                cache[SpringGroup(springs3, self.arrangement)] = a3

            return a2[0] + a3[0], a2[1] + a3[1], self.springs

    def partialSatisfiesArrangement(self, springs):
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
                    if groupId >= len(self.arrangement) or self.arrangement[groupId] != len(currentGroup):
                        # print(springs, self.arrangement, groups)
                        return False
                    groupId += 1
                    currentGroup = ""
        if currentGroup != "":
            groups.append(len(currentGroup))
        if len(groups) > len(self.arrangement):
            return False
        # if there are more "#" than the sum of arrangement
        if getNumChars(springs, "#") > sum(self.arrangement):
            return False
        return True

    def satisfiesArrangement(self, springs):
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
                    if groupId >= len(self.arrangement) or self.arrangement[groupId] != len(currentGroup):
                        # print(springs, self.arrangement, groups)
                        return False
                    groupId += 1
                    currentGroup = ""
        if currentGroup != "":
            groups.append(len(currentGroup))
        return groups == self.arrangement

    def guessArrangement(self):
        # print(self)

        # get all possible combos of filling in the question marks
        answer = 0
        for combo in itertools.product([".", "#"], repeat=self.numUnknownSprings):
            numComboSprings = getNumChars(combo)
            # prune off combos that don't have the same total number of springs we expect
            if numComboSprings + self.numKnownSprings != self.totalSprings:
                continue
            springs = ""
            c = 0
            for i in range(len(self.springs)):
                char = self.springs[i]
                if char == "?":
                    springs += combo[c]
                    c += 1
                else:
                    springs += char
            # print(springs, numComboSprings, self.numKnownSprings, self.totalSprings)
            # check if this satisfies and count it
            if self.satisfiesArrangement(springs):
                answer += 1
        return self, answer

    def unfold(self):
        c = copy.deepcopy(self.springs)
        for i in range(4):
            self.springs += "?" + c
        # print(self.springs)
        c = copy.deepcopy(self.arrangement)
        for i in range(4):
            self.arrangement += c
        # print(self.arrangement)
        # recompute totals
        self.numKnownSprings = getNumChars(self.springs)
        self.totalSprings = sum(self.arrangement)
        self.numUnknownSprings = getNumChars(self.springs, "?")
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

def part1():
    springGroups = parseInput(12)
    answer = 0
    for group in springGroups:
        g, a = group.guessArrangement()
        print(group, a)
        answer += a
    print(answer)

    # testing
    # g = SpringGroup("???.###", [1, 1, 3])
    # print(g.satisfiesArrangement("...#...#.###..."))
    # print(g.guessArrangement())


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
def solve3(springs, arrangement):
    hashed = hashSpringsArrangement(springs, arrangement)
    # print(hashed)
    if hashed in cache:
        # print("cache hit", hashed,  "--->", cache[hashed])
        return cache[hashed], 0
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
                a2 = solve3(springs2, arrangement2)
                cache[hashSpringsArrangement(springs2, arrangement2)] = a2[0]
        else:
            # see if this makes anything valid for the first group in arrangement
            if partialSatisfiesArrangement(springs2, arrangement):
                a2 = solve3(springs2, arrangement)
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
                a3 = solve3(springs3, arrangement3)
                cache[hashSpringsArrangement(springs3, arrangement3)] = a3[0]
        else:
            # see if this makes anything valid for the first group in arrangement
            if partialSatisfiesArrangement(springs3, arrangement):
                a3 = solve3(springs3, arrangement)
                cache[hashed3] = a3[0]
        if hashed3 not in cache:
            cache[hashed3] = 0

        return a2[0] + a3[0], a2[1] + a3[1]
    except:
        # we're done
        if satisfiesArrangement(springs, arrangement):
            cache[hashed] = 1
            return 1, 1
        else:
            cache[hashed] = 0
            return 0, 1


def part2():
    springGroups = parseInput(12)

    # print(checkFirstGroup("###", 3))

    pool = Pool()
    processes = []

    answer = 0
    for group in springGroups:
        # print(group)
        group.unfold()
        print("starting", group, group.numUnknownSprings, "; totalPossible: ", math.pow(2, group.numUnknownSprings))
        processes.append(pool.apply_async(solve3, args=[group.springs, group.arrangement]))

    for process in processes:
        a, totalChecked = process.get()
        print("finished", group, "; answer:", a, "; totalChecked:", totalChecked)
        answer += a
    print(answer)

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
