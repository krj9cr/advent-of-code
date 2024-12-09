import time


def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)
        return lines[0]

def part1():
    line = parseInput(9)
    blocks = []
    storage = []
    num_free_spots = 0
    for i in range(len(line)):
        size = int(line[i])
        if i % 2 == 0:
            id = int((i/2))
            for j in range(size):
                storage.append(id)
        else:
            num_free_spots += 1
            for j in range(size):
                storage.append(".")
    # print(storage)
    total_size = len(storage)

    # find first free spot
    free_idx = 0
    for i in range(total_size):
        item = storage[i]
        if item == ".":
            free_idx = i
            break
    # print(free_idx)
    # print(num_free_spots)

    # find last file spot
    file_idx = total_size - 1
    for i in range(file_idx, -1, -1):
        item = storage[i]
        if item != ".":
            file_idx = i
            break
    # print(file_idx)

    count = 0
    while True:
        storage[free_idx] = storage[file_idx]
        storage[file_idx] = "."

        # find next free spot
        for i in range(free_idx + 1, total_size):
            item = storage[i]
            if item == ".":
                free_idx = i
                break

        # find next file spot
        for i in range(file_idx - 1, -1, -1):
            item = storage[i]
            if item != ".":
                file_idx = i
                break
        # print(free_idx, file_idx)

        # print(storage)
        count += 1
        # if count > 10:
        #     break
        if free_idx > file_idx:
            break

    # get answer
    total = 0
    for i in range(total_size):
        item = storage[i]
        if item != ".":
            total += i * storage[i]
        else:
            break
    print(total)




def part2():
    line = parseInput(9)
    blocks = []
    storage = []
    num_free_spots = 0
    for i in range(len(line)):
        size = int(line[i])
        if i % 2 == 0:
            id = int((i / 2))
            for j in range(size):
                storage.append(id)
        else:
            num_free_spots += 1
            for j in range(size):
                storage.append(".")
    # print(storage)
    total_size = len(storage)

    # find first free spot
    free_idx = 0
    for i in range(total_size):
        item = storage[i]
        if item == ".":
            free_idx = i
            break
    # print(free_idx)
    # print(num_free_spots)

    # find last file spot
    file_idx = total_size - 1
    for i in range(file_idx, -1, -1):
        item = storage[i]
        if item != ".":
            file_idx = i
            break
    # print(file_idx)

    count = 0
    while True:
        storage[free_idx] = storage[file_idx]
        storage[file_idx] = "."

        # find next free spot
        for i in range(free_idx + 1, total_size):
            item = storage[i]
            if item == ".":
                free_idx = i
                break

        # find next file spot
        for i in range(file_idx - 1, -1, -1):
            item = storage[i]
            if item != ".":
                file_idx = i
                break
        # print(free_idx, file_idx)

        # print(storage)
        count += 1
        # if count > 10:
        #     break
        if free_idx > file_idx:
            break

    # get answer
    total = 0
    for i in range(total_size):
        item = storage[i]
        if item != ".":
            total += i * storage[i]
        else:
            break
    print(total)

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
