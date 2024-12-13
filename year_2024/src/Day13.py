import sys
import time
import re
import math

class Machine:
    def __init__(self):
        self.a_x = 0
        self.a_y = 0
        self.b_x = 0
        self.b_y = 0
        self.prize_x = 0
        self.prize_y = 0

    def __str__(self):
        return "A: " + str(self.a_x) + "," + str(self.a_y) + " B: " + str(self.b_x) + "," + str(self.b_y) \
               + "\nPrize: " + str(self.prize_x) + "," + str(self.prize_y) + "\n"

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        machines = []
        machine = Machine()
        for line in file:
            line = line.strip()
            if line == "":
                machines.append(machine)
                machine = Machine()
                continue
            if "Button" in line:
                matches = re.finditer(r"Button ([A|B]): X\+([0-9]+), Y\+([0-9]+)", line)
                for match in matches:
                    letter = match.group(1)
                    x = int(match.group(2))
                    y = int(match.group(3))
                    if letter == "A":
                        machine.a_x = x
                        machine.a_y = y
                    elif letter == "B":
                        machine.b_x = x
                        machine.b_y = y
            elif "Prize" in line:
                matches = re.finditer(r"Prize: X=([0-9]+), Y=([0-9]+)", line)
                for match in matches:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    machine.prize_x = x
                    machine.prize_y = y
        machines.append(machine)
        return machines

def part1():
    machines = parseInput(13)

    total = 0
    for machine in machines:
        print(machine)

        # from 0 to 100 for both buttons
        made_it = False
        min_cost = sys.maxsize
        for i_a in range(0, 101):
            x = 0
            y = 0
            for i_b in range(0, 101):
                # try pressing the button that many times and see if we win da prize
                x = machine.a_x * i_a + machine.b_x * i_b
                y = machine.a_y * i_a + machine.b_y * i_b
                if machine.prize_x == x and machine.prize_y == y:
                    print("Made it in A presses:", i_a, "and B presses:", i_b)
                    made_it = True
                    # compute cost
                    cost = i_a * 3 + i_b * 1
                    if cost < min_cost:
                        min_cost = cost
        if made_it:
            total += min_cost

    print(total)

'''
A * a_x + B * b_x = prize_x
A * a_y + B * b_y = prize_y

Cramer's rule:
A = (prize_x*b_y - prize_y*b_x) / (a_x*b_y - a_y*b_x)
B = (a_x*prize_y - a_y*prize_x) / (a_x*b_y - a_y*b_x)
'''
def part2():
    machines = parseInput(13)

    for machine in machines:
        machine.prize_x += 10000000000000
        machine.prize_y += 10000000000000

    total = 0
    for machine in machines:
        print(machine)

        det = (machine.a_x * machine.b_y - machine.a_y * machine.b_x)
        i_a = (machine.prize_x * machine.b_y - machine.prize_y * machine.b_x) // det
        i_b = (machine.prize_y * machine.a_x - machine.prize_x * machine.a_y) // det

        x = machine.a_x * i_a + machine.b_x * i_b
        y = machine.a_y * i_a + machine.b_y * i_b
        if machine.prize_x == x and machine.prize_y == y:
            print("Made it in A presses:", i_a, "and B presses:", i_b)

            cost = i_a * 3 + i_b * 1
            print("cost", cost)
            total += cost

    print(total)

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
