

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseFile(path: str):
    with open(path, 'r') as file:
        return parseInput(file)

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return line.strip()

def seatNumber(line: str):
    low = 0
    high = 127
    row = 0
    for letter in line[0:6]:
        mid = (high + low) // 2
        # print("low", low, "high", high, "mid", mid)
        if letter == "F":
            high = mid
        elif letter == "B":
            low = mid + 1
    if line[6] == "F":
        row = low
    elif line[6] == "B":
        row = high

    low = 0
    high = 7
    col = 0
    for letter in line[-3:]:
        mid = (high + low) // 2
        # print("low", low, "high", high, "mid", mid)
        if letter == "L":
            high = mid
        elif letter == "R":
            low = mid + 1
    if line[-1] == "L":
        col = low
    elif line[-1] == "R":
        col = high
    # print("row",row,"col",col)
    return (row * 8) + col

###########################
# part1
###########################
def part1(data):
    print(data)
    m = 0
    for line in data:
        wow = seatNumber(line)
        if wow > m:
            m = wow
    print(m)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)
    m = 938
    seats = []
    for line in data:
        seats.append(seatNumber(line))
    print(sorted(seats))
    for i in range(seats[0], m+1):
        if i not in seats:
            print(i)

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
