import re
import sys
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip('\n') for line in file]
        w = len(lines[0])  # assumes first line is one of the longest

        # pad lines with spaces
        grid = []
        for line in lines[:-2]:
            if len(line) < w:
                line = line + ' ' * (w - len(line))
            grid.append(line)

        directions = lines[-1]
        directions = re.split('(\d+)',directions)[1:-1]
        return grid, directions

def part1():
    grid, directions = parseInput(22)

    w = len(grid[0]) # assumes first line is the longest
    h = len(grid)

    # print("w: ", w, "h: ", h)
    #
    # print(grid)
    # print(directions)

    # get starting position
    start = (0, 0)
    # 0 is up
    # 90 is right
    # 180 is down
    # 270 is left
    facing = 90
    for x in range(w):
        if grid[0][x] == ".":
            start = (x, 0)
            break
    print("start", start)

    curr_pos = (start[0], start[1])
    # go through directions
    for direction in directions:
        # print("direction", direction)
        if direction.isnumeric():
            # step
            for step in range(int(direction)):
                wrap = False
                if facing == 0: # up
                    # print("moving up")
                    nx, ny = (curr_pos[0], curr_pos[1] - 1)
                    next_spot = None
                    if ny < 0: # wrap
                        wrap = True
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ":  # wrap
                            wrap = True
                    if wrap:
                        # find the first spot from the bottom that's open, or a wall
                        for i in range(h - 1, -1, -1):
                            wrap_spot = grid[i][nx]
                            if wrap_spot != " ":
                                next_spot = wrap_spot
                                ny = i
                                break
                    if next_spot == "#":  # stop since we hit a wall
                        # print("hit wall")
                        break
                    # the spot is open, so we can move
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                elif facing == 90: # right
                    # print("moving right")
                    nx, ny = (curr_pos[0] + 1, curr_pos[1])
                    next_spot = None
                    if nx >= w:
                        wrap = True
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ": # wrap
                            wrap = True
                    if wrap:
                        # find the first spot from the left that's open, or a wall
                        for i in range(w):
                            wrap_spot = grid[ny][i]
                            if wrap_spot != " ":
                                next_spot = wrap_spot
                                nx = i
                                break
                    if next_spot == "#": # stop since we hit a wall
                        # print("hit wall")
                        break
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                elif facing == 180:
                    # print("moving down")
                    nx, ny = (curr_pos[0], curr_pos[1] + 1)
                    next_spot = None
                    if ny >= h:
                        wrap = True
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ": # wrap
                            wrap = True
                    if wrap:
                        # find the first spot from the left that's open, or a wall
                        for i in range(h):
                            wrap_spot = grid[i][nx]
                            if wrap_spot != " ":
                                next_spot = wrap_spot
                                ny = i
                                break
                    if next_spot == "#": # stop since we hit a wall
                        # print("hit wall")
                        break
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                elif facing == 270:
                    # print("moving left")
                    nx, ny = (curr_pos[0] - 1, curr_pos[1])
                    next_spot = None
                    if nx < 0: # wrap
                        wrap = True
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ":  # wrap
                            wrap = True
                    if wrap:
                        # find the first spot from the right that's open, or a wall
                        for i in range(w - 1, -1, -1):  # TODO: check whether this is right
                            wrap_spot = grid[ny][i]
                            if wrap_spot != " ":
                                next_spot = wrap_spot
                                nx = i
                                break
                    if next_spot == "#":  # stop since we hit a wall
                        # print("hit wall")
                        break
                    # the spot is open, so we can move
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                else:
                    print("facing unknown direction", facing)
                    sys.exit(1)
        else: # turn
            if direction == "R":
                facing += 90
            elif direction == "L":
                facing -= 90
            facing = facing % 360
        # print()
    print("final pos", curr_pos, "final facing", facing)

    final_facing = 0
    if facing == 180:
        final_facing = 1
    elif facing == 270:
        final_facing = 2
    elif facing == 0:
        final_facing = 3
    final_row = curr_pos[0]+1
    final_col = curr_pos[1]+1
    print("answer final pos",final_row, final_col, "final facing", final_facing)

    print("answer: ", (1000 * final_col) + (4 * final_row) + final_facing)



