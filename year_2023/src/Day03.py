import time

class PartNumber:
    def __init__(self, id, value, coords):
        self.id = id
        self.value = value
        self.coords = set(coords)

    def __hash__(self):
        return hash((self.id, self.value, tuple(self.coords)))

    def __str__(self):
        return str(self.id) + ": " + str(self.value) + ": " + str(self.coords)

class PartSymbol:
    def __init__(self, value, coord):
        self.value = value
        self.coord = coord

    def __str__(self):
        return str(self.value) + ": " + str(self.coord)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]

        # raw data as 2d array
        rows = []
        for line in lines:
            row = []
            for char in line:
                row.append(char)
            rows.append(row)

        # find numbers and symbols
        part_numbers = []
        part_id = 0
        part_symbols = []
        for y in range(0, len(lines)):
            row = lines[y]
            curr_digit = ""
            curr_coords = []
            for x in range(len(row)):
                char = row[x]
                if char.isdecimal():
                    curr_digit += char
                    curr_coords.append(tuple([x, y]))
                else:
                    if curr_digit != "":
                        part_numbers.append(PartNumber(part_id, int(curr_digit), curr_coords))
                        part_id += 1
                    curr_digit = ""
                    curr_coords = []
                    # it's a symbol
                    if char != ".":
                        part_symbols.append(PartSymbol(char, tuple([x, y])))
            if curr_digit != "":
                part_numbers.append(PartNumber(part_id, int(curr_digit), curr_coords))

        return rows, part_numbers, part_symbols

def get_neighbors(x, y, w, h):
    neighbors = []
    for nx, ny in (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (
    x + 1, y + 1):
        if 0 <= nx < w and 0 <= ny < h:
            neighbors.append([nx, ny])
    return neighbors

def part1():
    rows, part_numbers, part_symbols = parseInput(3)

    h = len(rows)
    w = len(rows[0])

    nums_to_add = set()
    # for each symbol, check its neighbors for part_numbers
    for part_symbol in part_symbols:
        print(part_symbol)
        for nx, ny in get_neighbors(part_symbol.coord[0], part_symbol.coord[1], w, h):
            if rows[ny][nx].isdecimal():
                # lookup the coords in the part_numbers
                for part_number in part_numbers:
                    if (nx, ny) in part_number.coords:
                        print("adding: ", part_number)
                        nums_to_add.add(part_number)
    answer = 0
    for n in nums_to_add:
        print(n)
        answer += n.value
    print(answer)


def part2():
    rows, part_numbers, part_symbols = parseInput(3)

    h = len(rows)
    w = len(rows[0])

    gear_ratios = []
    # for each symbol, check its neighbors for part_numbers
    for part_symbol in part_symbols:
        print(part_symbol)
        nums_to_add = set()
        for nx, ny in get_neighbors(part_symbol.coord[0], part_symbol.coord[1], w, h):
            if rows[ny][nx].isdecimal():
                # lookup the coords in the part_numbers
                for part_number in part_numbers:
                    if (nx, ny) in part_number.coords:
                        print("adding: ", part_number)
                        nums_to_add.add(part_number)
        # check if it's a 'gear'
        gear_ratio = 1
        if len(nums_to_add) == 2:
            for n in nums_to_add:
                gear_ratio = gear_ratio * n.value
            print(gear_ratio)
            gear_ratios.append(gear_ratio)
    print(sum(gear_ratios))

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
