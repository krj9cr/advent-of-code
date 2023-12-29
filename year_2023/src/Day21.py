import copy
import math
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy
from Day09 import processSequence, allSame

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
        # print(elf_locations)
    print(len(elf_locations))

def pos_to_tile(pos, w, h):
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

def tile_first_coord(tile, w, h):
    return tile[0] * w, tile[1] * h

def print_tiles(elf_locations, rocks, tiles, w, h):
    # find the mins/maxes
    minX = 0
    maxX = w
    minY = 0
    maxY = h
    tile_coords = []
    for tile in tiles:
        x, y = tile_first_coord(tile, w, h)
        tile_coords.append((x, y))
        if x < minX:
            minX = x
        if x + w > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y + h > maxY:
            maxY = y

    print("tile_coords:", tile_coords)
    print("x", minX, maxX, "y:", minY, maxY)
    for j in range(minY, maxY):
        for i in range(minX, maxX):
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
    print("w/h:", w, h)

    # takes about 20 minutes to do 1000
    num_steps = 65 + (2*131)

    orig_rocks = copy.deepcopy(rocks)
    seen_tiles = set()

    elf_locations = {startPos}
    history = []
    # steps_plt = []
    # step_counts = []
    for step in range(num_steps+1):
        if step == 65 or step == 65 + 131 or step == 65 + (2*131):
            num_elf_locations = len(elf_locations)
            print("step", step, "elf_locations", num_elf_locations)
            history.append(num_elf_locations)
            # print_area(elf_locations, rocks, minX, maxX, minY, maxY)
            # print_tiles(elf_locations, rocks, seen_tiles, w, h)
        # print(seen_tiles)
        # print()
        elf_locations2 = set()
        for loc in elf_locations:
            x, y = loc
            for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
                nextPos = (x2, y2)
                # idea: compute where the rocks are dynamically?
                # figure out what tile we're in
                tile = pos_to_tile(loc, w, h)
                if tile not in seen_tiles:
                    # get all that tiles rocks
                    for rock in orig_rocks:
                        new_rock = rock_to_tile(rock, tile, w, h)
                        rocks.add(new_rock)
                    seen_tiles.add(tile)
                # then check if this pos is in that list of rocks
                if nextPos not in rocks:
                    elf_locations2.add(nextPos)
        elf_locations = elf_locations2

    # read a hint to use Day09 stuff to predict next numbers
    # history = [3955, 35214, 97607]
    # since 202300 * 131 + 65 = 26501365, we generate a sequence of numbers that fits
    for k in range(202300):
        sequences = [history]
        # generate all the sequences until we end up with one with the same number
        while True:
            sequences.append(processSequence(sequences[-1]))
            if allSame(sequences[-1]):
                break
        # print(sequences)
        num = sequences[-1][0]
        for i in range(len(sequences) - 2, -1, -1):
            sequence = sequences[i]
            num = sequence[-1] + num
        # remove one from the front otherwise this will increasingly take forever
        history = history[1:] + [num]
        if k == 202297:  # we use this number because we already computed 3 values in the sequence
            print(k, ":", num)

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
