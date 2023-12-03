import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        rows = []
        # num_coords = {}
        for line in lines:
            row = []
            # curr_digit = ""
            for char in line:
                # if char.isdecimal():
                #     curr_digit += char
                # else:
                #     if curr_digit != "":
                #         row.append(curr_digit)
                #     curr_digit = ""
                #     row.append(char)
                row.append(char)
            rows.append(row)
        return rows

def get_neighbors(x, y, w, h):
    neighbors = []
    for nx, ny in (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (
    x + 1, y + 1):
        if 0 <= nx < w and 0 <= ny < h:
            neighbors.append([nx, ny])
    return neighbors

def part1():
    lines = parseInput(3)

    h = len(lines)
    w = len(lines[0])

    # find numbers
    num_coords = {}
    for y in range(0, len(lines)):
        row = lines[y]
        curr_digit = ""
        curr_coords = []
        for x in range(len(row)):
            char = row[x]
            if char.isdecimal():
                curr_digit += char
                curr_coords.append([x, y])
            else:
                if curr_digit != "":
                    for coord in curr_coords:
                        num_coords[tuple(coord)] = int(curr_digit)
                    # num_coords[curr_digit] = curr_coords
                curr_digit = ""
                curr_coords = []
        if curr_digit != "":
            for coord in curr_coords:
                num_coords[tuple(coord)] = int(curr_digit)
    print(num_coords)

    # find symbols and get their neighbors
    nums_to_add = set()
    for y in range(0, len(lines)):
        row = lines[y]
        for x in range(len(row)):
            char = row[x]
            if not char.isdecimal() and char != ".":
                print(x, y, ":", char)
                for nx, ny in get_neighbors(x, y, w, h):
                    neighbor = lines[ny][nx]
                    print("checking neighbor:",nx,ny, neighbor)
                    if neighbor.isdecimal():
                        # if num_coords.get(tuple([nx, ny])):
                        nums_to_add.add(num_coords[tuple([nx, ny])])
    print(nums_to_add)
    print(sum(nums_to_add))

    # not 334580
    # not 335331
    # not 336560



def part2():
    lines = parseInput(3)
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
