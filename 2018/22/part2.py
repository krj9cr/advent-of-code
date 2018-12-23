from collections import deque
import heapq


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


def costToMove(board, nextSpot, currentTool):
    x2, y2 = nextSpot
    # check if our current tool works in the next region
    if checkRegion(board[y2][x2], currentTool):
        return 1
    else:
        return 7


# source: https://www.redblobgames.com/pathfinding/a-star/implementation.html
def dijkstra_search(board, start, goal):
    frontier = PriorityQueue()
    frontier.put((start, 0), 0)
    came_from = {}
    cost_so_far = {}
    tried_tools = {}
    came_from[start] = None
    cost_so_far[start] = 0
    tried_tools[start] = [0]
    tried_tools[goal] = [0]

    while not frontier.empty():
        current, current_tool = frontier.get()
        x, y = current

        if current == goal:
            if current_tool != 0:
                cost_so_far[goal] += 7
            break

        for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                next_spot = (x2, y2)
                # check the tools we've tried for the next spot
                if next_spot not in tried_tools:
                    next_tool = switchTool(board, x2, y2, start, goal, current_tool, [])
                    tried_tools[next_spot] = [next_tool]
                else:
                    if next_spot == start or next_spot == goal:
                        next_tool = 0
                    else:
                        next_tool = switchTool(board, x2, y2, start, goal, current_tool, tried_tools[next_spot])
                        tried_tools[next_spot] = tried_tools[next_spot] + [next_tool]
                # get cost based on whether or not we switch tools
                if current_tool != next_tool:
                    move_cost = 7
                else:
                    move_cost = 1
                # set tool
                # current_tool = next_tool
                new_cost = cost_so_far[current] + move_cost
                if next_spot not in cost_so_far or \
                        new_cost < cost_so_far[next_spot] or\
                        (next_spot != start and next_spot != goal and len(tried_tools[next_spot]) < 2):
                    if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                        cost_so_far[next_spot] = new_cost
                    frontier.put((next_spot, next_tool), new_cost)
                    came_from[next_spot] = (current, current_tool)

    return came_from, cost_so_far


def switchTool(board, x, y, start, end, current_tool, tried_tools):
    if (x, y) == start or (x, y) == end:
        return 0
    region_type = board[y][x]
    if checkRegion(region_type, current_tool):
        return current_tool
    else:
        if region_type == 0:
            if 0 in tried_tools:
                return 1
            else:
                return 0
        elif region_type == 1:
            if 1 in tried_tools:
                return 2
            else:
                return 1
        elif region_type == 2:
            if 2 in tried_tools:
                return 0
            else:
                return 2


def checkRegion(regionType, currentTool):
    # currentTool
    #   0 => torch
    #   1 => climbing gear
    #   2 => neither
    #
    # In rocky regions, you can use the climbing gear or the torch.
    # You cannot use neither (you'll likely slip and fall).
    if regionType == 0:
        if currentTool == 0 or currentTool == 1:
            return True
        else:
            return False
    # In wet regions, you can use the climbing gear or neither tool.
    # You cannot use the torch (if it gets wet, you won't have a light source).
    if regionType == 1:
        if currentTool == 1 or currentTool == 2:
            return True
        else:
            return False
    # In narrow regions, you can use the torch or neither tool.
    # You cannot use the climbing gear (it's too bulky to fit).
    if regionType == 2:
        if currentTool == 0 or currentTool == 2:
            return True
        else:
            return False
    return False


def reconstruct_path(came_from, start, goal):
    current = goal
    current_tool = 0
    path = []
    while current != start:
        path.append((current, current_tool))
        current, current_tool = came_from[current]
    path.append((start, 0))  # optional
    path.reverse()  # optional
    return path

# between 899 and 1051, not 1009, not 1044
def part2(depth: int, targetX: int, targetY: int):
    # init board
    board = initBoard(0, 0, targetX, targetY, depth, 20)
    fillBoard(board, targetX, targetY, depth)
    fillBoardTypes(board)
    printBoard(board)

    # init vars
    start = (0, 0)
    end = (targetX, targetY)

    # run pathfinding
    came_from, time = dijkstra_search(board, start, end)
    # print(time)
    print(time[start], time[end])
    path = reconstruct_path(came_from, start, end)
    print(path)
    total_cost = 0
    current_tool = 0
    for spot, next_tool in path:
        if next_tool != current_tool:
            total_cost += 7
        else:
            total_cost += 1
        current_tool = next_tool
    print("total_cost:", total_cost)
