import time, os

class Region():
    def __init__(self, width, height, quantities):
        self.width = width
        self.height = height
        self.quantities = quantities

    def __str__(self):
        return f"{self.width}x{self.height}: {str(self.quantities)}"

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

        # set up the regions
        regions = []
        for line in lines[30:]:
            line_split = line.split(": ")
            w_h = line_split[0].split("x")
            width = w_h[0]
            height = w_h[1]
            quantities = [int(i) for i in line_split[1].split(" ")]
            regions.append(Region(width, height, quantities))

        return shapes, regions

def part1():
    shapes, regions = parseInput()
    for shape_index, shape in enumerate(shapes):
        print(f"{shape_index}:")
        for row in shape:
            print(row)
        print()

    for region in regions:
        print(region)

def part2():
    lines = parseInput()
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
