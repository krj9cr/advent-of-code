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
            row = [int(i) for i in line]
            grid.append(row)
        return grid, len(grid[0]), len(grid)

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
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

# 0 up
# 1 right
# 2 down
# 3 left
def getNextMoves(x, y, direction, steps_in_current_direction):
    nextMoves = []
    if direction == 0:  # up
        if steps_in_current_direction <= 3:
            # go up and straight
            nextMoves.append((x, y - 1, 0, steps_in_current_direction + 1))
        # turn left, go left
        nextMoves.append((x - 1, y, 3, steps_in_current_direction))
        # turn right, go right
        nextMoves.append((x + 1, y, 1, steps_in_current_direction))
    elif direction == 1:  # right
        if steps_in_current_direction <= 3:
            # go right and straight
            nextMoves.append((x + 1, y, 1, steps_in_current_direction + 1))
        # turn left, go up
        nextMoves.append((x, y - 1, 0, steps_in_current_direction))
        # turn right, go down
        nextMoves.append((x, y + 1, 2, steps_in_current_direction))
    elif direction == 2:  # down
        if steps_in_current_direction <= 3:
            # go down and straight
            nextMoves.append((x, y + 1, 2, steps_in_current_direction + 1))
        # turn left, go right
        nextMoves.append((x + 1, y, 1, steps_in_current_direction))
        # turn right, go left
        nextMoves.append((x - 1, y, 3, steps_in_current_direction))
    elif direction == 3:  # left
        if steps_in_current_direction <= 3:
            # go left and straight
            nextMoves.append((x - 1, y, 3, steps_in_current_direction + 1))
        # turn left, go down
        nextMoves.append((x, y + 1, 2, steps_in_current_direction))
        # turn right, go up
        nextMoves.append((x, y - 1, 0, steps_in_current_direction))
    return nextMoves

# See: https://www.redblobgames.com/pathfinding/a-star/implementation.html
# board  - a 2d array of strings or numbers
# start  - a tuple of numbers representing the starting coordinate in the 2d grid
# goal   - a tuple of numbers representing the ending coordinate in the 2d grid
def a_star_search(board, starts, goal):
    # init
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    for (x, y, direction, steps_in_curr_direction) in starts:
        queue.put((x, y, direction, steps_in_curr_direction), board[y][x])
        came_from[(x, y)] = None
        cost_so_far[(x, y)] = board[y][x]

    while not queue.empty():
        x, y, direction, steps_in_current_direction = queue.get()

        if (x, y) == goal:
            break

        # for each next valid move (only straight, left, right, not backwards) and max 3 steps in one direction
        for x2, y2, direction2, steps_in_current_direction2 in getNextMoves(x, y, direction, steps_in_current_direction):
            # if we're not out of bounds
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                cost_to_move = board[y2][x2]  # cost to move is the number value in the board
                new_cost = cost_so_far[(x, y)] + cost_to_move
                next_spot = (x2, y2, direction2, steps_in_current_direction2)
                if (x2, y2) not in cost_so_far or new_cost < cost_so_far[(x2, y2)]:
                    cost_so_far[(x2, y2)] = new_cost
                    priority = new_cost #+ heuristic(goal, x2, y2)
                    queue.put(next_spot, priority)
                    came_from[(x2, y2)] = (x, y)
    # return the end pos, too, because it'll have a direction and steps
    return came_from, cost_so_far, (x, y, direction, steps_in_current_direction)

# 0 up
# 1 right
# 2 down
# 3 left

def part1():
    grid, w, h = parseInput(17)
    # print_2d_grid(grid)
    # print(w, h)
    starts = [(1, 0, 1, 1), (0, 1, 2, 1)]
    endPos = (w - 1, h - 1)

    came_from, cost_so_far, _ = a_star_search(grid, starts, endPos)
    print(came_from)

    # reconstruct path
    path = []
    curr = came_from[endPos]
    while curr is not None:
        print(curr)
        path.append(curr)
        curr = came_from[curr]
    print(list(reversed(path)))

    grid2 = copy.deepcopy(grid)
    for (i, j) in path:
        grid2[j][i] = "#"
        # if direction == 0:  # up
        #     grid2[j][i] = "^"
        # elif direction == 1:  # right
        #     grid2[j][i] = ">"
        # elif direction == 2:  # down
        #     grid2[j][i] = "v"
        # elif direction == 3:  # left
        #     grid2[j][i] = "<"
    print_2d_grid(grid2)
    print(cost_so_far[endPos])


def part2():
    lines = parseInput(17)
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
