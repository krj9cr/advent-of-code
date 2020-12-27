import time
from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return parseLine(file.readlines()[0])

def parseLine(line: str):
    l = line.strip().split(",")
    return [ int(s) for s in l ]

###########################
# part1
###########################
def part1(data):
    print(data)
    twice = set()
    turn = 0
    spoken = []
    for num in data:
        spoken.append(num)
        turn += 1
    while turn < 2020:
        print(turn)
        last = spoken[-1]
        if last not in spoken[:-1]:
            spoken.append(0)
        else:
            lastturn = -1
            for i in range(len(spoken)-2, -1, -1):
                if spoken[i] == last:
                    lastturn = i
                    break
            print(lastturn)
            val = turn - lastturn - 1
            spoken.append(val)
        print(spoken)
        turn += 1
    print(spoken[-1])

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
# almost same algorithm as part one, but use dicts
# instead of a long list that would prob eat up memory
def part2(data):
    print(data)
    twice = set()
    turn = 1
    spoken = {}
    spokentwice = {}
    last = None
    for num in data:
        spoken[num] = turn
        last = num
        print(last)
        turn += 1
    while turn <= 30000000:
        if turn % 10000 == 0:
            print(turn)
        if last in spokentwice:
            lastturn = spokentwice[last]
            speak = turn - 1 - lastturn
            last = speak
            if last in spoken:
                spokentwice[last] = deepcopy(spoken[last])
            spoken[last] = turn
            # print("turn", turn,"lastturn", lastturn)
        else:
            last = 0
            if last in spoken:
                spokentwice[last] = deepcopy(spoken[last])
            spoken[last] = turn
        # print(spoken)
        # print(spokentwice)
        # print("speak",last)
        turn += 1
    print(last)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

# not 0 lol

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
