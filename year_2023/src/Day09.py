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

def allZeros(sequence):
    for s in sequence:
        if s != 0:
            return False
    return True

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
        # print("done")
        num = sequences[-1][0]
        for i in range(len(sequences)-2, -1, -1):
            sequence = sequences[i]
            sequence.append(sequence[-1] + num)
            num = sequence[-1]
        # print(sequences)
        value = sequences[0][-1]
        # print(value)
        answer += value
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
        # sequences = list(reversed(sequences))[1:]
        # print(sequences)
        # print("done")
        num = sequences[-1][0]
        newSeqs = []
        for i in range(len(sequences)-2, -1, -1):
            sequence = sequences[i]
            sequence = [sequence[0] - num] + sequence
            newSeqs.append(sequence)
            # print(sequence)
            num = sequence[0]
        # print(newSeqs)
        value = newSeqs[-1][0]
        # print(value)
        answer += value
    print(answer)

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
