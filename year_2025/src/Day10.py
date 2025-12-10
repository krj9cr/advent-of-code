import time, os
import re
import heapq
import numpy as np
import pulp

class Machine:
    def __init__(self, lights_str, buttons_str, joltage_str):
        # parse lights
        lights = lights_str.strip("[").strip("]")
        self.lights = ""
        for l in lights:
            if l == ".":
                self.lights += "0"
            else:
                self.lights += "1"

        self.original_lights = self.lights

        # parse buttons
        buttons_split = buttons_str.split(" ")
        # print(buttons_split)
        self.buttons = []
        for button in buttons_split:
            self.buttons.append([int(i) for i in button.strip("(").strip(")").strip().split(",")])

        # parst joltage
        self.joltage = [int(i) for i in joltage_str.strip("{").strip("}").split(",")]

    def reset_lights(self):
        self.lights = self.original_lights

    def __str__(self):
        return str(self.lights) + " " + str(self.buttons) + " " + str(self.joltage)

    def find_buttons_to_press(self, lights):
        indicies = []
        for index, char in enumerate(lights):
            if char == "1":
                indicies.append(index)
        # print(indicies)
        # find buttons that include these indicies
        button_indices = set()
        for button_index, button in enumerate(self.buttons):
            for index in indicies:
                if index in button:
                    button_indices.add(button_index)
        # print("button_indices:", button_indices)
        return button_indices

    def press_button(self, lights, button_idx):
        button = self.buttons[button_idx]
        print("pressing button: ", button)
        # turn the button into a binary sequence
        # TODO: separate this out so we don't repeat it every button press
        button_flags = ["0"] * len(lights)
        print("lights", lights)
        for light_idx in button:
            button_flags[light_idx] = "1"
        print("flags ", ''.join(button_flags))
        # do an XOR on the lights with button flags
        xor_result = int(lights,2) ^  int(''.join(button_flags), 2)
        result = f"{xor_result:0{len(lights)}b}"
        print("result", lights)
        return result

    def part1(self):
        initial_state = "0" * len(self.original_lights)
        # Priority queue stores tuples: (current_cost, current_state, button_sequence)
        # The smallest cost is always popped first
        priority_queue = [(0, initial_state, [])]

        # We track the minimum cost found so far to reach a specific node.
        # This is crucial when cycles exist and nodes are revisited.
        min_cost_to_node = {initial_state: 0}

        while priority_queue:
            current_cost, current_state, button_sequence = heapq.heappop(priority_queue)

            # If we have already found a cheaper way to this node than
            # the current path's cost, skip this path.
            if current_cost > min_cost_to_node.get(current_state, float('inf')):
                continue

            # if all the lights off, we are done
            if current_state == self.original_lights:
                print("DONE", current_state)
                return button_sequence

            # Explore neighbors, which are next buttons to press
            # generate sequences of button presses...
            # prioritize starting with buttons that include lights that are on
            button_indices = range(len(self.buttons))  #self.find_buttons_to_press(current_state)

            # create paths/branches for each button press, trying to press each button
            for button_index in button_indices:
                button = self.buttons[button_index]
                next_state = self.press_button(current_state, button_index)
                new_cost = current_cost + 1

                # check if any joltages are higher than what we want
                bad = False
                for i, joltage in next_state:
                    if joltage > self.joltage[i]:
                        bad = True
                        break
                if not bad:
                    # If this new path to the neighbor is cheaper than any
                    # previous path recorded for that neighbor:
                    if new_cost < min_cost_to_node.get(next_state, float('inf')):
                        min_cost_to_node[next_state] = new_cost
                        new_path = list(button_sequence)
                        new_path.append(button)
                        # Add this promising new path to the priority queue
                        heapq.heappush(priority_queue, (new_cost, next_state, new_path))

        return

    def press_button_part2(self, joltages, button_idx):
        button = self.buttons[button_idx]
        # print("pressing button: ", button)
        new_joltages = list(joltages)
        for index in button:
            new_joltages[index] += 1
        # print("result", new_joltages)
        return new_joltages

    def part2(self):
        # idea: rather than creating paths, simulate pressing this button multiple times?
        # then press each button X times in different sequences? because the buttton sequence shouldn't
        # matter as much since we're just incrementing?
        # it is like we need
        # b0 * x + b1 * y + b2 * z + ... = [j1, j2, j3, j4]
        # which is really
        # [b0a, b0b, b0c] * x + [b1a, b1b, b1c] * y + ... = [ja, jb, jc...]

        # but that can be decomposed into multiple equations...
        # b0a * x + b1a * y +... = ja
        # b0b * x + b1b * y +... = jb

        # for each joltage index
        # find the buttons that press it, generate an array
        coefficients = []
        constants = []
        for joltage_index, joltage in enumerate(self.joltage):
            constants.append(joltage)
            joltage_coefficients = []
            for button_index, button in enumerate(self.buttons):
                if joltage_index in button:
                    joltage_coefficients.append(1)
                else:
                    joltage_coefficients.append(0)
            coefficients.append(joltage_coefficients)
        print(coefficients)
        print(constants)

        A = np.array(coefficients)
        b = np.array(constants)

        n = A.shape[1]

        # ILP problem: minimize sum(x)
        prob = pulp.LpProblem("MinIntegerSolution", pulp.LpMinimize)

        # integer variables x1..xn >= 0
        x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(n)]

        # objective
        prob += sum(x)

        # constraints A·x = b
        for i in range(A.shape[0]):
            prob += (pulp.lpDot(A[i], x) == int(b[i]))

        # solve
        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        button_presses = [x[i].value() for i in range(n)]
        print(button_presses)

        return int(sum(button_presses))


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
    answer = 0
    for machine in machines:
        print(machine)
        # machine.press_button(0)
        # machine.find_buttons_to_press()
        buttons = machine.part1()
        presses = len(buttons)
        print(buttons, presses)
        answer += presses
        print()
    print("answer:", answer)

def part2():
    machines = parseInput()
    answer = 0
    for machine in machines:
        print(machine)
        # machine.press_button_part2([0] * len(machine.joltage), 0)
        presses = machine.part2()
        print("presses", presses)
        answer += presses
        print()
    print("answer:", answer)

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
