import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip("") for line in file][0]
        return lines

def check(line, windowSize):
    for i in iter(range(len(line) - 2)):
        window = line[i:i + windowSize]
        # print(window)
        charcount = {}

        allOnes = True
        for char in window:
            if charcount.get(char) is not None:
                allOnes = False
                break
            else:
                charcount[char] = 1
        # print(charcount)
        if allOnes:
            print(window)
            print(line.index(window)+windowSize)
            break


def part1():
    line = parseInput(6)
    # print(line)
    check(line, 4)

def part2():
    line = parseInput(6)
    # print(line)
    check(line, 14)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
