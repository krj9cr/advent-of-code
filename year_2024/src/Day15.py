import copy
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        grid = []
        directions = []
        break_line = False
        for line in file:
            line = line.strip()
            if line == "":
                break_line = True
            if break_line:
                directions += line
            else:
                grid.append([char for char in line])
        return grid, directions

def print_stuff(robot, walls, boxes, w, h):
    for j in range(h):
        for i in range(w):
            item = (i, j)
            if item == robot:
                print("@", end="")
            elif item in walls:
                print("#", end="")
            elif item in boxes:
                print("O", end="")
            else:
                print(".", end="")
        print()
    print()

def check_object_move(thing, direction, walls, boxes):
    (nx, ny) = thing
    if direction == "^":
        ny -= 1
    elif direction == "v":
        ny += 1
    elif direction == ">":
        nx += 1
    elif direction == "<":
        nx -= 1
    # try to move
    if (nx, ny) in walls:
        # thing doesn't move
        return False, thing
    elif (nx, ny) in boxes:
        # push the box and any boxes after it
        # check if this box can move...
        the_box_can_move, box_coords = check_object_move((nx, ny), direction, walls, boxes)
        if the_box_can_move:
            boxes.remove((nx, ny))
            boxes.add(box_coords)
            return True, (nx, ny)
        else:
            return False, thing
    else:
        # empty, so move
        return True, (nx, ny)

def part1():
    grid, directions = parseInput(15)

    h = len(grid)
    w = len(grid[0])
    robot = ()
    walls = set()
    boxes = set()
    # get coordinates of everything
    for j in range(h):
        row = grid[j]
        for i in range(w):
            item = row[i]
            if item == "@":
                robot = (i, j)
            elif item == "#":
                walls.add((i, j))
            elif item == "O":
                boxes.add((i, j))
    # print_stuff(robot, walls, boxes, w, h)

    # run the sim
    steps = 0
    for direction in directions:
        ### Check if robot can move
        robot_can_move, robot_coords = check_object_move(robot, direction, walls, boxes)
        if robot_can_move:
            robot = robot_coords
        # print("Steps", steps, "Dir", direction)
        # print_stuff(robot, walls, boxes, w, h)
        steps += 1

    # Count up the answer
    total = 0
    for (bx, by) in boxes:
        total += by * 100 + bx
    print(total)


def print_stuff2(robot, walls, boxes, w, h):
    for j in range(h):
        for i in range(w):
            item = (i, j)
            if item == robot:
                print("@", end="")
            elif item in walls:
                print("#", end="")
            elif item in boxes:
                print(boxes[(i, j)], end="")
            else:
                print(".", end="")
        print()
    print()

def check_object_move2(thing, direction, walls, boxes, boxes_to_move={}, depth=0):
    (nx, ny) = thing
    if direction == "^":
        ny -= 1
    elif direction == "v":
        ny += 1
    elif direction == ">":
        nx += 1
    elif direction == "<":
        nx -= 1
    # try to move
    if (nx, ny) in walls:
        # thing doesn't move
        return False, thing
    elif (nx, ny) in boxes:
        # push the box and any boxes after it
        item = boxes[(nx, ny)]
        # print("checking item", item, "at", (nx, ny))
        if direction == "^" or direction == "v":
            px, py = copy.deepcopy((nx, ny))
            if item == "]": # we know it has a pair to check, too
                px = nx - 1
            elif item == "[":
                px = nx + 1
            # check if this box can move...
            # print("recursing for", (nx, ny), (px, py))
            first_can_move, first_coords = check_object_move2((nx, ny), direction, walls, boxes, boxes_to_move, depth+1)
            second_can_move, second_coords = check_object_move2((px, py), direction, walls, boxes, boxes_to_move, depth+1)
            if first_can_move and second_can_move:
                boxes_to_move[(nx, ny)] = (first_coords, boxes[(nx, ny)])
                boxes_to_move[(px, py)] = (second_coords, boxes[(px, py)])
                if depth == 0:
                    # print("moving", boxes_to_move)
                    for old_coord in boxes_to_move:
                        new_coord, item = boxes_to_move[old_coord]
                        boxes.pop(old_coord)
                        boxes[new_coord] = item
                # else:
                    # print("able to move", (nx, ny), (px, py), "to", first_coords, second_coords)
                    # print("depth", depth, "boxes to move", boxes_to_move)
                return True, (nx, ny)
            else:
                return False, thing
        else:
            # check if this box can move horizontally, so same logic as before
            the_box_can_move, box_coords = check_object_move2((nx, ny), direction, walls, boxes)
            if the_box_can_move:
                item = boxes.pop((nx, ny))
                boxes[box_coords] = item
                return True, (nx, ny)
            else:
                return False, thing
    else:
        # empty, so move
        return True, (nx, ny)

def part2():
    grid, directions = parseInput(15)
    h = len(grid)
    w = len(grid[0])

    # embiggen the grid
    newGrid = []
    for j in range(h):
        row = grid[j]
        newRow = []
        for i in range(w):
            item = row[i]
            if item == "@":
                newRow += ["@", "."]
            elif item == "#":
                newRow += ["#", "#"]
            elif item == "O":
                newRow += ["[", "]"]
            elif item == ".":
                newRow += [".", "."]
        newGrid.append(newRow)

    grid = newGrid
    h = len(grid)
    w = len(grid[0])

    robot = ()
    walls = set()
    boxes = {}
    # get coordinates of everything
    for j in range(h):
        row = grid[j]
        for i in range(w):
            item = row[i]
            if item == "@":
                robot = (i, j)
            elif item == "#":
                walls.add((i, j))
            elif item == "[" or item == "]":
                boxes[(i, j)] = item
    # print_stuff2(robot, walls, boxes, w, h)

    # run the sim
    steps = 0
    for direction in directions:
        # print("Dir", direction)
        ### Check if robot can move
        robot_can_move, robot_coords = check_object_move2(robot, direction, walls, boxes, boxes_to_move={}, depth=0)
        if robot_can_move:
            robot = robot_coords
        # print("Steps", steps)
        # print_stuff2(robot, walls, boxes, w, h)
        steps += 1

    # Count up the answer
    total = 0
    for (bx, by) in boxes:
        item = boxes[(bx, by)]
        if item == "[":
            total += by * 100 + bx
        else:
            continue
    print(total)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
