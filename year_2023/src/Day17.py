import copy
import time
import heapq
import sys
import queue

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

# A custom priority queue
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def __str__(self):
        return str(self.elements)

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    # returns (priority, item)
    def get(self):
        return heapq.heappop(self.elements)

def print_2d_grid(grid):
    for row in grid:
        for item in row:
            print(item, end="")
        print()

# Function to print the path taken to reach destination
def printPath(path):
    for i in path:
        print(i, end=", ")
    print()

def printPathGrid(grid, path):
    grid2 = copy.deepcopy(grid)
    for (i, j, direction) in path:
        if direction == 0:  # up
            grid2[j][i] = "^"
        elif direction == 1:  # right
            grid2[j][i] = ">"
        elif direction == 2:  # down
            grid2[j][i] = "v"
        elif direction == 3:  # left
            grid2[j][i] = "<"
    print_2d_grid(grid2)
    print()

def getPathCost(grid, path):
    cost = 0
    # print(path)
    for (i, j, direction, _) in path:
        cost += grid[j][i]
    return cost

def heuristic(goal, next):
    (x1, y1) = goal
    (x2, y2) = next
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

def get_neighbors(grid, node):
    x, y, direction = node
    w = len(grid[0])
    h = len(grid)
    neighbors = []
    if direction == 0:
        # same direction
        # next_cost = 0
        # for i in range(1, 3):
        #     x2, y2 = (x, y - i)
        #     if 0 <= x2 < w and 0 <= y2 < h:
        #         next_cost += grid[y2][x2]
        #         neighbors.append((x2, y2, direction, next_cost))
        # go left
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x - i, y
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 3, next_cost))
        # go right
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x + i, y
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 1, next_cost))
    elif direction == 1:  # right
        # same direction
        # next_cost = 0
        # for i in range(1, 3):
        #     x2, y2 = (x + i, y)
        #     if 0 <= x2 < w and 0 <= y2 < h:
        #         next_cost += grid[y2][x2]
        #         neighbors.append((x2, y2, direction, next_cost))
        # go left, which is up
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x, y - i
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 0, next_cost))
        # go right, which is down
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x, y + i
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 2, next_cost))
    elif direction == 2:  # down
        # same direction
        # next_cost = 0
        # for i in range(1, 3):
        #     x2, y2 = (x, y + i)
        #     if 0 <= x2 < w and 0 <= y2 < h:
        #         next_cost += grid[y2][x2]
        #         neighbors.append((x2, y2, direction, next_cost))
        # go left
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x - i, y
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 3, next_cost))
        # go right
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x + i, y
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 1, next_cost))
    elif direction == 3:  # left
        # same direction
        # next_cost = 0
        # for i in range(1, 3):
        #     x2, y2 = (x - i, y)
        #     if 0 <= x2 < w and 0 <= y2 < h:
        #         next_cost += grid[y2][x2]
        #         neighbors.append((x2, y2, direction, next_cost))
        # go right, which is up
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x, y - i
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 0, next_cost))
        # go left, which is down
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x, y + i
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 2, next_cost))
    else:  # direction is None, so we're at the start, so just go down and right
        # go down
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x, y + i
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 2, next_cost))
        # go right
        next_cost = 0
        for i in range(1, 4):
            x2, y2 = x + i, y
            if 0 <= x2 < w and 0 <= y2 < h:
                next_cost += grid[y2][x2]
                neighbors.append((x2, y2, 1, next_cost))
    # x, y, direction, next_cost
    return neighbors

# 0 up
# 1 right
# 2 down
# 3 left

# TODO: this gets the example wrong but my input right :)
def part1():
    grid, w, h = parseInput(17)
    # print_2d_grid(grid)
    start = (0, 0, None)
    goal = (w-1, h-1)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        _, current = frontier.get()
        x, y, direction = current

        if (x, y) == goal:
            break

        for next in get_neighbors(grid, current):
            x2, y2, direction2, cost2 = next
            if 0 <= x2 < w and 0 <= y2 < h:
                new_cost = cost_so_far[current] + cost2
                if (x2, y2, direction2) not in cost_so_far or new_cost < cost_so_far[(x2, y2, direction2)]:
                    cost_so_far[(x2, y2, direction2)] = new_cost
                    priority = new_cost + heuristic(goal, (x2, y2))
                    frontier.put((x2, y2, direction2), priority)
                    came_from[(x2, y2, direction2)] = current

    print("came_from", came_from)
    endNode = None
    for (x, y, direction) in came_from:
        if (x, y) == goal:
            endNode = (x, y, direction)
            break
    print("end", endNode)

    path = []
    current = endNode
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)  # optional
    path.reverse()  # optional
    print("path", path)

    printPathGrid(grid, path)
    print(cost_so_far)
    print(cost_so_far[endNode])

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
