import heapq
from collections import deque

# grid    - a 2d array of strings or numbers
# start   - a tuple of numbers representing the starting coordinate in the 2d grid
# end     - a tuple of numbers representing the ending coordinate in the 2d grid
# include - characters allowed to traverse, e.g. "."
# exclude - characters not allowed to traverse, e.g. "#"
def bfs_2d_grid(grid, start, end, include="", exclude=""):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                next = (x2, y2)
                nextItem = grid[y2][x2]
                if next not in seen and \
                        (include == "" or nextItem in include) and \
                        (exclude == "" or nextItem not in exclude):
                    queue.append(path + [next])
                    seen.add(next)

# map     - a dict of coordinate tuples to values in the map, for example:
#           { (2,2): "#", (2,1): "." }
#           this allows for better storage of sparse maps, or only storing open or known coordinates
# start   - a tuple of numbers representing the starting coordinate
# end     - a tuple of numbers representing the ending coordinate
# include - characters allowed to traverse, e.g. "."
# exclude - characters not allowed to traverse, e.g. "#"
def bfs_2d_map(map, start, end, include="", exclude=""):
    queue = deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == end:
            return path
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            next = (x2, y2)
            nextItem = map[(x2, y2)]
            if next not in seen and \
                    (include == "" or nextItem in include) and \
                    (exclude == "" or nextItem not in exclude):
                queue.append(path + [next])
                seen.add(next)

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
def a_star_search(board, start, goal):
    # init
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    queue.put((start[0], start[1]), 0)
    came_from[(start[0], start[1], 0)] = None
    cost_so_far[(start[0], start[1], 0)] = 0

    while not queue.empty():
        x, y = queue.get()

        if (x, y) == goal:
            break

        # for each adjacent square
        for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
            cost_to_move = 1  # note this could vary on implementation
            new_cost = cost_so_far[(x, y)] + cost_to_move
            # if we're not out of bounds
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                next_spot = (x2, y2)
                if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                    cost_so_far[next_spot] = new_cost
                    priority = new_cost + heuristic(goal, x2, y2)
                    queue.put(next_spot, priority)
                    came_from[next_spot] = (x, y)
    return came_from, cost_so_far
