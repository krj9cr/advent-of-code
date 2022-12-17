import sys
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        line = [line.strip() for line in file][0]
        return [ char for char in line ]

w = 7
bottom = 0

def get_next_rock(rock_idx, max_height):
    mod = rock_idx % 5
    start_y = max_height + 4
    start_x = 2
    coords = []
    if mod == 0: # minus shape
        for i in range(4):
            coords.append((start_x + i, start_y))
    elif mod == 1: # plus shape
        for j in range(3):
            if j == 0 or j == 2:
                coords.append((start_x + 1, start_y + j))
            elif j == 1:
                for i in range(3):
                    coords.append((start_x + i, start_y + j))
    elif mod == 2: # backwards L shape
        for j in range(3):
            if j == 2 or j == 1:
                coords.append((start_x + 2, start_y + j))
            elif j == 0:
                for i in range(3):
                    coords.append((start_x + i, start_y + j))
    elif mod == 3: # vertical line
        for i in range(4):
            coords.append((start_x, start_y + i))
    elif mod == 4: # square
        coords = [(start_x, start_y), (start_x + 1, start_y),
                  (start_x, start_y + 1), (start_x + 1, start_y + 1)]
    else:
        print("Unknown mod...???", mod)

    return coords

def draw(all_rock_coords, max_height, falling_rock_coords=None):
    h = max(max_height, 4)
    for j in range(h, 0, -1):
        for i in range(w):
            # print(i, j)
            if (i, j) in all_rock_coords or (i, j) in falling_rock_coords:
                print("#",end="")
            else:
                print(".", end="")
        print()
    print()


def part1():
    jets = parseInput(17)
    num_jets = len(jets)
    jet_idx = 0
    print(jets)
    all_rock_coords = [] # all rock coords that have landed
    max_height = 0

    for rock_idx in range(2022):
        # update max height
        for coord in all_rock_coords:
            if coord[1] > max_height:
                max_height = coord[1]
        # rock appears
        print(rock_idx, "rock appears, max_height = ", max_height)
        falling_rock_coords = get_next_rock(rock_idx, max_height)

        # keep falling until it stops
        while True:
            min_y = 9999999
            max_y = 0
            for coord in falling_rock_coords:
                if coord[1] < min_y:
                    min_y = coord[1]
                if coord[1] > max_y:
                    max_y = coord[1]
            # print("min_y",min_y, "max_y", max_y)
            # update max height
            max_height = max_y
            # print(rock_idx, falling_rock_coords)
            # draw(all_rock_coords, max_height, falling_rock_coords)

            # move with jet
            jet_falling_rock_coords = falling_rock_coords
            jet = jets[jet_idx]
            # print("jet", jet)
            if jet == ">":
                # get max x of rock
                max_x = 0
                for coord in falling_rock_coords:
                    if coord[0] > max_x:
                        max_x = coord[0]
                # print("max_x", max_x)
                if max_x <= w - 2:
                    can_move = True
                    jet_falling_rock_coords = []
                    for coord in falling_rock_coords:
                        new_coord = (coord[0] + 1, coord[1])
                        jet_falling_rock_coords.append(new_coord)
                        # check if blocked
                        if new_coord in all_rock_coords:
                            can_move = False
                            break
                    if not can_move: # this rock won't be moved by the jet
                        jet_falling_rock_coords = falling_rock_coords
            elif jet == "<":
                # get min x of rock
                min_x = w
                for coord in falling_rock_coords:
                    if coord[0] < min_x:
                        min_x = coord[0]
                # print("min_x", min_x)
                if min_x >= 1:
                    can_move = True
                    jet_falling_rock_coords = []
                    for coord in falling_rock_coords:
                        new_coord = (coord[0] - 1, coord[1])
                        jet_falling_rock_coords.append(new_coord)
                        if new_coord in all_rock_coords:
                            can_move = False
                            break
                    if not can_move: # this rock won't be moved by the jet
                        jet_falling_rock_coords = falling_rock_coords
            else:
                print("unknown jet direction")
                sys.exit(1)
            # draw(all_rock_coords, max_height, jet_falling_rock_coords)

            jet_idx += 1
            # wrap around if we pass the end
            if jet_idx >= num_jets:
                jet_idx = 0

            # move down
            down_falling_rock_coords = []
            # check if moving down would hit floor
            if min_y - 1 == 0:
                # print("rock hit floor")
                for coord in jet_falling_rock_coords:
                    all_rock_coords.append(coord)
                break
            else:
                # check if moving down would intersect another rock
                hit_rock = False
                for coord in jet_falling_rock_coords:
                    new_coord = (coord[0], coord[1] - 1)
                    if new_coord in all_rock_coords:
                        # print("rock would hit another rock")
                        hit_rock = True
                        break
                    down_falling_rock_coords.append(new_coord)
                if hit_rock:
                    for coord in jet_falling_rock_coords:
                        all_rock_coords.append(coord)
                    break
            falling_rock_coords = down_falling_rock_coords
            # draw(all_rock_coords, max_height, falling_rock_coords)
    print("max height", max_height)


