import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        # lines = [line.strip() for line in file]
        # groups = []
        # currGroup = 0
        # for line in lines:
        #     if line == "":
        #         groups.append(currGroup)
        #         currGroup = 0
        #     else:
        #         currGroup += int(line)
        # return groups
        lines = [line.strip() for line in file]
        return lines

def part1():
    lines = parseInput(1)
    nums = []
    for line in lines:
        numStr = ""
        for char in line:
            try:
                c = int(char)
                numStr += char
            except:
                continue
        num = int(numStr[0] + numStr[-1])
        nums.append(num)
    print(sum(nums))
    # print(max(lines))

def part2():
    lines = parseInput(1)
    nums = []

    for line in lines:
        numStr = ""
        i = 0
        while i < len(line):
            char = line[i]
            # print(char)
            if char == "o":
                if i+2 < len(line) and line[i+1] == "n" and line[i+2] == "e":
                    numStr += "1"
            elif char == "t":
                if i+2 < len(line) and line[i+1] == "w" and line[i+2] == "o":
                    numStr += "2"
                elif i+4 < len(line) and line[i+1] == "h" and line[i+2] == "r" and line[i+3] == "e" and line[i+4] == "e":
                    numStr += "3"
            elif char == "f":
                if i+3 < len(line) and line[i+1] == "o" and line[i+2] == "u" and line[i+3] == "r":
                    numStr += "4"
                elif i+3 < len(line) and line[i+1] == "i" and line[i+2] == "v" and line[i+3] == "e":
                    numStr += "5"
            elif char == "s":
                if i+2 < len(line) and line[i+1] == "i" and line[i+2] == "x":
                    numStr += "6"
                elif i+4 < len(line) and line[i+1] == "e" and line[i+2] == "v" and line[i+3] == "e" and line[i+4] == "n":
                    numStr += "7"
            elif char == "e":
                if i+4 < len(line) and line[i+1] == "i" and line[i+2] == "g" and line[i+3] == "h" and line[i+4] == "t":
                    numStr += "8"
            elif char == "n":
                if i+3 < len(line) and line[i+1] == "i" and line[i+2] == "n" and line[i+3] == "e":
                    numStr += "9"
            else:
                try:
                    c = int(char)
                    numStr += char
                except:
                    True

            i += 1
        # print(numStr)
        num = int(numStr[0] + numStr[-1])
        nums.append(num)
        print(num)
    print(sum(nums))

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # total = end - start
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)
