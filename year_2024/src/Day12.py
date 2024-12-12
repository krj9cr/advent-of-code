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

def part2():
    grid = parseInput(12)
    # print_2d_grid(grid)
    garden_plots = part1()

    # for each garden plot, somehow compute the number of sides
    # something like: https://en.wikipedia.org/wiki/Gift_wrapping_algorithm ?
    for garden_plot in garden_plots:
        print(garden_plot)
        # Sort the points by Y, then by X, which puts them in grid order
        sorted_y_points = list(garden_plot.points)
        sorted_y_points.sort(key=lambda x: x[1])
        sorted_y_points.sort(key=lambda x: x[0])
        print("Sorted Points", sorted_y_points)
        print()

        # Starting with the upper-left-most point, which is guaranteed to have at least 2 sides
        # check the left, and lower 2 cells, if they match the letter, we count the sides differently
        #  4   3   3   3   2   2
        #  XA  XX  XA  XA  XX  XX
        # AA? AA? XX? AX? XX? AX?
        # depending on the layout, we recurse to the next relevant cells, maybe just finding all the cells on the edge

        # then for each cell on the edge, count its sides

        # maybe do a separate pass for holes? ughudlkj


        '''
        algorithm jarvis(S) is
            // S is the set of points
            // P will be the set of points which form the convex hull. Final set size is i.
            pointOnHull := leftmost point in S // which is guaranteed to be part of the CH(S)
            i := 0
            repeat
                P[i] := pointOnHull
                endpoint := S[0]      // initial endpoint for a candidate edge on the hull
                for j from 0 to |S| do
                    // endpoint == pointOnHull is a rare case and can happen only when j == 1 and a better endpoint has not yet been set for the loop
                    if (endpoint == pointOnHull) or (S[j] is on left of line from P[i] to endpoint) then
                        endpoint := S[j]   // found greater left turn, update endpoint
                i := i + 1
                pointOnHull := endpoint
            until endpoint == P[0]      // wrapped around to first hull point
        '''

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
