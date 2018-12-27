import heapq

#   0 => torch
#   1 => climbing gear
#   2 => neither
# In rocky regions, you can use the climbing gear or the torch.
# You cannot use neither (you'll likely slip and fall).
rocky_tools = {0, 1}
# In wet regions, you can use the climbing gear or neither tool.
# You cannot use the torch (if it gets wet, you won't have a light source).
wet_tools = {1, 2}
# In narrow regions, you can use the torch or neither tool.
# You cannot use the climbing gear (it's too bulky to fit).
narrow_tools = {0, 2}

#   0 => rocky
#   1 => wet
#   2 => narrow
allowed_tools = {0: rocky_tools, 1: wet_tools, 2: narrow_tools}


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def geologicalIndex(board, x: int, y: int, targetX: int, targetY: int):
    if x == 0 and y == 0:
        return 0
    elif x == targetX and y == targetY:
        return 0
    else:
        if y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        else:
            return board[y][x-1] * board[y-1][x]


def geologicalIndexEdges(x: int, y: int, targetX: int, targetY: int):
    if x == 0 and y == 0:
        return 0
    elif x == targetX and y == targetY:
        return 0
    else:
        if y == 0:
            return x * 16807
        elif x == 0:
            return y * 48271
        else:
            return 0


def erosionLevelEdges(x: int, y:int, targetX: int, targetY: int, depth: int):
    return (geologicalIndexEdges(x, y, targetX, targetY) + depth) % 20183


def erosionLevel(board, x: int, y:int, targetX: int, targetY: int, depth: int):
    return (geologicalIndex(board, x, y, targetX, targetY) + depth) % 20183


def fillBoardTypes(board):
    for y in range(0, len(board)):
        row = board[y]
        for x in range(0, len(row)):
            board[y][x] = board[y][x] % 3


def fillBoard(board, targetX: int, targetY: int, depth: int):
    for y in range(1, len(board)):
        row = board[y]
        for x in range(1, len(row)):
            board[y][x] = erosionLevel(board, x, y, targetX, targetY, depth)


def printBoard(board):
    for row in board:
        for item in row:
            regionType = item % 3
            if regionType == 0:
                print(".", end="")
            elif regionType == 1:
                print("=", end ="")
            elif regionType == 2:
                print("|", end="")
            else:
                print("?", end="")
        print("")


def initBoard(startX: int, startY: int, targetX: int, targetY: int, depth: int, padding: int):
    board = []
    for j in range(startY, targetY+1+padding):
        row = []
        for i in range(startX, targetX+1+padding):
            if i == 0 or j == 0:
                row.append(erosionLevelEdges(i, j, targetX, targetY, depth))
            else:
                row.append(0)
        board.append(row)
    return board


# guesses the cost of going from current position to goal
# should always underestimate the actual cost
def heuristic(goal, x2, y2, current_tool):
    (x1, y1) = goal
    dist = abs(x1 - x2) + abs(y1 - y2)
    # if current tool is different than torch, we will have to change it at least once
    if current_tool != 0:
        dist += 7
    return dist


def a_star_search(board, start, goal):
    # init
    queue = PriorityQueue()
    current_tool = 0
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y), tool)

    # add start infos
    queue.put((start[0], start[1], current_tool), 0)
    came_from[(start[0], start[1], 0)] = None
    cost_so_far[(start[0], start[1], 0)] = 0

    while not queue.empty():
        x, y, current_tool = queue.get()

        if (x, y) == goal:
            break

        # for each adjacent square
        for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                next_spot = (x2, y2)
                tool_set = allowed_tools[board[y2][x2]]
                if next_spot == goal or next_spot == start:
                    tool_set = {0}
                # we can only switch tools if BOTH current and next spots allow it?!!!!!??!?!?
                tool_set = tool_set.intersection(allowed_tools[board[y][x]])
                # for each allowed tool at that spot
                for allowed_tool in tool_set:
                    cost_to_move = 1
                    if allowed_tool != current_tool:
                        cost_to_move += 7
                    new_cost = cost_so_far[(x, y, current_tool)] + cost_to_move
                    if (x2, y2, allowed_tool) not in cost_so_far or\
                            new_cost < cost_so_far[(x2, y2, allowed_tool)]:
                        cost_so_far[(x2, y2, allowed_tool)] = new_cost
                        priority = new_cost + heuristic(goal, x2, y2, allowed_tool)
                        queue.put((x2, y2, allowed_tool), priority)
                        came_from[(x2, y2, allowed_tool)] = (x, y, current_tool)

    return came_from, cost_so_far


def reconstruct_path_with_tool(came_from, start, goal):
    x, y = goal
    current_tool = 0
    path = []
    while (x, y) != start:
        path.append((x, y, current_tool))
        x, y, current_tool = came_from[(x, y, current_tool)]
    path.append((start[0], start[1], 0))  # optional
    path.reverse()  # optional
    return path


def part2(depth: int, targetX: int, targetY: int):
    # init board
    # note padding here because we can travel BEYOND the rectangle between the start/end points
    board = initBoard(0, 0, targetX, targetY, depth, 100)
    fillBoard(board, targetX, targetY, depth)
    fillBoardTypes(board)
    # printBoard(board)

    # init vars
    start = (0, 0)
    end = (targetX, targetY)

    # run pathfinding
    came_from, cost_so_far = a_star_search(board, start, end)
    print("end cost:", cost_so_far[(targetX, targetY, 0)])
    path = reconstruct_path_with_tool(came_from, start, end)
    # print(path)
    total_cost = -1  # accounts for +1 for just starting at start
    current_tool = 0
    for x, y, next_tool in path:
        total_cost += 1
        if next_tool != current_tool:
            total_cost += 7
        current_tool = next_tool
    print("total_cost:", total_cost)
