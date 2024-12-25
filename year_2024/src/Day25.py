import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        grids = []
        current_grid = []
        for line in file:
            line = line.strip()
            if line == "":
                grids.append(current_grid)
                current_grid = []
            else:
                current_grid.append(line)

        grids.append(current_grid)
        return grids

def grids_to_keys_and_locks(grids):
    a = []
    b = []
    for grid in grids:
        if grid[0] == "#####":
            cols = [0, 0, 0, 0, 0]
            for row in grid[1:]:
                for i in range(5):
                    if row[i] == "#":
                        cols[i] += 1
            a.append(cols)
        else:
            cols = [0, 0, 0, 0, 0]
            for row in grid[:-1]:
                for i in range(5):
                    if row[i] == "#":
                        cols[i] += 1
            b.append(cols)
    return a, b


def part1():
    grids = parseInput(25)
    print(grids)
    locks, keys = grids_to_keys_and_locks(grids)
    print(locks)
    print(keys)

    # try to fit every key with every lock
    total = 0
    for key in keys:
        for lock in locks:
            fit = True
            for i in range(5):
                if key[i] + lock[i] > 5:
                    fit = False
                    break
            if fit:
                total += 1
    print(total)


def part2():
    lines = parseInput(25)
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
