import copy
import math
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        startPos = None
        rocks = set()
        j = 0
        for line in file:
            line = line.strip()
            for i in range(len(line)):
                char = line[i]
                if char == "#":
                    rocks.add((i, j))
                elif char == "S":
                    startPos = (i, j)
            j += 1
        return startPos, rocks, i + 1, j

def part1():
    startPos, rocks, _, _ = parseInput(21)
    # print(startPos, rocks)

    num_steps = 64

    elf_locations = {startPos}
    for step in range(num_steps):
        elf_locations2 = set()
        for loc in elf_locations:
            x, y = loc
            for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                nextPos = (x2, y2)
                if nextPos not in rocks:
                    elf_locations2.add(nextPos)
        elf_locations = elf_locations2
        print(elf_locations)
    print(len(elf_locations))

def get_tile(pos, w, h):
    x, y = pos
    x2 = math.floor(x / w)
    y2 = math.floor(y / h)
    return x2, y2

def rock_to_tile(rock, tile, w, h):
    t1, t2 = tile
    r1, r2 = rock
    x = r1 + (t1 * w)
    y = r2 + (t2 * h)
    return x, y

def print_center_tile(elf_locations, rocks, w, h):
    for j in range(h):
        for i in range(w):
            if (i, j) in elf_locations:
                print("O", end="")
            elif (i, j) in rocks:
                print("#", end="")
            else:
                print(".", end="")
        print()

def print_area(elf_locations, rocks, minX, maxX, minY, maxY):
    for j in range(minX, maxX):
        for i in range(minY, maxY):
            if (i, j) in elf_locations:
                print("O", end="")
            elif (i, j) in rocks:
                print("#", end="")
            else:
                print(".", end="")
        print()

# insight:
# once the center tile gets filled out, spots "alternate" between on and off
# ...also the rate at which we grow might be something tha can be graphed and predicted
def part2():
    startPos, rocks, w, h = parseInput(21)
    # print(startPos, rocks)
    # print(w, h)

    # takes 20 minutes to do 1000
    num_steps = 30

    orig_rocks = copy.deepcopy(rocks)
    seen_tiles = set()

    elf_locations = {startPos}
    minX = minY = 0
    maxX = w
    maxY = h
    # steps_plt = []
    # step_counts = []
    for step in range(num_steps):
        if step % 1 == 0:
            print("step", step)
            # print("elf locations", len(elf_locations))
            # print(elf_locations)
            # steps_plt.append(step)
            # step_counts.append(len(elf_locations))
            # print_center_tile(elf_locations, rocks, w, h)
            print_area(elf_locations, rocks, minX, maxX, minY, maxY)
        print(seen_tiles)
        print()
        elf_locations2 = set()
        for loc in elf_locations:
            x, y = loc
            for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                nextPos = (x2, y2)
                # idea: compute where the rocks are dynamically?
                # figure out what tile we're in
                tile = get_tile(loc, w, h)
                if tile not in seen_tiles:
                    # get all that tiles rocks
                    for rock in orig_rocks:
                        new_rock = rock_to_tile(rock, tile, w, h)
                        rocks.add(new_rock)
                    seen_tiles.add(tile)
                # then check if this pos is in that list of rocks
                if nextPos not in rocks:
                    elf_locations2.add(nextPos)
                    # update mins
                    if x2 < minX:
                        minX = x
                    if x2 > maxX:
                        maxX = x
                    if y2 < minY:
                        minY = y2
                    if y2 > maxY:
                        maxY = y2
        elf_locations = elf_locations2
        # print(elf_locations)

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
