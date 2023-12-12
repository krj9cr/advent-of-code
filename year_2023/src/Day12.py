import itertools
import time
import copy

class SpringGroup:
    def __init__(self, springs, arrangement):
        self.springs = springs
        self.arrangement = arrangement

    def __str__(self):
        return self.springs + " " + str(self.arrangement)

    def satisfiesArrangement(self, springs):
        groups = []
        currentGroup = ""
        for char in springs:
            if char == "#":
                currentGroup += char
            else:
                if currentGroup != "":
                    groups.append(len(currentGroup))
                    currentGroup = ""
        if currentGroup != "":
            groups.append(len(currentGroup))
        return groups == self.arrangement

    def guessArrangement(self):
        # print(self)
        # how many question marks
        numQuestions = 0
        for char in self.springs:
            if char == "?":
                numQuestions += 1
        # print(numQuestions)

        # get all possible combos of filling in the question marks
        combos = list(itertools.product([".", "#"], repeat=numQuestions))
        answer = 0
        for combo in combos:
            springs = ""
            c = 0
            for i in range(len(self.springs)):
                char = self.springs[i]
                if char == "?":
                    springs += combo[c]
                    c += 1
                else:
                    springs += char
            print(springs)
            # check if this satisfies and count it
            if self.satisfiesArrangement(springs):
                answer += 1
        return answer

    def unfold(self):
        c = copy.deepcopy(self.springs)
        for i in range(4):
            self.springs += "?" + c
        # print(self.springs)
        c = copy.deepcopy(self.arrangement)
        for i in range(4):
            self.arrangement += c
        # print(self.arrangement)


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
        a = group.guessArrangement()
        print(group, a)
        answer += a
    print(answer)

    # testing
    # g = SpringGroup("???.###", [1, 1, 3])
    # print(g.satisfiesArrangement("...#...#.###..."))
    # print(g.guessArrangement())

def part2():
    springGroups = parseInput(12)
    answer = 0
    for group in springGroups:
        group.unfold()
        a = group.guessArrangement()
        print(group, a)
        answer += a
    print(answer)

    # testing
    # g = SpringGroup("???.###", [1,1,3])
    # print(g.unfold())

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
