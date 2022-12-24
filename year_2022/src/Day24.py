import heapq
import sys
import time

class Blizzard:
    def __init__(self, coord, char):
        self.coord = coord # (i, j)
        self.char = char # e.g. ^, v, >, <

    def __repr__(self):
        return str(self.coord) + " : " + self.char

    def overlap(self, other):
        return self.coord == other.coord

    def move(self, w, h):
        if self.char == "<":
            next_coord = (self.coord[0] -1, self.coord[1])
            if next_coord[0] == 0:
                next_coord = (w - 2, self.coord[1])
        elif self.char == ">":
            next_coord = (self.coord[0] + 1, self.coord[1])
            if next_coord[0] == w - 1:
                next_coord = (1, self.coord[1])
        elif self.char == "^":
            next_coord = (self.coord[0], self.coord[1] - 1)
            if next_coord[1] == 0:
                next_coord = (self.coord[0], h - 2)
        elif self.char == "v":
            next_coord = (self.coord[0], self.coord[1] + 1)
            if next_coord[1] == h - 1:
                next_coord = (self.coord[0], 1)
        self.coord = next_coord

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        grid = []
        blizzards = []
        walls = set()
        h = len(lines)
        w = len(lines[0])
        for j in range(h):
            row = []
            for i in range(w):
                coord = (i, j)
                char = lines[j][i]
                row.append(char)
                if char == "#":
                    walls.add(coord)
                elif char != ".":
                    blizzards.append(Blizzard(coord, char))
            grid.append(row)

        # same for sample and actual input
        start = (1, 0)
        end = (w-2, h-1)
        return w, h, blizzards, walls, start, end

def print_grid(w, h, blizzards, walls):
    for j in range(h):
        for i in range(w):
            if (i, j) in walls:
                print("#", end="")
                continue
            printed_blizzard = False
            for b in blizzards:
                if (i, j) == b.coord:
                    print(b.char, end="")
                    printed_blizzard = True
                    break
            if not printed_blizzard:
                print(".", end="")
        print()
    print()


# A custom priority queue used for A Star Search below
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        if (priority, item) not in self.elements:
            heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def __repr__(self):
        return str(self.elements)

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
def a_star_search(w, h, walls, blizzards, start, goal):
    # init
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    queue.put((start[0], start[1], 0), 0)
    came_from[(start[0], start[1], 0)] = None # coord and minutes waited there
    cost_so_far[(start[0], start[1], 0)] = 0

    while not queue.empty():
        x, y, minutes_waited = queue.get()

        if (x, y) == goal:
            break

        # move each blizzard
        blizzard_coords = []
        for b in blizzards:
            b.move(w, h)
            blizzard_coords.append(b.coord)

        # move our spot
        can_move = False
        cost_to_move = 0 # this increments the minute we're on
        new_cost = cost_so_far[(x, y, minutes_waited)] + cost_to_move
        # for each adjacent square
        for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
            next_spot = (x2, y2)
            # if we're in bounds
            if 0 <= x2 < w and 0 <= y2 < h:
                # if we're not hitting a wall or blizzard
                if next_spot not in walls and next_spot not in blizzard_coords:
                    if next_spot not in cost_so_far or new_cost < cost_so_far[(x2, y2, minutes_waited)]:
                        cost_so_far[(x2, y2, minutes_waited)] = new_cost
                        priority = new_cost + heuristic(goal, x2, y2)
                        queue.put((x2, y2, minutes_waited), priority)
                        came_from[(x2, y2, minutes_waited)] = (x, y)
        # TODO: add the option of waiting
        if (x, y) not in blizzard_coords:
            print("adding option to wait at ", x,y)
            cost_so_far[(x, y, minutes_waited+1)] = new_cost + 1
            priority = new_cost + 1 + heuristic(goal, x, y)
            queue.put((x, y, minutes_waited+1), priority)

        print(queue)
    return came_from, cost_so_far

def part1():
    w, h, blizzards, walls, start, end = parseInput(24)
    print_grid(w, h, blizzards, walls)

    # print(blizzards)
    # print(walls)
    print("start", start, "end", end)

    cap = (w + h) * 2

    minute = 0
    spots = PriorityQueue() # use a queue to prioritize the path we take
    spots.put(start, 0) # keep track of (x, y), as if we were simultaneously in each spot
    while True:
        # print(spots)
        # move all the blizzards
        blizzard_coords = []
        for b in blizzards:
            b.move(w, h)
            blizzard_coords.append(b.coord)

        # move our location(s)
        next_spots = PriorityQueue()
        while not spots.empty():
            (x, y) = spots.get()
            # get all adjacent open spots
            for x2, y2 in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
                next_spot = (x2, y2)
                # if we're in bounds
                if 0 <= x2 < w and 0 <= y2 < h:
                    # if we're not hitting a wall or blizzard
                    if next_spot not in walls and next_spot not in blizzard_coords:
                        cost = minute + heuristic(end, x2, y2)
                        # if cost < cap:
                        next_spots.put(next_spot, cost)
                        # if any spot is the end goal, return minutes_elapsed
                        if next_spot == end:
                            print("made it to the end! in ", minute+1, "Minutes")
                            return
            # add waiting at the current spot as an option, if it's open
            if (x, y) not in blizzard_coords:
                cost = minute + heuristic(end, x, y)
                next_spots.put((x, y), cost)
        spots = next_spots
        print(spots)

        minute += 1



def part2():
    lines = parseInput(24)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start_time = time.perf_counter()
    part1()
    end_time = time.perf_counter()
    print("Time (ms):", (end_time - start_time) * 1000)

    # print("\nPART 2 RESULT")
    # start_time = time.perf_counter()
    # part2()
    # end_time = time.perf_counter()
    # print("Time (ms):", (end_time - start_time) * 1000)
