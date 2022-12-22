import copy
import re
import sys
import time
import math

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        blueprints = []
        for line in lines:
            # split = line.split(".")
            # print(split)
            numbers = re.findall(r'\d+', line)
            _, ore_robot_ore_cost, clay_robot_ore_cost,\
            obsidian_robot_ore_cost, obsidian_robot_clay_cost,\
            geode_robot_ore_cost, geode_robot_obsidian_cost = [int(x) for x in numbers]
            # ore_robot_ore_cost = int(split[0].split(" ")[-2])
            # clay_robot_ore_cost = int(split[1].split(" ")[-2])
            # obsidian_robot_ore_cost = int(split[2].split(" ")[5])
            # obsidian_robot_clay_cost = int(split[2].split(" ")[-2])
            # geode_robot_ore_cost = int(split[3].split(" ")[5])
            # geode_robot_obsidian_cost = int(split[3].split(" ")[-2])

            blueprints.append(Blueprint(ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost,
                                        obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost))
        return blueprints

class Blueprint:
    def __init__(self, ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost,
                 geode_robot_ore_cost, geode_robot_obsidian_cost, minute=1):
        self.ore_robot_count = 1
        self.clay_robot_count = 0
        self.obsidian_robot_count = 0
        self.geode_robot_count = 0
        self.minute = minute

        self.ore_robot_ore_cost = ore_robot_ore_cost
        self.clay_robot_ore_cost = clay_robot_ore_cost
        self.obsidian_robot_ore_cost = obsidian_robot_ore_cost
        self.obsidian_robot_clay_cost = obsidian_robot_clay_cost
        self.geode_robot_ore_cost = geode_robot_ore_cost
        self.geode_robot_obsidian_cost = geode_robot_obsidian_cost

        # limit building robots to the most expensive cost of any robot
        self.max_ore_bots = max(self.ore_robot_ore_cost, self.clay_robot_ore_cost, self.obsidian_robot_ore_cost, self.geode_robot_ore_cost)
        self.max_clay_bots = self.obsidian_robot_clay_cost
        self.max_obsidian_bots = self.obsidian_robot_clay_cost

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

    def hash(self):
        return f"{self.minute}: {self.ore_robot_count}, {self.clay_robot_count}, {self.obsidian_robot_count}, " \
               f"{self.geode_robot_count}. {self.ore}, {self.clay}, {self.obsidian}, {self.geodes}"

    def get_next_states(self, best_so_far, max_minutes):
        minutes_left = max_minutes - self.minute + 1
        # print(self.hash(), "best", best)

        # check if we should just stop
        # if we hypothetically created a geode bot every remaining minute and are still less than best
        best_possible_geodes = self.geodes
        for i in range(minutes_left+1):
            best_possible_geodes += self.geode_robot_count + i
        if best_so_far > 0 and best_possible_geodes < best_so_far:
            return []

        states = []
        # play it out, doing this helps us get a better best_so_far
        if self.geode_robot_count > 0:
            next_state = copy.deepcopy(self)
            next_state.collect(minutes_left)
            next_state.minute += minutes_left
            states.append(next_state)

        # build geode
        if self.obsidian_robot_count > 0:
            ore_minutes_from_now = math.ceil(max(self.geode_robot_ore_cost - self.ore, 0) / self.ore_robot_count) + 1
            obsidian_minutes_from_now = math.ceil(max(self.geode_robot_obsidian_cost - self.obsidian, 0) / self.obsidian_robot_count) + 1
            minutes_from_now = max(ore_minutes_from_now, obsidian_minutes_from_now, 0)
            if minutes_from_now <= minutes_left:
                next_state = copy.deepcopy(self)
                next_state.collect(minutes_from_now)
                next_state.build_robot(3)
                next_state.minute += minutes_from_now
                states.append(next_state)
                # return states # TODO: make this faster?

        # build obsidian
        if self.clay_robot_count > 0 and self.obsidian_robot_count < self.max_obsidian_bots:
            ore_minutes_from_now = math.ceil(max(self.obsidian_robot_ore_cost - self.ore, 0) / self.ore_robot_count) + 1
            clay_minutes_from_now = math.ceil(max(self.obsidian_robot_clay_cost - self.clay,0) / self.clay_robot_count) + 1
            minutes_from_now = max(ore_minutes_from_now, clay_minutes_from_now, 0)
            if minutes_from_now <= minutes_left:
                next_state = copy.deepcopy(self)
                next_state.collect(minutes_from_now)
                next_state.build_robot(2)
                next_state.minute += minutes_from_now
                states.append(next_state)

        # build clay
        if self.clay_robot_count < self.max_clay_bots:
            minutes_from_now = math.ceil(max(self.clay_robot_ore_cost - self.ore, 0) / self.ore_robot_count) + 1
            minutes_from_now = max(minutes_from_now, 0)
            if minutes_from_now <= minutes_left:
                next_state = copy.deepcopy(self)
                next_state.collect(minutes_from_now)
                next_state.build_robot(1)
                next_state.minute += minutes_from_now
                states.append(next_state)

        # build ore
        if self.ore_robot_count < self.max_ore_bots:
            minutes_from_now = math.ceil(max(self.ore_robot_ore_cost - self.ore, 0) / self.ore_robot_count) + 1
            minutes_from_now = max(minutes_from_now, 0)
            if minutes_from_now <= minutes_left:
                next_state = copy.deepcopy(self)
                next_state.collect(minutes_from_now)
                next_state.build_robot(0)
                next_state.minute += minutes_from_now
                states.append(next_state)

        return states

    def collect(self, minutes=1):
        self.ore += self.ore_robot_count * minutes
        self.clay += self.clay_robot_count * minutes
        self.obsidian += self.obsidian_robot_count * minutes
        self.geodes += self.geode_robot_count * minutes

    # 0 - ore, 1 - clay, 2 - obsidian, 3 - geode
    # Don't call this before 'collect'!
    def build_robot(self, robot_idx):
        if robot_idx == 0:
            self.ore -= self.ore_robot_ore_cost
            self.ore_robot_count += 1
        elif robot_idx == 1:
            self.ore -= self.clay_robot_ore_cost
            self.clay_robot_count += 1
        elif robot_idx == 2:
            self.ore -= self.obsidian_robot_ore_cost
            self.clay -= self.obsidian_robot_clay_cost
            self.obsidian_robot_count += 1
        elif robot_idx == 3:
            self.ore -= self.geode_robot_ore_cost
            self.obsidian -= self.geode_robot_obsidian_cost
            self.geode_robot_count += 1
        else:
            print("error, bad robot index", robot_idx)
            sys.exit(1)


    def __repr__(self):
        return f"Blueprint robots: {self.ore_robot_count}, {self.clay_robot_count}, {self.obsidian_robot_count}, " \
               f"{self.geode_robot_count}. Costs: {self.ore_robot_ore_cost}, {self.clay_robot_ore_cost}, " \
               f"{self.obsidian_robot_ore_cost} + {self.obsidian_robot_clay_cost}, {self.geode_robot_ore_cost} + " \
               f"{self.geode_robot_obsidian_cost}. Resources: {self.ore}, {self.clay}, {self.obsidian}, {self.geodes}"


