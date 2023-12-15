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

def part2():
    springGroups = parseInput(12)

    pool = Pool()
    processes = []

    answer = 0
    for group in springGroups:
        # print(group)
        group.unfold()
        print("starting", group, group.numUnknownSprings, "; totalPossible: ", math.pow(2, group.numUnknownSprings))
        processes.append(pool.apply_async(group.solve, args=[group.springs]))

    for process in processes:
        a, totalChecked, group = process.get()
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
