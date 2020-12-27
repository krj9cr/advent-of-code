

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return sorted([parseLine(line) for line in file])

def parseLine(line: str):
    return int(line.strip())

###########################
# part1
###########################
def part1(data):
    print(data)
    charge = 0
    prev = 0
    joltdiffs = {1: 0, 3:0}
    for i in range(len(data)):
        diff = data[i] - prev
        # print("Charge", charge, "val", data[i], "diff", diff)
        if diff == 1:
            joltdiffs[1] += 1
        elif diff == 3:
            joltdiffs[3] += 1
        charge += data[i]
        prev = data[i]
    joltdiffs[3] +=1
    print(joltdiffs)
    print(joltdiffs[1] * joltdiffs[3])

def runpart1():
    part1(parseInputFile())

cache = {}

def idk(data, i, prev, limit):
    if i in cache:
        return cache[i]
    res = 0
    if prev >= limit:
        return 1
    if i + 1 < len(data) and data[i+1] - prev <= 3:
        res += idk(data, i+1, data[i+1], limit)
    if i + 2 < len(data) and data[i+2] - prev <= 3:
        res += idk(data, i+2, data[i+2], limit)
    if i + 3 < len(data) and data[i+3] - prev <= 3:
        res += idk(data, i+3, data[i+3], limit)
    cache[i] = res
    return res

###########################
# part2
###########################
def part2(data):
    print(data)
    limit = data[-1]
    res = idk(data, -1, 0, limit)
    print(res)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