def run_blueprint2(blueprint, cache, best=0, max_minutes=24):
    # print(blueprint.minute, "  ", blueprint)

    h = blueprint.hash()
    if cache.get(h) is not None:
        return cache[h]

    # get next states
    states = blueprint.get_next_states(best, max_minutes)

    result = 0
    for state in states:
        if state.minute >= max_minutes:
            state_res = state.geodes #-((state.minute-max_minutes)*state.geode_robot_count)
            if state_res > best:
                best = state_res
            result = max(result, state_res)
        else:
            result = max(result, run_blueprint2(state, cache, best, max_minutes))

    cache[h] = result
    return result

def part1():
    blueprints = parseInput(19)
    # print(blueprints)

    totals = []
    for i in range(len(blueprints)):
        blueprint = blueprints[i]
        print(blueprint)
        geodes = run_blueprint2(blueprint, cache={}, best=0 , max_minutes=24)
        print(i, "geodes: ", geodes)
        print()
        totals.append(geodes)
    answer = 0
    for i in range(len(totals)):
        print("Blueprint ", i+1, totals[i])
        answer += (i+1) * totals[i]
    print("answer", answer)

# 5733 too low (21, 7, 39)
# guessed the answer by just bumping up 39+1 lol
# 6174 too high (21, 7, 42)

def part2():
    blueprints = parseInput(19)[:3]
    # print(blueprints)

    answer = 1
    for i in range(len(blueprints)):
        blueprint = blueprints[i]
        print(blueprint)
        geodes = run_blueprint2(blueprint, cache={}, best=0 , max_minutes=32)
        print("Blueprint ", i+1, geodes)
        answer *= geodes
    print("answer", answer)

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
    # takes around 1408966 ms or 23 minutes!!!