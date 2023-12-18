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

def heuristic(goal, next):
    (x1, y1) = goal
    (x2, y2) = next
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

# move a max of 3 moves in one direction
def getNextMoves(x, y, direction, steps_in_current_direction):
    nextMoves = []
    if direction == 0:  # up
        if steps_in_current_direction < 3:
            # go up and straight
            nextMoves.append((x, y - 1, 0, steps_in_current_direction + 1))
        # turn left, go left
        nextMoves.append((x - 1, y, 3, 1))
        # turn right, go right
        nextMoves.append((x + 1, y, 1, 1))
    elif direction == 1:  # right
        if steps_in_current_direction < 3:
            # go right and straight
            nextMoves.append((x + 1, y, 1, steps_in_current_direction + 1))
        # turn left, go up
        nextMoves.append((x, y - 1, 0, 1))
        # turn right, go down
        nextMoves.append((x, y + 1, 2, 1))
    elif direction == 2:  # down
        if steps_in_current_direction < 3:
            # go down and straight
            nextMoves.append((x, y + 1, 2, steps_in_current_direction + 1))
        # turn left, go right
        nextMoves.append((x + 1, y, 1, 1))
        # turn right, go left
        nextMoves.append((x - 1, y, 3, 1))
    elif direction == 3:  # left
        if steps_in_current_direction < 3:
            # go left and straight
            nextMoves.append((x - 1, y, 3, steps_in_current_direction + 1))
        # turn left, go down
        nextMoves.append((x, y + 1, 2, 1))
        # turn right, go up
        nextMoves.append((x, y - 1, 0, 1))
    else:
        # go down
        nextMoves.append((x, y + 1, 2, 1))
        # go right
        nextMoves.append((x + 1, y, 1, 1))

    return nextMoves

# move at least 4 in one direction, max 10
def getNextMoves2(x, y, direction, steps_in_current_direction):
    nextMoves = []
    if direction == 0:  # up
        if steps_in_current_direction < 4:  # jump ahead
            nextMoves.append((x, y - 1, direction, steps_in_current_direction + 1))
        else:
            if steps_in_current_direction < 10:
                # go up and straight
                nextMoves.append((x, y - 1, 0, steps_in_current_direction + 1))
            # turn left, go left
            nextMoves.append((x - 1, y, 3, 1))
            # turn right, go right
            nextMoves.append((x + 1, y, 1, 1))
    elif direction == 1:  # right
        if steps_in_current_direction < 4:  # jump ahead
            nextMoves.append((x + 1, y, direction, steps_in_current_direction + 1))
        else:
            if steps_in_current_direction < 10:
                # go right and straight
                nextMoves.append((x + 1, y, 1, steps_in_current_direction + 1))
            # turn left, go up
            nextMoves.append((x, y - 1, 0, 1))
            # turn right, go down
            nextMoves.append((x, y + 1, 2, 1))
    elif direction == 2:  # down
        if steps_in_current_direction < 4:  # jump ahead
            nextMoves.append((x, y + 1, direction, steps_in_current_direction + 1))
        else:
            if steps_in_current_direction < 10:
                # go down and straight
                nextMoves.append((x, y + 1, 2, steps_in_current_direction + 1))
            # turn left, go right
            nextMoves.append((x + 1, y, 1, 1))
            # turn right, go left
            nextMoves.append((x - 1, y, 3, 1))
    elif direction == 3:  # left
        if steps_in_current_direction < 4:  # jump ahead
            nextMoves.append((x - 1, y, direction, steps_in_current_direction + 1))
        else:
            if steps_in_current_direction < 10:
                # go left and straight
                nextMoves.append((x - 1, y, 3, steps_in_current_direction + 1))
            # turn left, go down
            nextMoves.append((x, y + 1, 2, 1))
            # turn right, go up
            nextMoves.append((x, y - 1, 0, 1))
    else:
        # go down
        nextMoves.append((x, y + 1, 2, 1))
        # go right
        nextMoves.append((x + 1, y, 1, 1))

    return nextMoves

# 0 up
# 1 right
# 2 down
# 3 left

def part1():
    grid, w, h = parseInput(17)
    # print_2d_grid(grid)
    start = (0, 0, None, 0)
    goal = (w-1, h-1)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        _, current = frontier.get()
        x, y, direction, steps = current

        if (x, y) == goal:
            break

        for next in getNextMoves(x, y, direction, steps):
            x2, y2, direction2, steps2 = next
            if 0 <= x2 < w and 0 <= y2 < h:
                new_cost = cost_so_far[current] + grid[y2][x2]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, (x2, y2))
                    frontier.put(next, priority)
                    came_from[next] = current

    # print("came_from", came_from)
    # find the end node, since we won't know how we turned into it
    endNode = None
    for (x, y, direction, steps) in came_from:
        if (x, y) == goal:
            endNode = (x, y, direction, steps)
            break
    # print("end", endNode)

    # reconstruct path for debugging
    # path = []
    # current = endNode
    # while current != start:
    #     path.append(current)
    #     current = came_from[current]
    # path.append(start)  # optional
    # path.reverse()  # optional
    # print("path", path)
    # printPathGrid(grid, path)

    # print(cost_so_far)
    print(cost_so_far[endNode])

def part2():
    grid, w, h = parseInput(17)
    # print_2d_grid(grid)
    start = (0, 0, None, 0)
    goal = (w-1, h-1)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        _, current = frontier.get()
        x, y, direction, steps = current

        if (x, y) == goal:
            break

        for next in getNextMoves2(x, y, direction, steps):
            x2, y2, direction2, steps2 = next
            if 0 <= x2 < w and 0 <= y2 < h:
                new_cost = cost_so_far[current] + grid[y2][x2]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, (x2, y2))
                    frontier.put(next, priority)
                    came_from[next] = current

    # print("came_from", came_from)
    # find the end node, since we won't know how we turned into it
    endNode = None
    for (x, y, direction, steps) in came_from:
        if (x, y) == goal:
            endNode = (x, y, direction, steps)
            break
    # print("end", endNode)

    # reconstruct path for debugging
    # path = []
    # current = endNode
    # while current != start:
    #     path.append(current)
    #     current = came_from[current]
    # path.append(start)
    # path.reverse()
    # print("path", path)
    # printPathGrid(grid, path)

    # print(cost_so_far)
    print(cost_so_far[endNode])

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
