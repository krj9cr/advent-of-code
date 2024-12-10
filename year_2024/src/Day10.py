import copy
import time
from collections import deque

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            row = [int(char) for char in line]
            lines.append(row)
        return lines

def print_2d_grid(grid, points=None):
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            if points and (i,j) not in points:
                print(".",end="")
            else:
                item = row[i]
                print(item, end="")
        print()
    print()

def bfs_2d_grid(grid, start, nines):
    ends = copy.deepcopy(nines)
    score = 0
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        currentItem = grid[y][x]
        if (x, y) in ends:
            ends.remove((x, y))
            score += 1
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                next = (x2, y2)
                nextItem = grid[y2][x2]
                if next not in seen and nextItem - currentItem == 1:
                    queue.append(path + [next])
                    seen.add(next)
    return score, path

def part1():
    grid = parseInput(10)
    print_2d_grid(grid)

    nines = set()
    # find 9's
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if item == 9:
                nines.add((i, j))
    print(nines)

    # find zeros
    total = 0
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if item == 0:
                score, path = bfs_2d_grid(grid, (i, j), nines)
                print((i, j), "SCORE:", score)
                total += score
                print_2d_grid(grid, path)
    print(total)

def bfs_2d_grid_part2(grid, curr, nines, seen_ends):
    x, y = curr
    currentItem = grid[y][x]
    if (x, y) in nines:
        # print("AT end", x,y)
        if seen_ends.get((x, y)):
            seen_ends[(x, y)] += 1
        else:
            seen_ends[(x, y)] = 1
    for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
        if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
            nextItem = grid[y2][x2]
            if nextItem - currentItem == 1:
                bfs_2d_grid_part2(grid, (x2, y2), nines, seen_ends)
    # print(seen_ends)
    return seen_ends

def part2():
    grid = parseInput(10)
    # print_2d_grid(grid)

    nines = set()
    # find 9's
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if item == 9:
                nines.add((i, j))
    # print(nines)

    # find zeros
    total = 0
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if item == 0:
                seen = bfs_2d_grid_part2(grid, (i, j), nines, {})
                # print("SEEN:", seen)
                for nine in seen:
                    total += seen[nine]
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
