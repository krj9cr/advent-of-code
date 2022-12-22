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

    print("w: ", w, "h: ", h)

    print(grid)
    print(directions)

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
        print("direction", direction)
        if direction.isnumeric():
            # step
            for step in range(int(direction)):
                wrap = False
                if facing == 0: # up
                    print("moving up")
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
                        for i in range(h - 1, -1, -1):  # TODO: check whether this is right
                            print(nx, i)
                            wrap_spot = grid[i][nx]
                            if wrap_spot != " ":
                                next_spot = wrap_spot
                                ny = i
                                break
                    if next_spot == "#":  # stop since we hit a wall
                        print("hit wall")
                        break
                    # the spot is open, so we can move
                    curr_pos = (nx, ny)
                    print("curr_pos", curr_pos)
                elif facing == 90: # right
                    print("moving right")
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
                        print("hit wall")
                        break
                    curr_pos = (nx, ny)
                    print("curr_pos", curr_pos)
                elif facing == 180:
                    print("moving down")
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
                        print("hit wall")
                        break
                    curr_pos = (nx, ny)
                    print("curr_pos", curr_pos)
                elif facing == 270:
                    print("moving left")
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
                        print("hit wall")
                        break
                    # the spot is open, so we can move
                    curr_pos = (nx, ny)
                    print("curr_pos", curr_pos)
                else:
                    print("facing unknown direction", facing)
                    sys.exit(1)
        else: # turn
            if direction == "R":
                facing += 90
            elif direction == "L":
                facing -= 90
            facing = facing % 360
        print()
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
    lines = parseInput(22)
    print(lines)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start_time = time.perf_counter()
    part1()
    end_time = time.perf_counter()
    print("Time (ms):", (end_time - start_time) * 1000)

    # print("\nPART 2 RESULT")
    # start = time.perf_counter()
    # part2()
    # end = time.perf_counter()
    # print("Time (ms):", (end - start) * 1000)
