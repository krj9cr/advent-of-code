import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        line = [line.strip() for line in file][0]
        return line.split(',')

def HASH(string):
    curr = 0
    for char in string:
        ascii_code = ord(char)
        print("ascii_code", ascii_code)
        curr += ascii_code
        print("curr", curr)
        curr *= 17
        curr %= 256
    return curr

def part1():
    steps = parseInput(15)
    print(steps)

    answer = 0
    for step in steps:
        print(step)
        answer += HASH(step)
    print(answer)


def part2():
    True

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
