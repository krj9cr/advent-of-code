import time, os
from collections import deque

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

def custom_bfs(splitLocations, start, w, h):
    queue = deque([start])
    visited = set([])
    times_split = 0

    while queue:
        # print("queue:", queue)
        curr = queue.popleft()
        # print("current", curr)
        x, y = curr

        if x < w and y < h:
            next = (x, y + 1)
            if next in splitLocations:
                # split
                next1 = (x - 1, y + 1)
                next2 = (x + 1, y + 1)
                visited.add(next1)
                queue.append(next1)
                visited.add(next2)
                queue.append(next2)

                times_split += 1
            else:
                if next not in visited:
                    visited.add(next)
                    queue.append(next)

    print("split", times_split)
    return visited

def part1():
    start, splitLocations, w, h = parseInput()
    # print(start)
    # print(splitLocations)
    # print(w, h)

    visited = custom_bfs(splitLocations, start, w, h)

    # print graph
    # for j in range(h):
    #     for i in range(w):
    #         if (i, j) in splitLocations:
    #             print("^", end="")
    #         elif (i, j) in visited:
    #             print("|", end="")
    #         else:
    #             print(".", end="")
    #     print()

cache = {}

def count_unique_paths_dfs(splitLocations, start, w, h):
    if start in cache:
        return cache[start]

    x, y = start

    # print(x,y)
    count = 0

    if x < w and y < h:
        next = (x, y + 1)
        if next in splitLocations:
            # split
            next1 = (x - 1, y + 1)
            next2 = (x + 1, y + 1)

            count += count_unique_paths_dfs(splitLocations, next1, w, h)
            count += count_unique_paths_dfs(splitLocations, next2, w, h)
        else:
            count += count_unique_paths_dfs(splitLocations, next, w, h)
    else:
        cache[start] = 1
        return 1

    cache[start] = count
    return count

def part2():
    start, splitLocations, w, h = parseInput()

    visited = count_unique_paths_dfs(splitLocations, start, w, h)

    print(visited)



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
