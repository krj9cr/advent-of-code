import time
import heapq

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)
        return lines

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

def a_star_search(pad_dict, start_key, goal_key):
    start = pad_dict[start_key]
    goal = pad_dict[goal_key]
    queue = PriorityQueue()
    came_from = {}  # keeps track of our path to the goal
    cost_so_far = {}  # keeps track of cost to arrive at ((x, y))

    # add start infos
    queue.put((start[0], start[1]), 0)
    came_from[(start[0], start[1])] = (None, None)
    cost_so_far[(start[0], start[1])] = 0

    while not queue.empty():
        x, y = queue.get()

        if (x, y) == goal:
            break

        up = (x, y - 1)
        down = (x, y + 1)
        left = (x - 1, y)
        right = (x + 1, y)
        # for each adjacent square
        for x2, y2 in (up, down, left, right):
            cost_to_move = 1
            new_cost = cost_so_far[(x, y)] + cost_to_move
            if (x2, y2) in pad_dict.values():
                next_spot = (x2, y2)
                if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                    cost_so_far[next_spot] = new_cost
                    priority = new_cost + heuristic(goal, x2, y2)
                    queue.put((next_spot[0], next_spot[1]), priority)
                    direction = ">"
                    if next_spot == up:
                        direction = "^"
                    elif next_spot == down:
                        direction = "v"
                    elif next_spot == left:
                        direction = "<"
                    came_from[next_spot] = ((x, y), direction)
    return came_from, cost_so_far

memo = {}

def find_path(pad_dict, start_key, goal_key):
    if start_key == goal_key:
        return []
    if memo.get((start_key, goal_key)) is not None:
        return memo[(start_key, goal_key)]
    came_from, cost_so_far = a_star_search(pad_dict, start_key, goal_key)
    end = pad_dict[goal_key]

    if cost_so_far[end]:
        curr = end
        path = []
        directions = []
        direction = ""
        while curr is not None:
            path.append(curr)
            if direction != "":
                directions.append(direction)
            curr, direction = came_from[curr]
        # print_2d_grid(grid, path)
        memo[(start_key, goal_key)] = directions
        return directions
    return None, None, None

def print_2d_grid(grid, points=None):
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if points and (i,j) in points:
                print("O", end="")
            else:
                print(item, end="")
        print()
    print()

def get_directions(code, pad):
    directions = []
    for i in range(len(code) - 1):
        c1 = code[i]
        c2 = code[i + 1]
        sub_directions = find_path(pad, c1, c2)
        # print("finding", c1, c2)
        # print(sub_directions)
        directions += sorted(sub_directions) + ["A"]
    # TODO: not sure if we need 'path'
    return directions

numeric_keypad = [
    [ '7',  '8',  '9'],
    [ '4',  '5',  '6'],
    [ '1',  '2',  '3'],
    [-1,  '0', 'A'],
]

directional_keypad = [
    [-1, '^', 'A'],
    ['<', 'v', '>']
]

num_pad = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
           '4': (0, 1), '5': (1, 1), '6': (2, 1),
           '1': (0, 2), '2': (1, 2), '3': (2, 2),
                        '0': (1, 3), 'A': (2, 3)}

dir_pad = {             '^': (1, 0), 'A': (2, 0),
           '<': (0, 1), 'v': (1, 1), '>': (2, 1)}

def part1():
    codes = parseInput(21)
    print(codes)

    # TODO: need to keep track of where robot arms end up after each time
    # initially they start at "A", but after that, it could end up wherever
    # TODO: also sometimes it could be more efficient to do >>^A or ^>>A depending on if ^ or > is closer
    # we can maybe sort weighted be closeness to A, like "<" then "v", then "^" and ">" are the same

    total = 0
    for i in range(len(codes)):
        code = codes[i]
        # prepend A to the first code
        if i == 0:
            print("prepending A")
            code = "A" + code
        print("code", code)
        directions = get_directions(code, num_pad)
        print("numeric pad", ''.join(directions))

        if i == 0:
            print("prepending A")
            directions = ["A"] + directions
        directions2 = get_directions(directions, dir_pad)
        print("direction pad", ''.join(directions2))

        if i == 0:
            print("prepending A")
            directions2 = ["A"] + directions2
        directions3 = get_directions(directions2, dir_pad)
        print("direction pad", ''.join(directions3))

        lengh_of_seq = len(directions3)
        numeric_code = code[:-1]
        if i == 0:
            numeric_code = numeric_code[1:]
        numeric_code = int(numeric_code)
        print(lengh_of_seq, "*", numeric_code)
        print()
        total += lengh_of_seq * numeric_code

    print(total)




def part2():
    lines = parseInput(21)
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
