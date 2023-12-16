import sys
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        mirrors = {}
        j = 0
        for line in file:
            line = line.strip()
            for i in range(len(line)):
                char = line[i]
                if char != ".":
                    mirrors[(i, j)] = char
            j += 1
        return mirrors, i+1, j

# 0 up
# 1 right
# 2 down
# 3 left

def part1():
    mirrors, w, h = parseInput(16)
    print(mirrors)
    print(w, h)
    beams = [(0, 0, 1)]

    seen = set()
    seenMirrors = set()

    for step in range(1000):
        newBeams = []
        for beam in beams:
            newBeam = None
            i, j, direction = beam
            # check if the beam went out of bounds, and continue (let it die) if so
            if i < 0 or i >= w or j < 0 or j >= h:
                continue
            # move the beam
            if (i, j) in mirrors:
                mirror = mirrors[(i, j)]
                if mirror == "\\":
                    # if beam not in seenMirrors:
                    if direction == 0:  # go left
                        newBeam = (i - 1, j, 3)
                    elif direction == 1:  # go down
                        newBeam = (i, j + 1, 2)
                    elif direction == 2:  # go right
                        newBeam = (i + 1, j, 1)
                    elif direction == 3:  # go up
                        newBeam = (i, j - 1, 0)
                    newBeams.append(newBeam)
                elif mirror == "/":
                    if direction == 0:  # go right
                        newBeam = (i + 1, j, 1)
                    elif direction == 1:  # go up
                        newBeam = (i, j - 1, 0)
                    elif direction == 2:  # go left
                        newBeam = (i - 1, j, 3)
                    elif direction == 3:  # go down
                        newBeam = (i, j + 1, 2)
                    newBeams.append(newBeam)
                elif mirror == "|":  # split into two
                    if (i, j) not in seen:
                        beam1 = (i, j - 1, 0)
                        beam2 = (i, j + 1, 2)
                        newBeams.append(beam1)
                        newBeams.append(beam2)
                elif mirror == "-":
                    if (i, j) not in seen:
                        beam1 = (i - 1, j, 3)
                        beam2 = (i + 1, j, 1)
                        newBeams.append(beam1)
                        newBeams.append(beam2)
            # keep moving in same direction
            else:
                if direction == 0:  # up
                    newBeam = (i, j - 1, direction)
                elif direction == 1:  # right
                    newBeam = (i + 1, j, direction)
                elif direction == 2:  # down
                    newBeam = (i, j + 1, direction)
                elif direction == 3:  # left
                    newBeam = (i - 1, j, direction)
                else:
                    print("UH OH direction", direction)
                    sys.exit(1)
                newBeams.append(newBeam)

            seen.add((i, j))
        beams = newBeams
        # print(beams)
        print(len(seen))
    print(seen)
    for j in range(h):
        for i in range(w):
            if (i,j) in seen:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print(len(seen))

def part2():
    lines = parseInput(16)
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
