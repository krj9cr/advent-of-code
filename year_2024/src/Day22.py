import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(int(line))
        return lines

def part1():
    secrets = parseInput(22)
    print(secrets)

    total = 0
    for secret in secrets:
        print(secret)
        for i in range(2000):
            one = secret * 64
            newSecret = secret ^ one
            newSecret = newSecret % 16777216
            two = newSecret // 32
            newSecret = newSecret ^ two
            newSecret = newSecret % 16777216
            three = newSecret * 2048
            newSecret = newSecret ^ three
            newSecret = newSecret % 1677721
            secret = newSecret
        print(secret)
        total += secret
        print()
    print("Total", total)

def part2():
    lines = parseInput(22)
    print(lines)

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
