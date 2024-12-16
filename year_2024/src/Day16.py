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
    # init
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    queue.put((start[0], start[1], ">"), 0)
    came_from[(start[0], start[1])] = None
    cost_so_far[(start[0], start[1])] = 0

    while not queue.empty():
        x, y, direction = queue.get()
        print("at", x, y, direction)

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
                        print("adding", next_spot[0], next_spot[1], newDirection)
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

    print("start", start)
    print("end", end)

    came_from, cost_so_far = a_star_search(grid, start, direction, end)
    print(came_from)
    print(cost_so_far)
    print(cost_so_far[end])
    # reconstruct path
    curr = end
    path = []
    while curr is not None:
        curr = came_from[curr]
        path.append(curr)
    print(path)
    print_path(grid, w, h, path)
    print(cost_so_far[end])

'''
#########
#......E#
#.......#
#S......#
#########
'''

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
