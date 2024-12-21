import time
import heapq
import itertools

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
    direction = None

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
            next_spot = (x2, y2)
            newDirection = ">"
            if next_spot == up:
                newDirection = "^"
            elif next_spot == down:
                newDirection = "v"
            elif next_spot == left:
                newDirection = "<"
            if newDirection != direction:
                cost_to_move += 3
            new_cost = cost_so_far[(x, y)] + cost_to_move
            if (x2, y2) in pad_dict.values():
                if next_spot not in cost_so_far or new_cost < cost_so_far[next_spot]:
                    cost_so_far[next_spot] = new_cost
                    priority = new_cost + heuristic(goal, x2, y2)
                    queue.put((next_spot[0], next_spot[1]), priority)
                    came_from[next_spot] = ((x, y), newDirection)
                    direction = newDirection
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
    return None

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

arrow_weights = {
    "<": 3,
    "v": 2,
    "^": 1,
    ">": 1
}

def get_directions(code, pad):
    directions = []
    for i in range(len(code) - 1):
        c1 = code[i]
        c2 = code[i + 1]
        sub_directions = []
        if c1 != c2:
            sub_directions = pad[(c1, c2)]
        directions += sub_directions + ["A"]
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

num_pad_directions = {
    ('7', '8'): ['>'], ('8', '7'): ['<'], ('7', '9'): ['>', '>'], ('9', '7'): ['<', '<'], ('7', '4'): ['v'],
    ('4', '7'): ['^'], ('7', '5'): ['v', '>'], ('5', '7'): ['^', '<'],
    ('7', '6'): ['v', '>', '>'], ('6', '7'): ['<', '<', '^'], ('7', '1'): ['v', 'v'], ('1', '7'): ['^', '^'],
    ('7', '2'): ['v', 'v', '>'], ('2', '7'): ['<', '^', '^'], ('7', '3'): ['v', 'v', '>', '>'],
    ('3', '7'): ['<', '<', '^', '^'],
    ('7', '0'): ['>', 'v', 'v', 'v'],
    ('0', '7'): ['^', '^', '^', '<'],
    ('7', 'A'): ['>', '>', 'v', 'v', 'v'],
    ('A', '7'): ['^', '^', '^', '<', '<'],
    ('8', '9'): ['>'], ('9', '8'): ['<'], ('8', '4'): ['<', 'v'], ('4', '8'): ['>', '^'], ('8', '5'): ['v'],
    ('5', '8'): ['^'], ('8', '6'): ['v', '>'], ('6', '8'): ['<', '^'],
    ('8', '1'): ['<', 'v', 'v'], ('1', '8'): ['>', '^', '^'], ('8', '2'): ['v', 'v'], ('2', '8'): ['^', '^'],
    ('8', '3'): ['v', 'v', '>'], ('3', '8'): ['<', '^', '^'], ('8', '0'): ['v', 'v', 'v'],
    ('0', '8'): ['^', '^', '^'], ('8', 'A'): ['v', 'v', 'v', '>'], ('A', '8'): ['<', '^', '^', '^'],
    ('9', '4'): ['<', '<', 'v'], ('4', '9'): ['>', '>', '^'], ('9', '5'): ['<', 'v'],
    ('5', '9'): ['>', '^'], ('9', '6'): ['v'], ('6', '9'): ['^'], ('9', '1'): ['<', '<', 'v', 'v'],
    ('1', '9'): ['>', '>', '^', '^'], ('9', '2'): ['<', 'v', 'v'], ('2', '9'): ['>', '^', '^'],
    ('9', '3'): ['v', 'v'], ('3', '9'): ['^', '^'], ('9', '0'): ['<', 'v', 'v', 'v'],
    ('0', '9'): ['>', '^', '^', '^'], ('9', 'A'): ['v', 'v', 'v'], ('A', '9'): ['^', '^', '^'], ('4', '5'): ['>'],
    ('5', '4'): ['<'], ('4', '6'): ['>', '>'], ('6', '4'): ['<', '<'], ('4', '1'): ['v'], ('1', '4'): ['^'],
    ('4', '2'): ['v', '>'], ('2', '4'): ['^', '<'], ('4', '3'): ['v', '>', '>'], ('3', '4'): ['<', '<', '^'],
    ('4', '0'): ['>', 'v', 'v'], ('0', '4'): ['^', '^', '<'], ('4', 'A'): ['v', 'v', '>', '>'],
    ('A', '4'): ['^', '^', '<', '<'], ('5', '6'): ['>'], ('6', '5'): ['<'], ('5', '1'): ['<', 'v'],
    ('1', '5'): ['>', '^'], ('5', '2'): ['v'], ('2', '5'): ['^'], ('5', '3'): ['v', '>'], ('3', '5'): ['<', '^'],
    ('5', '0'): ['v', 'v'], ('0', '5'): ['^', '^'], ('5', 'A'): ['v', 'v', '>'], ('A', '5'): ['<', '^', '^'],
    ('6', '1'): ['<', '<', 'v'], ('1', '6'): ['>', '>', '^'], ('6', '2'): ['<', 'v'], ('2', '6'): ['>', '^'],
    ('6', '3'): ['v'], ('3', '6'): ['^'], ('6', '0'): ['<', 'v', 'v'], ('0', '6'): ['>', '^', '^'],
    ('6', 'A'): ['v', 'v'], ('A', '6'): ['^', '^'], ('1', '2'): ['>'], ('2', '1'): ['<'], ('1', '3'): ['>', '>'],
    ('3', '1'): ['<', '<'], ('1', '0'): ['>', 'v'], ('0', '1'): ['^', '<'], ('1', 'A'): ['>', '>', 'v'],
    ('A', '1'): ['^', '<', '<'], ('2', '3'): ['>'], ('3', '2'): ['<'], ('2', '0'): ['v'], ('0', '2'): ['^'],
    ('2', 'A'): ['v', '>'], ('A', '2'): ['<', '^'], ('3', '0'): ['<', 'v'], ('0', '3'): ['>', '^'],
    ('3', 'A'): ['v'], ('A', '3'): ['^'], ('0', 'A'): ['>'], ('A', '0'): ['<']
}

