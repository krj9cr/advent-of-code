import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        histories = []
        for line in file:
            line = line.strip()
            line = line.split(" ")
            histories.append([int(n) for n in line])
        return histories

def processSequence(sequence):
    diffs = []
    for i in range(1, len(sequence)):
        diffs.append(sequence[i] - sequence[i-1])
    return diffs

def allSame(sequence):
    first = sequence[0]
    for s in sequence:
        if s != first:
            return False
    return True

def part1():
    histories = parseInput(9)
    # print(histories)

    answer = 0
    for history in histories:
        sequences = [history]
        # generate all the sequences until we end up with one with the same number
        while True:
            sequences.append(processSequence(sequences[-1]))
            if allSame(sequences[-1]):
                break
        # print(sequences)
        num = sequences[-1][0]
        for i in range(len(sequences)-2, -1, -1):
            sequence = sequences[i]
            num = sequence[-1] + num
        # print(sequences)
        answer += num
    print(answer)


def part2():
    histories = parseInput(9)
    # print(histories)

    answer = 0
    for history in histories:
        sequences = [history]
        # generate all the sequences until we end up with one with the same number
        while True:
            sequences.append(processSequence(sequences[-1]))
            if allSame(sequences[-1]):
                break
        # print(sequences)
        num = sequences[-1][0]
        for i in range(len(sequences)-2, -1, -1):
            sequence = sequences[i]
            num = sequence[0] - num
        # print(value)
        answer += num
    print(answer)

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
