from collections import deque


def parseInput(path: str):
    with open(path, 'r') as file:
        return file.readline().strip("^").strip("$")


# almost same as day 15
def bfs(board, start):
    queue = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        y, x = path[-1]
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] != "#":
                if (y2, x2) not in seen:
                    queue.append(path + [(y2, x2)])
                    seen.add((y2, x2))
    return path


# almost the same as above but tracks cost of moving
def bfs_with_count(board, start):
    queue = deque([[start]])
    seen = {start: 0}  # key: coordinates, value: cost
    while queue:
        path = queue.popleft()
        y, x = path[-1]
        for x2, y2 in ((x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)):
            if 0 <= y2 < len(board) and 0 <= x2 < len(board[y2]) and board[y2][x2] != "#":
                new_cost = seen[(y, x)] + 1
                if (y2, x2) not in seen or new_cost < seen[(y2, x2)]:
                    queue.append(path + [(y2, x2)])
                    seen[(y2, x2)] = new_cost
    return seen


def printBoard(board):
    for row in board:
        print("".join(row))


def createBoard(doors, rooms):
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0
    points = doors.union(rooms)
    for x, y in points:
        if x < minX:
            minX = x
        if x > maxX:
            maxX = x
        if y < minY:
            minY = y
        if y > maxY:
            maxY = y
    # print("mins:", minX, minY)
    # print("maxes:", maxX, maxY)
    # we want minX, minY to be 0,0
    # and everything else offset from there
    board = []
    for j in range(0, maxY + abs(minY) + 3):
        row = []
        for i in range(0, maxX + abs(minX) + 3):
            row.append("#")
        board.append(row)
    # printBoard(board)
    for x, y in rooms:
        x2 = x + abs(minX) + 1
        y2 = y + abs(minY) + 1
        board[y2][x2] = "."
    for x, y in doors:
        x2 = x + abs(minX) + 1
        y2 = y + abs(minY) + 1
        board[y2][x2] = "|"
    start = (abs(minX)+1, abs(minY)+1)
    return board, start


def followDirections(line: str):
    stack = []
    x, y = (0, 0)
    rooms = {(x, y)}
    doors = set()

    for char in line:
        if char == "E":
            x += 1
            doors.add((x, y))
            x += 1
            rooms.add((x, y))
        elif char == "N":
            y -= 1
            doors.add((x, y))
            y -= 1
            rooms.add((x, y))
        elif char == "W":
            x -= 1
            doors.add((x, y))
            x -= 1
            rooms.add((x, y))
        elif char == "S":
            y += 1
            doors.add((x, y))
            y += 1
            rooms.add((x, y))
        elif char == "(":
            stack.append((x, y))
        elif char == ")":
            stack.pop()
        elif char == "|":
            x, y = stack[-1]  # peek
        else:
            print("bad character")
            exit(1)
    return doors, rooms


def part1(path: str):
    line = parseInput(path)
    # print(line)

    # get locations of rooms and doors
    doors, rooms = followDirections(line)
    # print("rooms:", rooms)

    # draw a map of the facility
    board, start = createBoard(doors, rooms)
    # printBoard(board)
    # print("start:", start)

    # run bfs
    flip_start = (start[1], start[0])
    path = bfs(board, flip_start)

    # print(path)
    # since we're "stepping" on doors and rooms
    # the total doors we went through is -1 for the start and divide 2 for the rooms
    print("part1:", (len(path)-1) / 2)


def part2(path: str):
    line = parseInput(path)
    doors, rooms = followDirections(line)
    board, start = createBoard(doors, rooms)

    flip_start = (start[1], start[0])
    rooms = bfs_with_count(board, flip_start)

    total_rooms = 0
    for x, y in rooms:
        # divide by 2 again since we're counting moving to doors and to rooms
        # rather than just counting moving "through" a door
        if board[y][x] == "." and rooms[(y, x)] / 2 >= 1000:
                total_rooms += 1
    print("part2:", total_rooms)
