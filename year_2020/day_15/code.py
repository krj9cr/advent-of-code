import time

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return parseLine(file.readlines()[0])

def parseLine(line: str):
    l = line.strip().split(",")
    return [ int(s) for s in l ]

def runGame(data, endTurn):
    # print(data)
    turn = 1
    spoken = {}
    last = None
    for num in data:
        spoken[num] = turn
        last = num
        # print(last)
        turn += 1
    while turn <= endTurn:
        # if turn % 10000 == 0:
        #     print(turn)
        prev = last
        lastturn = spoken.get(last)
        if lastturn is not None:
            last = turn - 1 - lastturn
            # print("turn", turn,"lastturn", lastturn)
        else:
            last = 0
        spoken[prev] = turn - 1
        # print(spoken)
        # print(spokentwice)
        # print("speak",last)
        turn += 1
    print(last)

###########################
# part1
###########################
def part1(data):
    runGame(data, 2020)

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
    runGame(data, 30000000)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
