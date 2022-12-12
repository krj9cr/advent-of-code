import heapq
import time

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


def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        grid = []
        for line in lines:
            row = []
            for c in line:
                row.append(c)
            grid.append(row)
        return grid


# See: https://www.redblobgames.com/pathfinding/a-star/implementation.html
# board  - a 2d array of strings or numbers
# start  - a tuple of numbers representing the starting coordinate in the 2d grid
# goal   - a tuple of numbers representing the ending coordinate in the 2d grid
def a_star_search(board, start, goal):
    # init
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
        current_item = board[y][x]
        # print("current_spot", current_item)

        # for each adjacent square
        for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
            cost_to_move = 1  # note this could vary on implementation
            new_cost = cost_so_far[(x, y)] + cost_to_move
            # if we're not out of bounds
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                next_spot = (x2, y2)
                next_item = board[y2][x2]
                ord_next = ord(next_item)
                # print("checking next_spot", next_spot, ":", next_item)
                if next_item == "E":
                    ord_next = ord("z")
                # check if elevation is appropriate
                if current_item == "S" or ord_next - ord(current_item) <= 1:
                    # print("can move")
                    # check cost
                    if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                        cost_so_far[next_spot] = new_cost
                        priority = new_cost + heuristic(goal, x2, y2)
                        queue.put(next_spot, priority)
                        came_from[next_spot] = (x, y)
                else:
                    # print("cannot move")
                    continue
    return came_from, cost_so_far


def part1():
    grid = parseInput(12)
    print(grid)
    start_coord = None
    end_coord = None
    w = len(grid[0])
    h = len(grid)
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if item == "S":
                start_coord = (i, j)
            elif item == "E":
                end_coord = (i, j)
    print("start", start_coord)
    print("end", end_coord)

    chain = a_star_search(grid, start_coord, end_coord)[0]
    # print(chain)
    path = []
    curr = end_coord
    while True:
        path.append(curr)
        # print(path)
        curr = chain[curr]
        if curr == start_coord:
            path.append(curr)
            break
    path = list(reversed(path))
    print(path)
    print(len(path)-1)



def part2():
    grid = parseInput(12)
    print(grid)
    start_coord = None
    end_coord = None
    w = len(grid[0])
    h = len(grid)
    possible_starts = []
    for j in range(h):
        for i in range(w):
            item = grid[j][i]
            if item == "S":
                start_coord = (i, j)
            elif item == "E":
                end_coord = (i, j)
            elif item == "a":
                possible_starts.append((i, j))
    print("start", start_coord)
    print("end", end_coord)
    print("possible_starts", possible_starts)

    min_dist = 9999999

    for possible_start in possible_starts:
        chain = a_star_search(grid, possible_start, end_coord)[0]
        # print(chain)
        path = []
        curr = end_coord
        is_path = True
        while True:
            path.append(curr)
            # print(path)
            try:
                curr = chain[curr]
            except:
                # no path???
                is_path = False
                break
            if curr == possible_start:
                path.append(curr)
                break
        if is_path:
            path = list(reversed(path))
            print(path)
            print(len(path)-1)
            dist = len(path) - 1
            if dist < min_dist:
                min_dist = dist
        else:
            print("no path from", possible_start)
    print("MIN DIST", min_dist)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start_time = time.perf_counter()
    # part1()
    # end_time = time.perf_counter()
    # print("Time (ms):", (end_time - start_time) * 1000)

    print("\nPART 2 RESULT")
    start_time = time.perf_counter()
    part2()
    end_time = time.perf_counter()
    print("Time (ms):", (end_time - start_time) * 1000)
