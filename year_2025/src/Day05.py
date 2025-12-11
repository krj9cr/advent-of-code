import copy
import time, os

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        freshRanges = []
        availableIngredients = []
        available = False
        for line in file:
            line = line.strip()
            if line == "":
                available = True
                continue
            if available:
                availableIngredients.append((int(line)))
            else:
                line = line.split("-")
                freshRanges.append((int(line[0]), int(line[1])))

        return freshRanges, availableIngredients

def part1():
    freshRanges, availableIngredients = parseInput()
    # print(freshRanges)
    # print(availableIngredients)

    total = 0
    for ingredient in availableIngredients:
        for minR, maxR in freshRanges:
            if minR <= ingredient <= maxR:
                # print(ingredient, "is freshly between", minR, "-", maxR)
                total += 1
                break
    print(total)


def part2():
    freshRanges, availableIngredients = parseInput()

    total = 0
    freshRanges = sorted(freshRanges)

    merged = []
    for start, end in freshRanges:
        # 2. If the list of merged intervals is empty or the current range
        #    does not overlap with the previous one, append it
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        # 3. Otherwise, there is an overlap, so merge the current and previous
        #    intervals by updating the end time of the previous one
        else:
            merged[-1][1] = max(merged[-1][1], end)

    freshRanges = [tuple(r) for r in merged]

    for minR, maxR in freshRanges:
        # print(minR, maxR)
        amount = maxR - minR + 1
        # print(amount)
        total += amount
    print()
    print(total)

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
