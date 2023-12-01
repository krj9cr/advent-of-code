import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

def part1():
    lines = parseInput(1)
    nums = []
    for line in lines:
        numStr = ""
        for char in line:
            if char.isdecimal():
                numStr += char
        num = int(numStr[0] + numStr[-1])
        nums.append(num)
    print(sum(nums))

def part2():
    lines = parseInput(1)
    nums = []

    for line in lines:
        numStr = ""
        i = 0
        buf3 = ""
        buf4 = ""
        buf5 = ""
        while i < len(line):
            char = line[i]
            if char.isalpha():
                buf3 += char
                buf4 += char
                buf5 += char
                if len(buf3) > 3:
                    buf3 = buf3[1:4]
                if len(buf4) > 4:
                    buf4 = buf4[1:5]
                if len(buf5) > 5:
                    buf5 = buf5[1:6]
                # print(buf3, buf4, buf5)
                if buf3 == "one":
                    numStr += "1"
                if buf3 == "two":
                    numStr += "2"
                if buf3 == "six":
                    numStr += "6"
                if buf4 == "four":
                    numStr += "4"
                if buf4 == "five":
                    numStr += "5"
                if buf4 == "nine":
                    numStr += "9"
                if buf5 == "three":
                    numStr += "3"
                if buf5 == "seven":
                    numStr += "7"
                if buf5 == "eight":
                    numStr += "8"
            else:
                numStr += char

            i += 1
        # print(numStr)
        num = int(numStr[0] + numStr[-1])
        nums.append(num)
        # print(num)
    print(sum(nums))

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    total = end - start
    print("Time (ms):", (end - start) * 1000)
