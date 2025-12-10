import time, os
import re

class Machine:
    def __init__(self, lights_str, buttons_str, joltage_str):
        lights = lights_str.strip("[").strip("]")
        # print(lights)
        self.lights = []
        for l in lights:
            if l == ".":
                self.lights.append(False)
            else:
                self.lights.append(True)
        buttons_split = buttons_str.split(" ")
        # print(buttons_split)
        self.buttons = []
        for button in buttons_split:
            self.buttons.append([int(i) for i in button.strip("(").strip(")").strip().split(",")])
        self.joltage = [int(i) for i in joltage_str.strip("{").strip("}").split(",")]

    def __str__(self):
        return str(self.lights) + " " + str(self.buttons) + " " + str(self.joltage)

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            pattern = r'(\[[\.#]+]) (.*) ({.*})'
            data_groups = re.findall(pattern, line)
            lines.append(Machine(data_groups[0][0], data_groups[0][1], data_groups[0][2]))
        return lines

def part1():
    machines = parseInput()
    for machine in machines:
        print(machine)

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
