import time
import itertools


def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append([char for  char in line])
        return lines

def part1():
    grid = parseInput(8)
    w = len(grid[0])
    h = len(grid)
    print(grid)
    print(w, h)
    antennae = {}
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if item != ".":
                if antennae.get(item):
                    antennae[item].append((i, j))
                else:
                    antennae[item] = [(i, j)]
    print(antennae)
    antinodes = set()
    # for all the antenna frequencies
    for frequency in antennae:
        freq_antennae = antennae[frequency]
        print(frequency)
        # for each pair of antennae of the same frequency
        for antenna1, antenna2 in itertools.combinations(freq_antennae, 2):
            # compute anti nodes
            x1, y1 = antenna1[0], antenna1[1]
            x2, y2 = antenna2[0], antenna2[1]
            if antenna1[0] > antenna2[0]:
                x2, y2 = antenna1[0], antenna1[1]
                x1, y1 = antenna2[0], antenna2[1]
            rise = (y2 - y1)
            run = (x2 - x1)
            # get one point ahead and one behind
            before1, before2 = x1 - run, y1 - rise
            after1, after2 = x2 + run, y2 + rise
            if 0 <= before1 < w and 0 <= before2 < h:
                antinodes.add((before1, before2))
            if 0 <= after1 < w and 0 <= after2 < h:
                antinodes.add((after1, after2))
            print((x1, y1), (x2, y2), rise, run, (before1, before2), (after1, after2))
    print(antinodes)
    print(len(antinodes))

def part2():
    lines = parseInput(8)
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