dir_pad_directions = {
    ('^', 'A'): ['>'], ('A', '^'): ['<'],
    ('^', '<'): ['<', 'v'],
    ('<', '^'): ['^', '>'],
    ('^', 'v'): ['v'], ('v', '^'): ['^'],
    ('^', '>'): ['v', '>'],
    ('>', '^'): ['<', '^'],
    ('A', '<'): ['v', '<', '<'],
    ('<', 'A'): ['>', '>', '^'],
    ('A', 'v'): ['v', '<'],
    ('v', 'A'): ['>', '^'],
    ('A', '>'): ['v'], ('>', 'A'): ['^'], ('<', 'v'): ['>'], ('v', '<'): ['<'], ('<', '>'): ['>', '>'],
    ('>', '<'): ['<', '<'], ('v', '>'): ['>'], ('>', 'v'): ['<']
}

def part1():
    codes = parseInput(21)
    print(codes)

    # get all combinations and the best path between them
    # num_pad_directions = {}
    # for c1, c2 in itertools.combinations(num_pad.keys(), 2):
    #     print(c1, c2)
    #     path = find_path(num_pad, c1, c2)
    #     path2 = find_path(num_pad, c2, c1)
    #     print(path)
    #     num_pad_directions[(c1, c2)] = path
    #     num_pad_directions[(c2, c1)] = path2
    # print("num_pad_directions", num_pad_directions)


    # TODO: need to keep track of where robot arms end up after each time
    # initially they start at "A", but after that, it could end up wherever... orrr they always end up at A actually?

    total = 0
    for i in range(len(codes)):
        code = codes[i]
        # prepend A to the first code.. actually it always starts and ends at A
        # if i == 0:
        print("prepending A")
        code = "A" + code
        print("code", code)
        directions = get_directions(code, num_pad_directions)
        print("numeric pad", ''.join(directions))

        # if i == 0:
        # print("prepending A")
        directions = ["A"] + directions
        directions2 = get_directions(directions, dir_pad_directions)
        print("direction pad", ''.join(directions2))

        # if i == 0:
        # print("prepending A")
        directions2 = ["A"] + directions2
        directions3 = get_directions(directions2, dir_pad_directions)
        print("direction pad", ''.join(directions3))
        # print("answer", "       <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

        lengh_of_seq = len(directions3)
        numeric_code = code[:-1]
        # if i == 0:
        numeric_code = numeric_code[1:]
        numeric_code = int(numeric_code)
        print(lengh_of_seq, "*", numeric_code)
        print()
        total += lengh_of_seq * numeric_code

    print(total)
    print(memo)

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
