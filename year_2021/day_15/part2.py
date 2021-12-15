
import heapq
import sys

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("part2.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return [int(c) for c in line.strip()]

# guesses the cost of going from current position to goal
# should always underestimate the actual cost
def heuristic(goal, x2, y2):
    (x1, y1) = goal
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist


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

        # for each adjacent square
        for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
            # if we're not out of bounds
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]):
                cost_to_move = board[y2][x2]  # note this could vary on implementation
                new_cost = cost_so_far[(x, y)] + cost_to_move
                next_spot = (x2, y2)
                if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                    cost_so_far[next_spot] = new_cost
                    priority = new_cost + heuristic(goal, x2, y2)
                    queue.put(next_spot, priority)
                    came_from[next_spot] = (x, y)
    return came_from, cost_so_far


def part2(board):

    w = len(board[0])
    h = len(board)

    multiplier = 4
    # expand board for part2 horizontally
    bigBoard = []
    for row in board:
      newRow = row[:]
      for s in range(1, multiplier+1):
        for i in range(0, w):
          item = row[i]
          newItem = item + s

          print("item: ", item, "  new item: ", newItem)
          if newItem > 9:
            newItem = newItem - 9
          newRow.append(newItem)
      bigBoard.append(newRow)

    # expand board vertically
    board = bigBoard
    newRows = []

    for s in range(1, multiplier+1):
      for row in board:
        newRow = []
        for i in range(0, len(board[0])):
          item = row[i]
          newItem = item + s
#           print("item: ", item, "  new item: ", newItem)
          if newItem > 9:
            newItem = newItem - 9
          newRow.append(newItem)
        newRows.append(newRow)

    board += newRows

    # init vars
    start = (0, 0)
    targetX = len(board)-1
    targetY = len(board[0])-1
    end = (targetX, targetY)

    # run pathfinding
    came_from, cost_so_far = a_star_search(board, start, end)
#     print("came from: ", came_from)
    print("end cost:", cost_so_far[(targetX, targetY)])

def runpart2():
    part2(parseInputFile())

if __name__ == '__main__':

    print("\nPART 2 RESULT")
    runpart2()
