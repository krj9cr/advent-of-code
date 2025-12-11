import time, os, re, heapq
import numpy as np
import pulp


BUTTON_REGEX = re.compile(r'(\[[.#]+]) (.*) ({.*})')


class Machine:
    def __init__(self, lights_str, buttons_str, joltage_str):
        # Convert `.##.` → "0110"
        raw = lights_str[1:-1]       # remove brackets
        self.original_lights = "".join("1" if c == "#" else "0" for c in raw)
        self.lights = self.original_lights

        # Parse buttons into lists of indices
        self.buttons = [
            [int(i) for i in btn.strip("()").split(",")]
            for btn in buttons_str.split()
        ]

        # Precompute bitmasks for fast XOR
        self.button_masks = [
            self._make_bitmask(button, len(self.lights))
            for button in self.buttons
        ]

        # Parse joltage
        self.joltage = [int(i) for i in joltage_str[1:-1].split(",")]

    @staticmethod
    def _make_bitmask(indices, length):
        """Return an integer bitmask from indices."""
        mask = 0
        for i in indices:
            mask |= (1 << (length - 1 - i))
        return mask

    def reset_lights(self):
        self.lights = self.original_lights

    def __str__(self):
        return f"{self.lights} {self.buttons} {self.joltage}"

    # ------------------------------------------------------------
    # Button pressing (FAST)
    # ------------------------------------------------------------
    def press_button(self, lights, button_idx):
        """XOR lights with a precomputed bitmask."""
        mask = self.button_masks[button_idx]
        xor_value = int(lights, 2) ^ mask
        return f"{xor_value:0{len(lights)}b}"

    # ------------------------------------------------------------
    # Part 1: Dijkstra / Uniform Cost Search
    # ------------------------------------------------------------
    def part1(self):
        start_state = "0" * len(self.lights)
        goal_state = self.original_lights

        pq = [(0, start_state)]
        min_cost = {start_state: 0}

        while pq:
            cost, state = heapq.heappop(pq)

            if cost > min_cost.get(state, float("inf")):
                continue

            if state == goal_state:
                return cost   # (you only care about number of presses)

            for idx in range(len(self.buttons)):
                next_state = self.press_button(state, idx)
                new_cost = cost + 1

                if new_cost < min_cost.get(next_state, float("inf")):
                    min_cost[next_state] = new_cost
                    heapq.heappush(pq, (new_cost, next_state))

        return None

    # ------------------------------------------------------------
    # Part 2: Integer Linear Programming
    # ------------------------------------------------------------
    def part2(self):
        # Build A (coeffs) and b (constants)
        num_buttons = len(self.buttons)
        num_joltage = len(self.joltage)

        A = np.zeros((num_joltage, num_buttons), dtype=int)

        for j_idx in range(num_joltage):
            for b_idx, button in enumerate(self.buttons):
                if j_idx in button:
                    A[j_idx][b_idx] = 1

        b = np.array(self.joltage, dtype=int)

        # ILP: minimize sum(x_i)
        prob = pulp.LpProblem("MinIntegerSolution", pulp.LpMinimize)
        x_vars = [pulp.LpVariable(f"x{i}", lowBound=0, cat="Integer")
                  for i in range(num_buttons)]

        prob += sum(x_vars)

        for row in range(A.shape[0]):
            prob += pulp.lpDot(A[row], x_vars) == int(b[row])

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        return int(sum(var.value() for var in x_vars))


# ------------------------------------------------------------
# Input Parsing
# ------------------------------------------------------------
def parseInput():
    path = os.path.abspath(__file__)
    day = os.path.basename(path).removeprefix("Day").removesuffix(".py")
    input_path = os.path.join(os.path.dirname(path), f"../input/day{day}.txt")

    machines = []
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            match = BUTTON_REGEX.findall(line)[0]
            machines.append(Machine(*match))

    return machines


def part1():
    machines = parseInput()
    answer = 0
    for machine in machines:
        answer += machine.part1()
    print("answer:", answer)


def part2():
    machines = parseInput()
    answer = 0
    for machine in machines:
        answer += machine.part2()
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
