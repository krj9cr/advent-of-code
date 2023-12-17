import copy
import time
import heapq
import sys

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
    for (i, j, direction, _) in path:
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

def heuristic(goal, x2, y2):
    (x1, y1) = goal
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

bestPath = []
bestPathCost = 99999

# Function to find all possible paths in a matrix from the top-left cell to the bottom-right cell
def findPaths(grid, path, starts):
    queue = PriorityQueue()
    global bestPathCost, bestPath
    w = len(grid[0])
    h = len(grid)

    # Include the current cell in the path
    for (i, j, direction, steps_in_curr_direction) in starts:
        path.append((i, j, direction, steps_in_curr_direction))
        cost = grid[j][i]
        queue.put((cost, path, {}), cost)
        print(queue)

    while not queue.empty():
        huer, (cost, path, cost_so_far) = queue.get()
        # print(cost, path)

        curr_pos = path[-1]
        (i, j, direction, steps_in_curr_direction) = curr_pos

        # If the bottom-right cell is reached, print the path
        if i == w - 1 and j == h - 1:
            path.append((i, j, direction, steps_in_curr_direction))
            # printPath(path)
            cost = getPathCost(grid, path)
            if cost < bestPathCost:
                bestPathCost = cost
                bestPath = path
                printPathGrid(grid, path)
                print("BEST COST", bestPathCost)

        # for all possible steps
        for next_pos in getNextMoves(i, j, direction, steps_in_curr_direction):
            (i2, j2, direction2, steps_in_curr_direction2) = next_pos
            if 0 <= i2 < w and 0 <= j2 < h:
                new_cost = cost + grid[j2][i2]
                new_huer = huer + grid[j2][i2] + heuristic((w-1, h-1), i2, j2)
                # if (next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]) and new_cost < bestPathCost:
                if (next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]) and new_cost < bestPathCost:
                    cost_so_far[next_pos] = new_cost
                    queue.put((new_cost, path + [next_pos], cost_so_far), new_huer)

# 0 up
# 1 right
# 2 down
# 3 left
def getNextMoves(x, y, direction, steps_in_current_direction):
    nextMoves = []
    if direction == 0:  # up
        if steps_in_current_direction < 3:
            # go up and straight
            nextMoves.append((x, y - 1, direction, steps_in_current_direction + 1))
        # turn right, go right
        nextMoves.append((x + 1, y, 1, 1))
        # turn left, go left
        nextMoves.append((x - 1, y, 3, 1))
    elif direction == 1:  # right
        if steps_in_current_direction < 3:
            # go right and straight
            nextMoves.append((x + 1, y, direction, steps_in_current_direction + 1))
        # turn right, go down
        nextMoves.append((x, y + 1, 2, 1))
        # turn left, go up
        nextMoves.append((x, y - 1, 0, 1))
    elif direction == 2:  # down
        if steps_in_current_direction < 3:
            # go down and straight
            nextMoves.append((x, y + 1, direction, steps_in_current_direction + 1))
        # turn left, go right
        nextMoves.append((x + 1, y, 1, 1))
        # turn right, go left
        nextMoves.append((x - 1, y, 3, 1))
    elif direction == 3:  # left
        if steps_in_current_direction < 3:
            # go left and straight
            nextMoves.append((x - 1, y, direction, steps_in_current_direction + 1))
        # turn left, go down
        nextMoves.append((x, y + 1, 2, 1))
        # turn right, go up
        nextMoves.append((x, y - 1, 0, 1))
    return nextMoves


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

    # print(sys.getrecursionlimit())
    # sys.setrecursionlimit(10000)

    path = []
    findPaths(grid, path, [(1, 0, 1, 1), (0, 1, 2, 1)])
    print("bestpathcost", bestPathCost)
    print(bestPath)
    print(getPathCost(grid, bestPath))

    # paths = a_star_search(grid, starts, endPos)
    #
    # for (priority, path) in paths:
    #     print((priority, path))
    #     grid2 = copy.deepcopy(grid)
    #     for (i, j, direction, _) in path:
    #         # grid2[j][i] = "#"
    #         if direction == 0:  # up
    #             grid2[j][i] = "^"
    #         elif direction == 1:  # right
    #             grid2[j][i] = ">"
    #         elif direction == 2:  # down
    #             grid2[j][i] = "v"
    #         elif direction == 3:  # left
    #             grid2[j][i] = "<"
    #     print_2d_grid(grid2)
    #     print()

# 857 too high

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
