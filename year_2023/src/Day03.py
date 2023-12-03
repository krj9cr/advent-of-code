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

        h = len(lines)
        w = len(lines[0])

        # raw data as 2d array
        rows = []

        # find numbers and symbols
        part_numbers = []
        part_id = 0
        part_symbols = []
        for y in range(0, h):
            raw_row = []
            row = lines[y]
            curr_digit = ""
            curr_coords = []
            for x in range(0, w):
                char = row[x]
                raw_row.append(char)
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
            rows.append(raw_row)
            if curr_digit != "":
                part_numbers.append(PartNumber(part_id, int(curr_digit), curr_coords))

        # convert part_numbers to a dict for easy coordinate lookups
        part_numbers_dict = {}
        for part_number in part_numbers:
            for coord in part_number.coords:
                part_numbers_dict[coord] = part_number

        return rows, w, h, part_numbers, part_symbols, part_numbers_dict

def get_neighbors(x, y, w, h):
    neighbors = []
    for nx, ny in (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), \
                  (x - 1, y), (x + 1, y), (x - 1, y + 1), \
                  (x, y + 1), (x + 1, y + 1):
        if 0 <= nx < w and 0 <= ny < h:
            neighbors.append([nx, ny])
    return neighbors

def part1():
    rows, w, h, part_numbers, part_symbols, part_numbers_dict = parseInput(3)

    nums_to_add = set()
    # for each symbol, check its neighbors for part_numbers
    for part_symbol in part_symbols:
        # print(part_symbol)
        for nx, ny in get_neighbors(part_symbol.coord[0], part_symbol.coord[1], w, h):
            if rows[ny][nx].isdecimal():
                # lookup the coords in the part_numbers
                nums_to_add.add(part_numbers_dict[(nx, ny)])
    answer = 0
    for n in nums_to_add:
        # print(n)
        answer += n.value
    print(answer)


def part2():
    rows, w, h, part_numbers, part_symbols, part_numbers_dict = parseInput(3)

    answer = 0
    # for each symbol, check its neighbors for part_numbers
    for part_symbol in part_symbols:
        # print(part_symbol)
        nums_to_add = set()
        for nx, ny in get_neighbors(part_symbol.coord[0], part_symbol.coord[1], w, h):
            if rows[ny][nx].isdecimal():
                # lookup the coords in the part_numbers
                nums_to_add.add(part_numbers_dict[(nx, ny)])
        # check if it's a 'gear'
        gear_ratio = 1
        if len(nums_to_add) == 2:
            for n in nums_to_add:
                gear_ratio = gear_ratio * n.value
            answer += gear_ratio
    print(answer)

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