def part2():
    jets = parseInput(17)
    num_jets = len(jets)
    jet_idx = 0
    print("num_jets", num_jets)
    pattern_idx = num_jets * 5

    all_rock_coords = [] # all rock coords that have landed
    max_height = 0

    total_rocks = 1000000000000
    # keep track of rock_idx and steps
    jet_rock_idx = None
    jet_rock_step = None
    repeat = False

    for rock_idx in range(total_rocks):
        # update max height
        for coord in all_rock_coords:
            if coord[1] > max_height:
                max_height = coord[1]
        if repeat:
            print("max height", max_height)
            r = rock_idx - 1
            print("answer?", ((total_rocks // r) * max_height) + (total_rocks % r))
            break
        # rock appears
        if rock_idx % 1000 == 0:
            print(rock_idx, "rock appears, max_height = ", max_height)
        falling_rock_coords = get_next_rock(rock_idx, max_height)

        rock_step = 0
        # keep falling until it stops
        while True:
            min_y = 9999999
            max_y = 0
            for coord in falling_rock_coords:
                if coord[1] < min_y:
                    min_y = coord[1]
                if coord[1] > max_y:
                    max_y = coord[1]
            # print("min_y",min_y, "max_y", max_y)
            # update max height
            max_height = max_y
            # print(rock_idx, falling_rock_coords)
            # draw(all_rock_coords, max_height, falling_rock_coords)

            # move with jet
            jet_falling_rock_coords = falling_rock_coords
            jet = jets[jet_idx]
            # print("jet", jet)
            if jet == ">":
                # get max x of rock
                max_x = 0
                for coord in falling_rock_coords:
                    if coord[0] > max_x:
                        max_x = coord[0]
                # print("max_x", max_x)
                if max_x <= w - 2:
                    can_move = True
                    jet_falling_rock_coords = []
                    for coord in falling_rock_coords:
                        new_coord = (coord[0] + 1, coord[1])
                        jet_falling_rock_coords.append(new_coord)
                        # check if blocked
                        if new_coord in all_rock_coords:
                            can_move = False
                            break
                    if not can_move: # this rock won't be moved by the jet
                        jet_falling_rock_coords = falling_rock_coords
            elif jet == "<":
                # get min x of rock
                min_x = w
                for coord in falling_rock_coords:
                    if coord[0] < min_x:
                        min_x = coord[0]
                # print("min_x", min_x)
                if min_x >= 1:
                    can_move = True
                    jet_falling_rock_coords = []
                    for coord in falling_rock_coords:
                        new_coord = (coord[0] - 1, coord[1])
                        jet_falling_rock_coords.append(new_coord)
                        if new_coord in all_rock_coords:
                            can_move = False
                            break
                    if not can_move: # this rock won't be moved by the jet
                        jet_falling_rock_coords = falling_rock_coords
            else:
                print("unknown jet direction")
                sys.exit(1)
            # draw(all_rock_coords, max_height, jet_falling_rock_coords)

            jet_idx += 1
            # wrap around if we pass the end
            if jet_idx >= num_jets:
                jet_idx = 0
                if jet_rock_idx is None:
                    jet_rock_idx = rock_idx
                    jet_rock_step = rock_step
                elif rock_idx == jet_rock_idx and jet_rock_step == rock_step:
                    print("repeat!! at index", rock_idx)
                    repeat = True


            # move down
            down_falling_rock_coords = []
            # check if moving down would hit floor
            if min_y - 1 == 0:
                # print("rock hit floor")
                for coord in jet_falling_rock_coords:
                    all_rock_coords.append(coord)
                break
            else:
                # check if moving down would intersect another rock
                hit_rock = False
                for coord in jet_falling_rock_coords:
                    new_coord = (coord[0], coord[1] - 1)
                    if new_coord in all_rock_coords:
                        # print("rock would hit another rock")
                        hit_rock = True
                        break
                    down_falling_rock_coords.append(new_coord)
                if hit_rock:
                    for coord in jet_falling_rock_coords:
                        all_rock_coords.append(coord)
                    break
            falling_rock_coords = down_falling_rock_coords
            # draw(all_rock_coords, max_height, falling_rock_coords)
            rock_step += 1

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
