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


def draw_to_file(all_rock_coords, max_height, file_path, falling_rock_coords=None):
    with open(file_path, 'w') as file:
        h = max(max_height, 4)
        for j in range(h, 0, -1):
            for i in range(w):
                # print(i, j)
                if (i, j) in all_rock_coords or (i, j) in falling_rock_coords:
                    file.write("#")
                else:
                    file.write(".")
            file.write("\n")
        file.write("\n")


def part1():
    jets = parseInput(17)
    num_jets = len(jets)
    jet_idx = 0
    print(jets)
    all_rock_coords = [] # all rock coords that have landed
    max_height = 0

    for rock_idx in range(2022):
        # update max height
        for coord in reversed(all_rock_coords):
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
                        if new_coord in reversed(all_rock_coords):
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
                        if new_coord in reversed(all_rock_coords):
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
                    if new_coord in reversed(all_rock_coords):
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

def manhattan(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1])

def part2():
    jets = parseInput(17)
    num_jets = len(jets)
    jet_idx = 0
    print("num_jets", num_jets)

    all_rock_coords = [] # all rock coords that have landed
    max_height = 0

    simulated_height = 0
    total_rocks = 1000000000000
    cycle = {} # keep track of (rock_type, x_coords) -> [(rock_idx, max_height)]
    prev_max_height = 0
    rock_idx = 0
    cycle_found= False

    while rock_idx < total_rocks:
        # update max height
        for coord in reversed(all_rock_coords):
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
                        if new_coord in reversed(all_rock_coords):
                            can_move = False
                            break
                    if not can_move:  # this rock won't be moved by the jet
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
                        if new_coord in reversed(all_rock_coords):
                            can_move = False
                            break
                    if not can_move:  # this rock won't be moved by the jet
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
                    if new_coord in reversed(all_rock_coords):
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

        # also try to detect cycles
        rock_type = rock_idx % 5
        if not cycle_found and rock_type == 0 and rock_idx > 0:
            # get the x coordinates for the rock
            x_coords = []
            for coord in falling_rock_coords:
                x_coords.append(coord[0])
            x_coords = tuple(x_coords)
            print("rock_idx:", rock_idx, " rock_type: ", rock_type, " coord: ", x_coords, " max_height:", max_height,
                  "diff:", max_height-prev_max_height)
            # get the relative heights of each column
            column_heights = [0] * w
            for (x, y) in all_rock_coords:
                column_heights[x] = max(column_heights[x], y)
            print("column_heights:", column_heights)
            min_col_height = min(column_heights)
            column_heights = tuple([h - min_col_height for h in column_heights])
            print("relative column_heights:", column_heights)
            print()
            prev_max_height = max_height
            cycle_key = (rock_type, jet_idx, column_heights)
            if cycle_key in cycle:
                print("key", cycle_key, "cycle with!!", cycle[cycle_key])
                prev_rock_idx, prev_cycle_height = cycle[cycle_key]
                # pre_cycle_height = heights[prev_rock_idx]
                print("pre-cycle height at rock_idx: ", prev_rock_idx, "was: ", prev_cycle_height)
                cycle_height = max_height - prev_cycle_height
                cycle_rocks = rock_idx - prev_rock_idx

                # jump ahead some rock_idx-es as if we re-cycled a bunch
                mult = (total_rocks - prev_rock_idx) // cycle_rocks
                min_answer = mult * cycle_height

                remainder = (total_rocks - rock_idx) % cycle_rocks
                print("cycle_height:", cycle_height, "cycle_rocks:", cycle_rocks, "mult:", mult,
                      "min_answer:", min_answer, "remainder:", remainder)

                # simulate the remaining rocks, because we'll end up somewhere in the middle of the cycle
                # and computing height mid-cycle is hard
                rock_idx = total_rocks - remainder
                simulated_height = prev_cycle_height + min_answer - max_height # subtract out current max height since we add it back in at the end
                print("new rock_idx:", rock_idx, "simulated height", simulated_height)

                cycle_found = True
            else:
                cycle[cycle_key] = (rock_idx, max_height)
        rock_idx += 1
    # all done
    # draw_to_file(all_rock_coords, max_height, "out.txt", falling_rock_coords)
    print("final height:", max_height + simulated_height, "simulated gain:", max_height-simulated_height, "total rocks:", rock_idx)


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
