import time, os

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        start = None
        splitLocations = []
        for line in file:
            line = line.strip()
            lines.append(line)

        h = len(lines)
        w = len(lines[0])

        for j in range(h):
            row = lines[j]
            for i in range(w):
                item = row[i]
                if item == "S":
                    start = (i, j)
                elif item == "^":
                    splitLocations.append((i, j))
        return start, splitLocations, w, h

cache = {}

def part1():
    start, splitLocations, w, h = parseInput()

    paths, splits = count_unique_paths_dfs(splitLocations, start, w, h)

    print(splits)
    return paths

def count_unique_paths_dfs(splitLocations, start, w, h):
    if start in cache:
        return cache[start], 0

    x, y = start

    # print(x,y)
    count = 0
    splits = 0

    if x < w and y < h:
        next = (x, y + 1)
        if next in splitLocations:
            # split
            next1 = (x - 1, y + 1)
            next2 = (x + 1, y + 1)

            c1, s1 = count_unique_paths_dfs(splitLocations, next1, w, h)
            c2, s2 = count_unique_paths_dfs(splitLocations, next2, w, h)
            count += c1 + c2
            splits += 1 + s1 + s2
        else:
            c1, s1 = count_unique_paths_dfs(splitLocations, next, w, h)
            count += c1
            splits += s1
    else:
        cache[start] = 1
        return 1, 0

    cache[start] = count
    return count, splits

def part2():
    paths = part1()
    print(paths)


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
