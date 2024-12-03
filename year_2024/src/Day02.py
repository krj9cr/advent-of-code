import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            row = []
            line = line.strip()
            line = line.split()
            for item in line:
                row.append(int(item))
            lines.append(row)
        return lines

def part1():
    lines = parseInput(2)
    total = 0
    for report in lines:
        print("Report: ", report)
        firstDiff = report[1] - report[0]
        decreasing = False
        if firstDiff < 0:
            decreasing = True

        isSafe = True
        for i in range(0, len(report)-1):
            item1 = report[i]
            item2 = report[i+1]
            if decreasing:
                diff = item1-item2
                if diff < 0:
                    print("Unsafe, increase", item1, item2)
                    isSafe = False
                    break
            else:
                diff = item2-item1
                if diff < 0:
                    print("Unsafe, decrease", item1, item2)
                    isSafe = False
                    break

            if diff > 3 or diff == 0:
                isSafe = False
                print("Unsafe: ", item1, item2, "is ", diff)
                break
        if isSafe:
            total += 1
    print(total)

def checkReport(report):
    print("Checking:", report)
    firstDiff = report[1] - report[0]
    decreasing = False
    if firstDiff < 0:
        decreasing = True

    isSafe = True
    for i in range(0, len(report) - 1):
        item1 = report[i]
        item2 = report[i + 1]
        if decreasing:
            diff = item1 - item2
            if diff < 0:
                print("Unsafe, increase", item1, item2)
                isSafe = False
                break
        else:
            diff = item2 - item1
            if diff < 0:
                print("Unsafe, decrease", item1, item2)
                isSafe = False
                break

        if diff > 3 or diff == 0:
            isSafe = False
            print("Unsafe: ", item1, item2, "is ", diff)
            break
    return isSafe

def part2():
    lines = parseInput(2)
    total = 0
    for report in lines:
        print(report)
        isSafe = checkReport(report)
        if isSafe:
            print("Safe")
            print()
            total += 1
        else:
            for j in range(0, len(report)):
                copyReport = report[:]
                copyReport.pop(j)
                isSafe = checkReport(copyReport)
                if isSafe:
                    print("Safe by", copyReport)
                    print()
                    total += 1
                    break
    print(total)

# 274 too low
# 776 too high

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
