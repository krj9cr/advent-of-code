import itertools
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

    # ???
    def reduce(self):
        # take the biggest number
        maxNum = max(self.arrangement)
        # see how many spots it can fit
        # split on dots?
        groups = []
        idx = 0
        string = ""
        for char in self.springs:
            if char == ".":
                if string != "":
                    charGroup = CharGroup(string, idx - len(string))
                    groups.append(charGroup)
                    # print("chargroup", charGroup)
                    string = ""
            else:
                string += char
            idx += 1
        if string != "":
            charGroup = CharGroup(string, idx - len(string))
            groups.append(charGroup)
            # print("chargroup", charGroup)

        # convert these to Spring Groups... by looking at arrangements?
        splitSpringGroups = []
        # if len(groups) == len(self.arrangement):
        #     # we know each group corresponds to a number, so we can split it
        #     for i in range(len(groups)):
        #         splitSpringGroups.append(SpringGroup(groups[i].string, [self.arrangement[i]]))
        # else:  # the number of groups is less (can't be more)
        # check the length, take the arrangements that are less than that length (adding periods)
        availableArrangments = copy.deepcopy(self.arrangement)
        for i in range(len(groups)):
            group = groups[i]
            print(group.string)
            numChars = len(group.string)
            # arr = availableArrangments.pop(0)  # this has to fit initially
            # total = arr
            # totalArr = [arr]
            total = 0
            totalArr = []
            added = False
            # TODO: there can be overlap... where arrangements fit into multiple groups, too
            #       e.g. ??##?##??????????.?? 14,1 ..... the 1 fits into both groups
            while len(availableArrangments) > 0:
                # try adding the next arrangement (after a period)
                arr = availableArrangments[0]
                print("next arr", arr)
                # add a period
                if total > 0:
                    total += 1
                if total + arr <= numChars:
                    total += arr
                    totalArr.append(arr)
                    availableArrangments = availableArrangments[1:]
                    print("total", total, totalArr)
                    print("availArr", availableArrangments)
                else:
                    splitSpringGroups.append(SpringGroup(group.string, totalArr))
                    added = True
                    break
            if not added:
                splitSpringGroups.append(SpringGroup(group.string, totalArr))

        for group in splitSpringGroups:
            print("spring group", group, group.guessArrangement()[1])


        # sizedGroups = []
        # for group in groups:
        #     if len(group.string) >= maxNum:
        #         sizedGroups.append(group)
        # print(sizedGroups)
        # if there's only one sizedGroup, slot that number in there, and generate more springGroups
        # still with question marks, but it should be fewer

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
                    if self.arrangement[groupId] != len(currentGroup):
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

    # testing
    # g = SpringGroup("???.###", [1,1,3])
    # print(g.reduce())
    for group in springGroups:
        print(group, group.reduce())

    # g = SpringGroup("??", [1])
    # print("answer", g.guessArrangement())

    # # pool = Pool()
    # # processes = []
    #
    # answer = 0
    # for group in springGroups:
    #     group.unfold()
    #     print("starting", group, group.numUnknownSprings)
    #     # a = group.guessArrangement()
    #     # answer += a
    #     # processes.append(pool.apply_async(group.guessArrangement))
    #
    # # for process in processes:
    # #     group, a = process.get()
    # #     print("finished processing", group, a)
    # #     answer += a
    # print(answer)



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
