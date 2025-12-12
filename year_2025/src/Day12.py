import time, os
import numpy as np

class Shape:
    def __init__(self, arr):
        self.arr = np.array(arr)
        self.area = len(self.get_coords(arr))

    @staticmethod
    def get_coords(arr):
        coords = []
        for j, row in enumerate(arr):
            for i, item in enumerate(row):
                if item == "#":
                    coords.append((i, j))
        return coords

    def __str__(self):
        arr_str = ""
        for row in self.arr:
            arr_str += row + "\n"
        return arr_str


class Region:
    def __init__(self, width, height, quantities):
        self.width = width
        self.height = height
        self.quantities = quantities
        self.filled_spots = []

    def __str__(self):
        return f"{self.width}x{self.height}: {str(self.quantities)}"

    def print_region(self):
        for j in range(self.height):
            for i in range(self.width):
                if (i, j) in self.filled_spots:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def check_shapes(self, shapes):
        area = self.width * self.height
        # ....ew
        over_assumed_shape_area = sum(self.quantities) * 8

        if over_assumed_shape_area < area:
            return True
        return False

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        # read all the lines
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)

        # grab the shapes manually I guess idc
        shapes = [ lines[1:4], lines[6:9], lines[11:14], lines[16:19], lines[21:24], lines[26:29]]
        for i, shape in enumerate(shapes):
            shapes[i] = Shape(shape)

        # set up the regions
        regions = []
        for line in lines[30:]:
            line_split = line.split(": ")
            w_h = line_split[0].split("x")
            width = int(w_h[0])
            height = int(w_h[1])
            quantities = [int(i) for i in line_split[1].split(" ")]
            regions.append(Region(width, height, quantities))

        return shapes, regions

def part1():
    shapes, regions = parseInput()

    # for shape in shapes:
    #     print(shape)
    #     print()

    count = 0
    for region in regions:
        # print(region)
        fits = region.check_shapes(shapes)
        if fits:
            count += 1
    print(count)


def part2():
    print("gold star")

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
