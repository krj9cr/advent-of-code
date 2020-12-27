import time

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return int(line.strip())

def reverse_transform(subject, target):
    val = 1
    loopsize = 0
    while val != target:
        val *= subject
        val %= 20201227
        loopsize += 1
    return loopsize

def transform(subject, loopsize):
    val = 1
    for l in range(loopsize):
        val *= subject
        val %= 20201227
    return val

###########################
# part1
###########################
def part1(data):
    print(data)
    card_public = data[0]
    door_public = data[1]

    card_loop_size = reverse_transform(7, card_public)
    door_loop_size = reverse_transform(7, door_public)

    encryption_key = transform(door_public, card_loop_size)
    print("res", encryption_key)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def part2(data):
    print(data)

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\nPART 2 RESULT")
    # runpart2()
