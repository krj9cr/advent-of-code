import copy
import time
import heapq

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        grid = []
        for line in file:
            line = line.strip()
            grid.append([char for char in line])
        return grid

def print_2d_grid(grid, points=None):
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if points and (i,j) in points:
                print("O", end="")
            else:
                print(item, end="")
        print()
    print()

# A custom priority queue used for A Star Search below
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

# guesses the cost of going from current position to goal
# should always underestimate the actual cost
def heuristic(goal, x2, y2):
    (x1, y1) = goal
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

def a_star_search(board, start, goal):
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    queue.put((start[0], start[1]), 0)
    came_from[(start[0], start[1])] = None
    cost_so_far[(start[0], start[1])] = 0

    while not queue.empty():
        x, y = queue.get()

        if (x, y) == goal:
            break

        up = (x, y - 1)
        down = (x, y + 1)
        left = (x - 1, y)
        right = (x + 1, y)
        # for each adjacent square
        for x2, y2 in (up, down, left, right):
            cost_to_move = 1
            # Try to move
            new_cost = cost_so_far[(x, y)] + cost_to_move
            # if we're not out of bounds
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                next_spot = (x2, y2)
                if board[y2][x2] != "#":
                    if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                        cost_so_far[next_spot] = new_cost
                        priority = new_cost + heuristic(goal, x2, y2)
                        queue.put((next_spot[0], next_spot[1]), priority)
                        came_from[next_spot] = (x, y)
    return came_from, cost_so_far


def part1():
    grid = parseInput(20)
    print(grid)

    h = len(grid)
    w = len(grid[0])
    start = None
    end = None
    # find start and end
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if item == "S":
                start = (i, j)
            elif item == "E":
                end = (i, j)
    print(start, end)

    def find_path(da_grid):
        came_from, cost_so_far = a_star_search(da_grid, start, end)

        if cost_so_far[end]:
            # curr = end
            # path = []
            # while curr is not None:
            #     curr = came_from[curr]
            #     path.append(curr)
            # print_2d_grid(grid, path)
            return cost_so_far[end]

    # find the initial path
    initial_race_length = find_path(grid)
    print("INITIAL RACE LENGTH", initial_race_length)


    # dumb idea: remove every wall that's not part of the borders and compute the new path
    # if the new path saves at least 100 steps, count it
    total = 0
    savings = {}
    for j in range(1, h-1):
        for i in range(1, w-1):
            if grid[j][i] == "#":
                # make a new grid without this spot
                tmp_grid = copy.deepcopy(grid)
                tmp_grid[j][i] = "."
                # run astar and check length
                race_length = find_path(tmp_grid)
                if race_length is not None:
                    length_savings = initial_race_length - race_length
                    if 0 < length_savings >= 100:
                        print("Shorter path for ", (i, j), "saves", length_savings)
                        total += 1
                        if savings.get(length_savings) is not None:
                            savings[length_savings] += 1
                        else:
                            savings[length_savings] = 1
    print(savings)
    print("Total paths with savings", total)

def manhattan(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1])

def get_diamond(grid, w, h, point, n=20):
    points = []
    for j in range(h):
        for i in range(w):
            if (i, j) == point:
                continue
            if manhattan((i, j), point) < n:
                item = grid[j][i]
                if item == "." or item == "E":
                    points.append((i, j))
    return points

def part2():
    grid = parseInput(20)
    # print(grid)

    h = len(grid)
    w = len(grid[0])
    start = None
    end = None
    # find start and end
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if item == "S":
                start = (i, j)
            elif item == "E":
                end = (i, j)
    # print(start, end)

    memo = {}
    def find_path(da_grid, s=start, e=end):
        if memo.get((s, e)) is not None:
            return memo[(s, e)]
        came_from, cost_so_far = a_star_search(da_grid, s, e)

        if cost_so_far[e]:
            curr = e
            path = []
            while curr is not None:
                path.append(curr)
                curr = came_from[curr]
            # print_2d_grid(grid, path)
            memo[(s, e)] = (cost_so_far[e], path)
            return cost_so_far[e], path
        memo[(s, e)] = (None, None)
        return None, None

    # find the initial path
    initial_race_length, initial_path = find_path(grid)
    print("INITIAL RACE LENGTH", initial_race_length)

    total = 0
    savings = {}
    # dumb part 2 extension: ...along the initial path... for every spot, try "activating" the cheat
    for i, cheat_start in enumerate(reversed(initial_path)):
        if cheat_start == end:
            continue
        print(i, "cheat_start", cheat_start)
        # from the cheat spot, take all unique "." points within 20 steps and call that the "end" cheat spot
        # generate all points from this point within 20 steps
        cheat_end_points = get_diamond(grid, w, h, cheat_start, 21)
        # print(cheat_end_points)
        # print_2d_grid(grid, cheat_end_points)

        # find path from start to cheat_start
        if start == cheat_start:
            path_length1 = 0
        else:
            path_length1, _ = find_path(grid, start, cheat_start)

        # effectively "erase" the walls/steps within the cheat path
        for cheat_end in cheat_end_points:
            # TODO: maybe we can not worry about paths where like... savings isn't enough somehow...
            path_length3 = manhattan(cheat_start, cheat_end)
            # if manhattan(start, cheat_start) + path_length3 + manhattan(cheat_end, end) >= initial_race_length:
            #     continue

            # find path from cheat_end to end
            if end == cheat_end:
                path_length2 = 0
            else:
                path_length2, _ = find_path(grid, cheat_end, end)
            # add in manhattan distance length between cheat_start and cheat_end
            if path_length1 is not None and path_length2 is not None:
                race_length = path_length1 + path_length2 + path_length3
                # print_2d_grid(grid, path1+path2)
                length_savings = initial_race_length - race_length
                # print("cheat_end", cheat_end, "len", race_length, "savings", length_savings)
                if length_savings >= 100:
                    total += 1
                    if savings.get(length_savings) is not None:
                        savings[length_savings] += 1
                    else:
                        savings[length_savings] = 1

    for key in sorted(savings.keys()):
        print(savings[key], "cheats that save", key, "seconds")
    print("total", total)

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
