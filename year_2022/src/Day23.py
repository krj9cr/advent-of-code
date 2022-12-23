import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        coords = []
        # get the coordinates of each #
        for j in range(len(lines)):
            row = lines[j]
            for i in range(len(row)):
                char = row[i]
                if char == '#':
                    coords.append((i, j))
        return coords

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

def get_neighbors(coord, direction=None):
    neighbors = []
    if direction is None: # get all neighbors
        for x, y in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            neighbors.append(tuple([coord[0] + x, coord[1] + y]))
    else:
        if direction == NORTH:
            for x, y in [(-1, -1), (0, -1), (1, -1)]:
                neighbors.append(tuple([coord[0]+x, coord[1]+y]))
        elif direction == EAST:
            for x, y in [(1, -1), (1, 0), (1, 1)]:
                neighbors.append(tuple([coord[0]+x, coord[1]+y]))
        elif direction == SOUTH:
            for x, y in [(-1, 1), (0, 1), (1, 1)]:
                neighbors.append(tuple([coord[0]+x, coord[1]+y]))
        elif direction == WEST:
            for x, y in [(-1, -1), (-1, 0), (-1, 1)]:
                neighbors.append(tuple([coord[0]+x, coord[1]+y]))
    return neighbors

def has_neighbors(elves, elf, direction=None):
    for neighbor in get_neighbors(elf, direction):
        if neighbor in elves:
            return True
    return False

def move_direction(elf, direction):
    if direction == NORTH:
        return elf[0], elf[1] - 1
    elif direction == EAST:
        return elf[0] + 1, elf[1]
    elif direction == SOUTH:
        return elf[0], elf[1] + 1
    elif direction == WEST:
        return elf[0] - 1, elf[1]

def find_size(elves):
    min_x = min_y = 99999
    max_x = max_y = -99999
    for elf in elves:
        min_x = min(min_x, elf[0])
        min_y = min(min_y, elf[1])
        max_x = max(max_x, elf[0])
        max_y = max(max_y, elf[1])
    return min_x, max_x, min_y, max_y

def draw_elves(elves):
    min_x, max_x, min_y, max_y = find_size(elves)
    for j in range(min_y, max_y+1):
        for i in range(min_x, max_x+1):
            if (i, j) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1():
    elves = set(parseInput(23))
    print(elves)
    num_elves = len(elves)

    rounds = 10

    # NORTH = 0
    # EAST = 1
    # SOUTH = 2
    # WEST = 3
    direction_order = [NORTH, SOUTH, WEST, EAST]

    for r in range(rounds):
        print("\nround ", r)
        # print(direction_order)
        # draw_elves(elves)
        next_elves = {}
        # During the first half of each round, each Elf considers the eight positions adjacent to themself.
        for elf in elves:
            # Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step
            # in the first valid direction:
            if has_neighbors(elves, elf, direction=None):
                can_move = False
                for direction in direction_order:
                    if not has_neighbors(elves, elf, direction=direction):
                        next_elf = move_direction(elf, direction)
                        # print("elf", elf, "goes", direction)
                        next_elves[elf] = next_elf
                        can_move = True
                        break
                if not can_move:
                    next_elves[elf] = elf # elf does not move
            # If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
            else:
                next_elves[elf] = elf # elf does not move
                # TODO: hopefully this isn't problematic with other elves trying to move

        # After each Elf has had a chance to propose a move, the second half of the round can begin.
        # Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose
        # moving to that position.
        # If two or more Elves propose moving to the same position, none of those Elves move.
        # print("next_elves", next_elves)
        # final_moves = []

        seen = set()
        for next_elf in next_elves.values():
            if next_elf not in seen:
                seen.add(next_elf)
            else:
                # we need to dedup
                for elf in next_elves:
                    next_elf2 = next_elves[elf]
                    if next_elf2 == next_elf:
                        next_elves[elf] = elf

        elves = set(next_elves.values())
        # print("actual next", elves)

        # Finally, at the end of the round, the first direction the Elves considered is moved to the end of the
        # list of directions.
        direction_order = direction_order[1:] + [direction_order[0]]

    # count the number of empty ground tiles contained by the smallest rectangle that contains every Elf.
    min_x, max_x, min_y, max_y = find_size(elves)

    # draw_elves(elves)

    print()
    count = 0
    for j in range(min_y, max_y+1):
        for i in range(min_x, max_x+1):
            if (i, j) not in elves:
                count += 1
    print("answer", count)



def part2():
    elves = set(parseInput(23))
    print(elves)
    num_elves = len(elves)

    r = 0

    # NORTH = 0
    # EAST = 1
    # SOUTH = 2
    # WEST = 3
    direction_order = [NORTH, SOUTH, WEST, EAST]

    while True:
        r += 1
        print("\nround ", r)
        # print(direction_order)
        # draw_elves(elves)
        next_elves = {}
        # During the first half of each round, each Elf considers the eight positions adjacent to themself.
        for elf in elves:
            # Otherwise, the Elf looks in each of four directions in the following order and proposes moving one step
            # in the first valid direction:
            if has_neighbors(elves, elf, direction=None):
                can_move = False
                for direction in direction_order:
                    if not has_neighbors(elves, elf, direction=direction):
                        next_elf = move_direction(elf, direction)
                        # print("elf", elf, "goes", direction)
                        next_elves[elf] = next_elf
                        can_move = True
                        break
                if not can_move:
                    next_elves[elf] = elf # elf does not move
            # If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
            else:
                next_elves[elf] = elf # elf does not move
                # TODO: hopefully this isn't problematic with other elves trying to move

        # After each Elf has had a chance to propose a move, the second half of the round can begin.
        # Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose
        # moving to that position.
        # If two or more Elves propose moving to the same position, none of those Elves move.
        # print("next_elves", next_elves)
        # final_moves = []

        seen = set()
        for next_elf in next_elves.values():
            if next_elf not in seen:
                seen.add(next_elf)
            else:
                # we need to dedup
                for elf in next_elves:
                    next_elf2 = next_elves[elf]
                    if next_elf2 == next_elf:
                        next_elves[elf] = elf

        # check if no elf moved
        if elves == set(next_elves.values()):
            break

        elves = set(next_elves.values())
        # print("actual next", elves)

        # Finally, at the end of the round, the first direction the Elves considered is moved to the end of the
        # list of directions.
        direction_order = direction_order[1:] + [direction_order[0]]

    # draw_elves(elves)

    print("answer", r)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
