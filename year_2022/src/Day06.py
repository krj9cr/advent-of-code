import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip("") for line in file][0]
        return lines

def part1():
    line = parseInput(6)
    print(line)

    windows = [line[i:i + 4] for i in iter(range(len(line) - 2))]
    for window in windows:
        print(window)
        charcount = {}
        for char in window:
            if charcount.get(char) is not None:
                charcount[char] += 1
            else:
                charcount[char] = 1
        allOnes = True
        for key, val in charcount.items():
            if val > 1:
                allOnes = False
                break
        print(charcount)
        if allOnes:
            print(window)
            print(line.index(window)+4)
            break

    # acc = ""
    # for i in range(len(line)):
    #     char = line[i]
    #     print(i+1, acc, "char:", char)
    #     if char not in acc:
    #         acc += char
    #     else:
    #
    #         acc = acc[1:] + char
    #     if len(acc) == 4:
    #         print(acc, i+1)
    #         break


def part2():
    line = parseInput(6)
    print(line)

    windows = [line[i:i + 14] for i in iter(range(len(line) - 2))]
    for window in windows:
        print(window)
        charcount = {}
        for char in window:
            if charcount.get(char) is not None:
                charcount[char] += 1
            else:
                charcount[char] = 1
        allOnes = True
        for key, val in charcount.items():
            if val > 1:
                allOnes = False
                break
        print(charcount)
        if allOnes:
            print(window)
            print(line.index(window)+14)
            break

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time:", end - start)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time:", end - start)
