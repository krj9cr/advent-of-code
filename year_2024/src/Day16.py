import copy
import time
import heapq

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append([char for char in line])
        return lines

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

# See: https://www.redblobgames.com/pathfinding/a-star/implementation.html
# board  - a 2d array of strings or numbers
# start  - a tuple of numbers representing the starting coordinate in the 2d grid
# goal   - a tuple of numbers representing the ending coordinate in the 2d grid
def a_star_search(board, start, direction, goal):
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    queue.put((start[0], start[1], ">"), 0)
    came_from[(start[0], start[1])] = None
    cost_so_far[(start[0], start[1])] = 0

    while not queue.empty():
        x, y, direction = queue.get()
        # print("at", x, y, direction)

        if (x, y) == goal:
            break

        up = (x, y - 1)
        down = (x, y + 1)
        left = (x - 1, y)
        right = (x + 1, y)
        # for each adjacent square
        for x2, y2 in (up, down, left, right):
            newDirection = direction
            if direction == ">":
                if (x2, y2) == right:
                    cost_to_move = 1
                elif (x2, y2) == left:
                    cost_to_move = 2000 + 1
                    newDirection = "<"
                else:
                    cost_to_move = 1000 + 1
                    if (x2, y2) == up:
                        newDirection = "^"
                    else:
                        newDirection = "v"
            elif direction == "<":
                if (x2, y2) == left:
                    cost_to_move = 1
                elif (x2, y2) == right:
                    cost_to_move = 2000 + 1
                    newDirection = ">"
                else:
                    cost_to_move = 1000 + 1
                    if (x2, y2) == up:
                        newDirection = "^"
                    else:
                        newDirection = "v"
            elif direction == "v":
                if (x2, y2) == down:
                    cost_to_move = 1
                elif (x2, y2) == up:
                    cost_to_move = 2000 + 1
                    newDirection = "^"
                else:
                    cost_to_move = 1000 + 1
                    if (x2, y2) == left:
                        newDirection = "<"
                    else:
                        newDirection = ">"
            elif direction == "^":
                if (x2, y2) == up:
                    cost_to_move = 1
                elif (x2, y2) == down:
                    cost_to_move = 2000 + 1
                    newDirection = "v"
                else:
                    cost_to_move = 1000 + 1
                    if (x2, y2) == left:
                        newDirection = "<"
                    else:
                        newDirection = ">"
            # Try to move
            # if (x, y) in cost_so_far:
            #     print(cost_so_far.get((x, y), direction))
            new_cost = cost_so_far[(x, y)] + cost_to_move
            # if we're not out of bounds
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                next_spot = (x2, y2)
                if board[y2][x2] != "#":
                    if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                        cost_so_far[next_spot] = new_cost
                        priority = new_cost + heuristic(goal, x2, y2)
                        queue.put((next_spot[0], next_spot[1], newDirection), priority)
                        # print("adding", next_spot[0], next_spot[1], newDirection)
                        came_from[next_spot] = (x, y)
    return came_from, cost_so_far

def print_path(grid, w, h, path):
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if (i, j) in path:
                print("X", end="")
            else:
                print(item, end="")
        print()
    print()


def part1():
    grid = parseInput(16)

    h = len(grid)
    w = len(grid[0])
    start = None
    end = None
    direction = ">"
    # find start and end
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if item == "S":
                start = (i, j)
            elif item == "E":
                end = (i, j)

    came_from, cost_so_far = a_star_search(grid, start, direction, end)
    # print(came_from)
    # print(cost_so_far)
    # print(cost_so_far[end])
    # reconstruct path
    curr = end
    path = []
    while curr is not None:
        curr = came_from[curr]
        path.append(curr)
    # print(path)
    # print_path(grid, w, h, path)
    print(cost_so_far[end])
    return cost_so_far[end], start, end

'''
#########
#......E#
#.#####.#
#S......#
#########
'''

# Adapted from https://stackoverflow.com/questions/60847450/path-finding-in-2d-map-with-python
def find_paths_util(board, w, h, curr, direction, goal, visited, best_cost, path, cost_so_far, paths):
    # print("at", curr)
    x, y = curr
    # if at the end, return something
    if curr == goal:
        if cost_so_far == best_cost:
            paths.append((path[:], cost_so_far))  # append copy of current path
            print("Made it to end, paths so far", len(paths))
        return

    if cost_so_far > best_cost:
        return

    # mark current cell as visited, keep track of cost_so_far
    visited[y][x] = True

    # if valid cell
    # if y < 0 or y >= h or x < 0 or x >= w or board[y][x] == "#":?
        # Use bfs on path in all valid directions

    # try moving to all 4 points... each one is a new path
    up = (x, y - 1)
    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)
    for x2, y2 in (up, down, left, right):
        newDirection = direction
        cost_to_move = 1
        if direction == ">":
            if (x2, y2) == right:
                cost_to_move = 1
            elif (x2, y2) == left:
                cost_to_move = 2000 + 1
                newDirection = "<"
            else:
                cost_to_move = 1000 + 1
                if (x2, y2) == up:
                    newDirection = "^"
                else:
                    newDirection = "v"
        elif direction == "<":
            if (x2, y2) == left:
                cost_to_move = 1
            elif (x2, y2) == right:
                cost_to_move = 2000 + 1
                newDirection = ">"
            else:
                cost_to_move = 1000 + 1
                if (x2, y2) == up:
                    newDirection = "^"
                else:
                    newDirection = "v"
        elif direction == "v":
            if (x2, y2) == down:
                cost_to_move = 1
            elif (x2, y2) == up:
                cost_to_move = 2000 + 1
                newDirection = "^"
            else:
                cost_to_move = 1000 + 1
                if (x2, y2) == left:
                    newDirection = "<"
                else:
                    newDirection = ">"
        elif direction == "^":
            if (x2, y2) == up:
                cost_to_move = 1
            elif (x2, y2) == down:
                cost_to_move = 2000 + 1
                newDirection = "v"
            else:
                cost_to_move = 1000 + 1
                if (x2, y2) == left:
                    newDirection = "<"
                else:
                    newDirection = ">"

        # don't proceed if out of bounds or wall, or visited
        if y2 < 0 or y2 >= h or x2 < 0 or x2 >= w or board[y2][x2] == "#" or visited[y2][x2] == True:
            continue

        path.append((x2, y2))
        find_paths_util(board, w, h, (x2, y2), newDirection, goal, visited, best_cost, path, cost_so_far + cost_to_move, paths)
        path.pop()

    # Unmark current cell as visited
    visited[y][x] = False

    return paths




def part2():
    grid = parseInput(16)

    h = len(grid)
    w = len(grid[0])

    best_cost, start, end = part1()
    print(best_cost)

    # now find all possible paths that match this cost
    visited = [[False] * w for _ in range(h)]

    path = [start]
    paths = []
    paths = find_paths_util(grid, w, h, start, ">", end, visited, best_cost, path, 0, paths)

    print(paths)
    print("num_paths", len(paths))

    points = set()
    for path, cost in paths:
        for point in path:
            points.add(point)
    print("num_points", len(points))




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
