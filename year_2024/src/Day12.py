import time

class GardenPlot:
    def __init__(self):
        self.letter = None
        self.area = 0
        self.perimeter = 0
        self.points = set()

    def __str__(self):
        return "Letter: " + str(self.letter) + " Area: " + str(self.area) + " Perimeter: " + str(self.perimeter) \
               + "\n Points: " + str(self.points)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append([char for char in line])
        return lines

def print_2d_grid(grid):
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            print(item, end="")
        print()
    print()

def find_garden_plot(first, letter, grid, garden_plot, seen, garden_seen=set()):
    garden_plot.letter = letter
    garden_plot.points.add(first)

    garden_seen.add(first)
    # print("...at", first)
    i, j = first
    for x2, y2 in ((i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)):
        if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
            item2 = grid[y2][x2]
            if item2 == letter:
                if (x2, y2) in garden_seen:
                    continue
                # print("...found", (x2, y2))
                garden_plot.points.add((x2, y2))
                garden_seen.add((x2, y2))
                # seen.add((x2, y2))
                find_garden_plot((x2, y2), letter, grid, garden_plot, seen, garden_seen)
            else:
                garden_plot.perimeter += 1
        else:
            garden_plot.perimeter += 1
    # print("seen", letter, (i, j))
    seen.add((i, j))

def part1():
    grid = parseInput(12)
    # print_2d_grid(grid)

    seen = set()
    garden_plots = []
    # maybe just find all the groups, first??
    # for every spot in the grid...
    for j in range(len(grid)):
        row = grid[j]
        for i in range(len(row)):
            item = row[i]
            if (i, j) in seen:
                continue
            # check what borders it
            loner = 0
            for x2, y2 in ((i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)):
                if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                    item2 = grid[y2][x2]
                    if item == item2:
                        if (x2, y2) in seen:
                            continue
                        # print(item, "Starting GROUP")
                        # we have a group!!!
                        # we need to figure out the whole group now, and get a garden plot
                        garden_plot = GardenPlot()
                        find_garden_plot((i, j), item, grid, garden_plot, seen)
                        garden_plots.append(garden_plot)
                        # print("seen", item2, (i, j))
                        seen.add((x2, y2))
                    else:
                        loner += 1
                        # we do not have a group
                        # count this towards the group perimeter, somehow
                        # start a new group for item2?
                else:
                    loner += 1
            if loner == 4:
                garden_plot = GardenPlot()
                garden_plot.letter = item
                garden_plot.points.add((i, j))
                garden_plot.perimeter = 4
                garden_plot.area = 1
                garden_plots.append(garden_plot)

    # at the end, add upp all the garden plots
    total = 0
    for garden_plot in garden_plots:
        garden_plot.area = len(garden_plot.points)
        # print(garden_plot)
        total += garden_plot.area * garden_plot.perimeter
    print("TOTAL", total)
    return garden_plots

def checkBounds(point, grid):
    x2, y2 = point
    if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
        return True
    return False

def part2():
    grid = parseInput(12)
    # print_2d_grid(grid)
    garden_plots = part1()

    total = 0
    # for each garden plot, somehow compute the number of sides
    # something like: https://en.wikipedia.org/wiki/Gift_wrapping_algorithm ?
    for garden_plot in garden_plots:
        print(garden_plot)
        letter = garden_plot.letter
        sides_total = 0

        side_points = set()
        # Do a recursive traversal and save all the cells that have a side
        for (x, y) in garden_plot.points:
            i, j = (x, y)
            item = grid[y][x]
            for x2, y2 in ((i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)):
                if 0 <= x2 < len(grid[0]) and 0 <= y2 < len(grid):
                    item2 = grid[y2][x2]
                    if item != item2:
                        side_points.add((x, y))
                else:
                    side_points.add((x, y))
        print("Side points", side_points)

        # Sort the points by Y, then by X, which puts them in grid order
        sorted_points = list(side_points)
        sorted_points.sort(key=lambda x: x[1])
        print("Sorted Points", sorted_points)

        first_j = sorted_points[0][1]
        last_j = sorted_points[-1][1]
        rows = []
        for j in range(first_j, last_j+1):
            row = []
            for (x, y) in sorted_points:
                if j == y:
                    row.append((x,y))
            if len(row) > 0:
                rows.append(row)
        sorted_points.sort(key=lambda x: x[0])
        first_i = sorted_points[0][0]
        last_i = sorted_points[-1][0]
        cols = []
        for i in range(first_i, last_i+1):
            col = []
            for (x, y) in sorted_points:
                if i == x:
                    col.append((x, y))
            if len(col) > 0:
                cols.append(col)
        print(rows)
        print(cols)

        # check which items have a top, group them together if adjacent
        for row in rows:
            has_top = []
            has_bottom = []
            for (x, y) in row:
                # TOPS
                x2, y2 = (x, y - 1)
                in_bounds = checkBounds((x2, y2), grid)
                if not in_bounds or (in_bounds and grid[y2][x2] != letter):
                    has_top.append((x, y))
                # BOTTOMS
                x2, y2 = (x, y + 1)
                in_bounds = checkBounds((x2, y2), grid)
                if not in_bounds or (in_bounds and grid[y2][x2] != letter):
                    has_bottom.append((x, y))
            # group the ones that have tops
            has_top.sort(key=lambda x: x[0])
            if len(has_top) > 0:
                curr_x = has_top[0][0]
                groups = 0
                for (x, y) in has_top:
                    if x - curr_x != 1:
                        groups += 1
                    curr_x = x
                print("row tops:", has_top, groups)
                sides_total += groups
            # group the ones that have bottoms
            has_bottom.sort(key=lambda x: x[0])
            if len(has_bottom) > 0:
                curr_x = has_bottom[0][0]
                groups = 0
                for (x, y) in has_bottom:
                    if x - curr_x != 1:
                        groups += 1
                    curr_x = x
                print("row bottoms:", has_bottom, groups)
                sides_total += groups

        ### OK
        # check which items have a LEFT and RIGHT, group them together if adjacent
        for col in cols:
            has_left = []
            has_right = []
            for (x, y) in col:
                # LEFTS
                x2, y2 = (x - 1, y)
                in_bounds = checkBounds((x2, y2), grid)
                if not in_bounds or (in_bounds and grid[y2][x2] != letter):
                    has_left.append((x, y))
                # BOTTOMS
                x2, y2 = (x + 1, y)
                in_bounds = checkBounds((x2, y2), grid)
                if not in_bounds or (in_bounds and grid[y2][x2] != letter):
                    has_right.append((x, y))
            # group the ones that have lefts
            has_left.sort(key=lambda x: x[1])
            if len(has_left) > 0:
                curr_y = has_left[0][1]
                groups = 0
                for (x, y) in has_left:
                    if y - curr_y != 1:
                        groups += 1
                    curr_y = y
                print("col lefts:", has_left, groups)
                sides_total += groups
            # group the ones that have bottoms
            has_right.sort(key=lambda x: x[1])
            if len(has_right) > 0:
                curr_y = has_right[0][1]
                groups = 0
                for (x, y) in has_right:
                    if y - curr_y != 1:
                        groups += 1
                    curr_y = y
                print("col rights:", has_right, groups)
                sides_total += groups
        print("Total sides: ", sides_total)
        total += garden_plot.area * sides_total
        print()
    print("TOTAL", total)


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