def part2():
    grid, directions = parseInput(22)

    w = len(grid[0]) # assumes first line is the longest
    h = len(grid)

    # print("w: ", w, "h: ", h)

    # print(grid)
    # print(directions)

    # get starting position
    start = (0, 0)
    # 0 is up
    # 90 is right
    # 180 is down
    # 270 is left
    facing = 90
    for x in range(w):
        if grid[0][x] == ".":
            start = (x, 0)
            break
    print("start", start)

    curr_pos = (start[0], start[1])
    # go through directions
    for direction in directions:
        # print("direction", direction)
        if direction.isnumeric():
            # step
            for step in range(int(direction)):
                old_facing = facing
                wrap = False
                if facing == 0: # up
                    # print("moving up")
                    nx, ny = (curr_pos[0], curr_pos[1] - 1)
                    next_spot = None
                    if ny < 0: # wrap goes out of bounds
                        wrap = True
                        # We are either in face 0, going to the left edge of 5 (0 left is 5 top)
                        if nx <= 99: # face 0
                            # go to left edge of 5, and face right
                            facing = 90
                            # (50,-1) becomes (0, 150)
                            # (51 , -1) becomes (0, 151)
                            # (99, -1) becomes (0, 199)
                            (nx, ny) = (0, curr_pos[0] + 100)
                        else: # face 1, going to bottom of 5
                            # print("face 1, going to bottom of 5")
                            # still going up
                            facing = 0
                            # (100, -1) becomes (0, 199)
                            # (149, -1) becomes (49, 199)
                            (nx, ny) = (curr_pos[0] - 100, 199)
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ":  # wrap
                            wrap = True
                            # we are in face 3, going to 2
                            # turn right
                            facing = 90
                            # (0, 99) becomes (50, 50)
                            # (49, 99) becomes (50, 99)
                            (nx, ny) = (50, curr_pos[0] + 50)

                    next_spot = grid[ny][nx]
                    if next_spot == "#":  # stop since we hit a wall
                        if wrap:
                            facing = old_facing # stay facing the original way
                        # print("hit wall")
                        break
                    # the spot is open, so we can move
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                elif facing == 90: # right
                    # print("moving right")
                    nx, ny = (curr_pos[0] + 1, curr_pos[1])
                    next_spot = None
                    if nx >= w: # wrap
                        wrap = True
                        # we must be in face 1, go to face 4
                        facing = 270
                        # (150, 0) becomes (99, 149)
                        # (150, 49) becomes (99, 100)
                        (nx, ny) = (99, 149 - curr_pos[1])
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ": # wrap
                            wrap = True
                            if ny <= 99: # face 2
                                # go to bottom of 1
                                facing = 0
                                # (100, 50) becomes (100, 49)
                                # (100, 99) becomes (149, 49)
                                (nx, ny) = (curr_pos[1] + 50, 49)
                            elif ny <= 149: # face 4
                                # go to right side of 1
                                facing = 270
                                # (100, 100) becomes (149, 49)
                                # (100, 149) becomes (149, 0)
                                (nx, ny) = (149, 149 - curr_pos[1])
                            else: # face 5
                                # go to bottom of 4
                                facing = 0
                                # (50, 150) becomes (50, 149)
                                # (50, 199) becomes (99, 149)
                                (nx, ny) = (curr_pos[1] - 100, 149)

                    next_spot = grid[ny][nx]
                    if next_spot == "#": # stop since we hit a wall
                        if wrap:
                            facing = old_facing # stay facing the original way
                        # print("hit wall")
                        break
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                elif facing == 180:
                    # print("moving down")
                    nx, ny = (curr_pos[0], curr_pos[1] + 1)
                    next_spot = None
                    if ny >= h: # face 5
                        wrap = True
                        # go to top of 1
                        # still going down
                        facing = 180
                        # (0, 200)  becomes (100, 0)
                        # (49, 200) becomes (149, 0)
                        (nx, ny) = (curr_pos[0] + 100, 0)
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ": # wrap
                            wrap = True
                            if ny == 50: # face 1
                                # go to right side of 2
                                facing = 270
                                # (100, 50) becomes (99, 50)
                                # (149, 50) becomes (99, 99)
                                (nx, ny) = (99, curr_pos[0] - 50)
                            else: # face 4
                                # go to right side of 5
                                facing = 270
                                # (50, 150) becomes (49, 150)
                                # (99, 150) becomes (49, 199)
                                (nx, ny) = (49, curr_pos[0] + 100)
                    next_spot = grid[ny][nx]
                    if next_spot == "#": # stop since we hit a wall
                        if wrap:
                            facing = old_facing # stay facing the original way
                        # print("hit wall")
                        break
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                elif facing == 270:
                    # print("moving left")
                    nx, ny = (curr_pos[0] - 1, curr_pos[1])
                    next_spot = None
                    if nx < 0: # wrap
                        wrap = True
                        if ny <= 149: # face 3
                            # go to right side of 0
                            facing = 90
                            # (-1, 100) becomes (50, 49)
                            # (-1, 149) becomes (50, 0)
                            (nx, ny) = (50, 149 - curr_pos[1])
                        else: # face 5
                            # go to top of 0
                            facing = 180
                            # (-1, 150) becomes (50, 0)
                            # (-1, 199) becomes (99, 0)
                            (nx, ny) = (curr_pos[1] - 100, 0)
                    else:
                        next_spot = grid[ny][nx]
                        if next_spot == " ":  # wrap
                            wrap = True
                            if ny <= 49: # face 0
                                # go to left side of 3
                                facing = 90
                                # (49, 0)  becomes (0, 1490)
                                # (49, 49) becomes (0, 100)
                                (nx, ny) = (0, 149 - curr_pos[1])
                            else: # face 2
                                # go to top of 3
                                facing = 180
                                # (49, 50) becomes (0, 100)
                                # (49, 99) becomes (49, 100)
                                (nx, ny) = (curr_pos[1] - 50, 100)
                    next_spot = grid[ny][nx]
                    if next_spot == "#":  # stop since we hit a wall
                        if wrap:
                            facing = old_facing # stay facing the original way
                        # # print("hit wall")
                        break
                    # the spot is open, so we can move
                    curr_pos = (nx, ny)
                    # print("curr_pos", curr_pos)
                else:
                    print("facing unknown direction", facing)
                    sys.exit(1)
        else: # turn
            if direction == "R":
                facing += 90
            elif direction == "L":
                facing -= 90
            facing = facing % 360
        # print()
    print("final pos", curr_pos, "final facing", facing)

    final_facing = 0
    if facing == 180:
        final_facing = 1
    elif facing == 270:
        final_facing = 2
    elif facing == 0:
        final_facing = 3
    final_row = curr_pos[0]+1
    final_col = curr_pos[1]+1
    print("answer final pos",final_row, final_col, "final facing", final_facing)

    print("answer: ", (1000 * final_col) + (4 * final_row) + final_facing)


if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start_time = time.perf_counter()
    part1()
    end_time = time.perf_counter()
    print("Time (ms):", (end_time - start_time) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
