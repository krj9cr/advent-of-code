import copy
import heapq
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
            split1 = line.split(".")
            print(split1)
            ore_robot_ore_cost = int(split1[0].split(" ")[-2])
            clay_robot_ore_cost = int(split1[1].split(" ")[-2])
            obsidian_robot_ore_cost = int(split1[2].split(" ")[5])
            obsidian_robot_clay_cost = int(split1[2].split(" ")[-2])
            geode_robot_ore_cost = int(split1[3].split(" ")[5])
            geode_robot_obsidian_cost = int(split1[3].split(" ")[-2])

            blueprints.append(Blueprint(ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost,
                                        obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost))
        return blueprints

class Blueprint:
    def __init__(self, ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost,
                 geode_robot_ore_cost, geode_robot_obsidian_cost, minute=0):
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

    def get_next_states(self, best):
        minutes_left = max_minutes - self.minute + 1

        # check if we should just stop
        # if we hypothetically created a geode bot every remaining minute and are still less than best
        best_geodes = self.geodes
        for i in range(minutes_left+1):
            best_geodes += self.geode_robot_count + i
        if best_geodes < best:
            return []

        states = []
        # build geode
        if self.obsidian_robot_count > 0:
            ore_minutes_from_now = math.ceil((self.geode_robot_ore_cost - self.ore) / self.ore_robot_count)
            obsidian_minutes_from_now = math.ceil((self.geode_robot_obsidian_cost - self.obsidian) / self.obsidian_robot_count)
            minutes_from_now = max(ore_minutes_from_now, obsidian_minutes_from_now, 0)
            next_state = copy.deepcopy(self)
            next_state.collect(minutes_from_now)
            if minutes_from_now <= minutes_left:
                next_state.build_robot(3)
            next_state.minute += minutes_from_now
            states.append(next_state)
            return states

        # build obsidian
        if self.clay_robot_count > 0 and self.obsidian_robot_count < self.max_obsidian_bots:
            ore_minutes_from_now = math.ceil((self.obsidian_robot_ore_cost - self.ore) / self.ore_robot_count)
            clay_minutes_from_now = math.ceil((self.obsidian_robot_clay_cost - self.clay) / self.clay_robot_count)
            minutes_from_now = max(ore_minutes_from_now, clay_minutes_from_now, 0)
            # minutes_from_now = min(minutes_left, minutes_from_now)
            next_state = copy.deepcopy(self)
            next_state.collect(minutes_from_now)
            if minutes_from_now <= minutes_left:
                next_state.build_robot(2)
            next_state.minute += minutes_from_now
            states.append(next_state)

        # build clay
        if self.clay_robot_count < self.max_clay_bots:
            minutes_from_now = math.ceil((self.clay_robot_ore_cost - self.ore) / self.ore_robot_count)
            minutes_from_now = max(minutes_from_now, 0)
            # minutes_from_now = min(minutes_left, minutes_from_now)
            next_state = copy.deepcopy(self)
            next_state.collect(minutes_from_now)
            if minutes_from_now <= minutes_left:
                next_state.build_robot(1)
            next_state.minute += minutes_from_now
            states.append(next_state)

        # build ore
        if self.ore_robot_count < self.max_ore_bots:
            minutes_from_now = math.ceil((self.ore_robot_ore_cost - self.ore) / self.ore_robot_count)
            minutes_from_now = max(minutes_from_now, 0)
            # minutes_from_now = min(minutes_left, minutes_from_now)
            next_state = copy.deepcopy(self)
            next_state.collect(minutes_from_now)
            next_state.build_robot(0)
            if minutes_from_now <= minutes_left:
                next_state.minute += minutes_from_now
            states.append(next_state)

        return states

    def can_build_robots(self):
        build_ore = False
        build_clay = False
        build_obsidian = False
        build_geode = False
        if self.ore >= self.ore_robot_ore_cost:
            build_ore = True
        if self.ore >= self.clay_robot_ore_cost:
            build_clay = True
        if self.ore >= self.obsidian_robot_ore_cost and self.clay >= self.obsidian_robot_clay_cost:
            build_obsidian = True
        if self.ore >= self.geode_robot_ore_cost and self.obsidian >= self.geode_robot_obsidian_cost:
            build_geode = True
        return build_ore, build_clay, build_obsidian, build_geode

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


max_minutes = 24
# cache =  {}

def run_blueprint2(blueprint, cache, best=0):
    print(blueprint.minute, "  ", blueprint)

    h = blueprint.hash()
    if cache.get(h) is not None:
        return cache[h]
    # get next states
    states = blueprint.get_next_states(best)

    results = [0]
    for state in states:
        if state.minute >= max_minutes:
            print("done, geodes:", state.geodes)
            if state.geodes > best:
                best = state.geodes
            results.append(state.geodes)
        else:
            results.append(run_blueprint2(state, cache, best))

    res = max(results)
    cache[h] = res
    return res

def run_blueprint(blueprint, minute):
    print(minute, "  ", blueprint)

    if minute >= max_minutes:
        print("done, geodes:", blueprint.geodes)
        return blueprint.geodes

    minutes_left = max_minutes - minute + 1

    # build a geode robot
    build_geode = 0
    # always try to build it
    if blueprint.ore >= blueprint.geode_robot_ore_cost and \
            blueprint.obsidian >= blueprint.geode_robot_obsidian_cost:
        geode_blueprint = copy.deepcopy(blueprint)
        geode_blueprint.ore -= blueprint.geode_robot_ore_cost
        geode_blueprint.obsidian -= blueprint.geode_robot_obsidian_cost

        geode_blueprint.ore += blueprint.ore_robot_count
        geode_blueprint.clay += blueprint.clay_robot_count
        geode_blueprint.obsidian += blueprint.obsidian_robot_count
        geode_blueprint.geodes += blueprint.geode_robot_count

        geode_blueprint.geode_robot_count += 1
        build_geode = run_blueprint(geode_blueprint, minute + 1)
    elif blueprint.obsidian_robot_count > 0: # we need at least one obsidian robot
        ore_minutes_from_now = math.ceil((blueprint.geode_robot_ore_cost - blueprint.ore) / blueprint.ore_robot_count)
        obsidian_minutes_from_now = math.ceil((blueprint.geode_robot_obsidian_cost - blueprint.obsidian) / blueprint.obsidian_robot_count)
        # minutes_from_now = max(blueprint.geode_robot_ore_cost - blueprint.ore, blueprint.geode_robot_obsidian_cost - blueprint.obsidian)
        minutes_from_now = max(ore_minutes_from_now, obsidian_minutes_from_now)
        if minute + minutes_from_now <= max_minutes:
            geode_blueprint = copy.deepcopy(blueprint)
            geode_blueprint.ore += blueprint.ore_robot_count * (minutes_from_now+1)
            geode_blueprint.clay += blueprint.clay_robot_count * (minutes_from_now+1)
            geode_blueprint.obsidian += blueprint.obsidian_robot_count * (minutes_from_now+1)
            geode_blueprint.geodes += blueprint.geode_robot_count * (minutes_from_now+1)

            geode_blueprint.ore -= blueprint.geode_robot_ore_cost
            geode_blueprint.obsidian -= blueprint.geode_robot_obsidian_cost
            geode_blueprint.geode_robot_count += 1
            build_geode = run_blueprint(geode_blueprint, minute + (minutes_from_now+1))
        # else: # TODO: just go to the end??
        #     build_geode = blueprint.geodes + (blueprint.geode_robot_count * minutes_left)

    # don't try making any other robots (may not be accurate, but will speed things up)
    # if build_geode > 0:
    #     print("stopping geodes: ", build_geode)
    #     return build_geode

    # branch for when we can build each robot next
    # build an ore robot
    build_ore = 0
    if blueprint.ore_robot_count * minutes_left + blueprint.ore < \
            minutes_left * max(blueprint.clay_robot_ore_cost,  # TODO: max or min, here?
                               blueprint.obsidian_robot_ore_cost, blueprint.geode_robot_ore_cost):
        if blueprint.ore >= blueprint.ore_robot_ore_cost:
            ore_blueprint = copy.deepcopy(blueprint)
            ore_blueprint.ore -= ore_blueprint.ore_robot_ore_cost

            ore_blueprint.ore += blueprint.ore_robot_count
            ore_blueprint.clay += blueprint.clay_robot_count
            ore_blueprint.obsidian += blueprint.obsidian_robot_count
            ore_blueprint.geodes += blueprint.geode_robot_count

            ore_blueprint.ore_robot_count += 1
            build_ore = run_blueprint(ore_blueprint, minute + 1)
        else:
            # ore_robot_ore_cost = 4
            # 2 ore robots
            # 1 ore
            # minutes from now should be 2
            # 2 = (4 - 1) / ore robots
            # ore + (ore_robots * minutes_from_now) >= cost
            #  (ore_robots * minutes_from_now) >= cost - ore
            # minutes_from_now >= (cost - ore) / ore_robots
            minutes_from_now = math.ceil((blueprint.ore_robot_ore_cost - blueprint.ore) / blueprint.ore_robot_count)
            # minutes_from_now = blueprint.ore_robot_ore_cost - blueprint.ore
            if minute + minutes_from_now <= max_minutes:
                ore_blueprint = copy.deepcopy(blueprint)

                ore_blueprint.ore += blueprint.ore_robot_count * (minutes_from_now+1)
                ore_blueprint.clay += blueprint.clay_robot_count * (minutes_from_now+1)
                ore_blueprint.obsidian += blueprint.obsidian_robot_count * (minutes_from_now+1)
                ore_blueprint.geodes += blueprint.geode_robot_count * (minutes_from_now+1)

                ore_blueprint.ore -= blueprint.ore_robot_ore_cost
                ore_blueprint.ore_robot_count += 1
                build_ore = run_blueprint(ore_blueprint, minute + (minutes_from_now+1))

    # build a clay robot
    build_clay = 0
    if blueprint.clay_robot_count * minutes_left + blueprint.clay < \
            minutes_left * blueprint.obsidian_robot_clay_cost:
        if blueprint.ore >= blueprint.clay_robot_ore_cost:
            clay_blueprint = copy.deepcopy(blueprint)
            clay_blueprint.ore -= clay_blueprint.clay_robot_ore_cost

            clay_blueprint.ore += blueprint.ore_robot_count
            clay_blueprint.clay += blueprint.clay_robot_count
            clay_blueprint.obsidian += blueprint.obsidian_robot_count
            clay_blueprint.geodes += blueprint.geode_robot_count

            clay_blueprint.clay_robot_count += 1
            build_clay = run_blueprint(clay_blueprint, minute + 1)
        else:
            minutes_from_now = math.ceil((blueprint.clay_robot_ore_cost - blueprint.ore) / blueprint.ore_robot_count)
            # minutes_from_now = blueprint.clay_robot_ore_cost - blueprint.ore
            if minute + minutes_from_now <= max_minutes:
                clay_blueprint = copy.deepcopy(blueprint)

                clay_blueprint.ore += blueprint.ore_robot_count * (minutes_from_now+1)
                clay_blueprint.clay += blueprint.clay_robot_count * (minutes_from_now+1)
                clay_blueprint.obsidian += blueprint.obsidian_robot_count * (minutes_from_now+1)
                clay_blueprint.geodes += blueprint.geode_robot_count * (minutes_from_now+1)

                clay_blueprint.ore -= blueprint.clay_robot_ore_cost
                clay_blueprint.clay_robot_count += 1
                build_clay = run_blueprint(clay_blueprint, minute + minutes_from_now+1)


    # build an obsidian robot
    build_obsidian = 0
    if blueprint.obsidian_robot_count * minutes_left + blueprint.obsidian < \
            minutes_left * blueprint.geode_robot_obsidian_cost:
        if blueprint.ore >= blueprint.obsidian_robot_ore_cost and \
                blueprint.clay >= blueprint.obsidian_robot_clay_cost:
            obsidian_blueprint = copy.deepcopy(blueprint)
            obsidian_blueprint.ore -= blueprint.obsidian_robot_ore_cost
            obsidian_blueprint.clay -= blueprint.obsidian_robot_clay_cost

            obsidian_blueprint.ore += blueprint.ore_robot_count
            obsidian_blueprint.clay += blueprint.clay_robot_count
            obsidian_blueprint.obsidian += blueprint.obsidian_robot_count
            obsidian_blueprint.geodes += blueprint.geode_robot_count

            obsidian_blueprint.obsidian_robot_count += 1
            build_obsidian = run_blueprint(obsidian_blueprint, minute + 1)
        elif blueprint.clay_robot_count > 0:  # we need at least one clay robot to jump ahead

            ore_minutes_from_now = math.ceil(
                (blueprint.geode_robot_ore_cost - blueprint.ore) / blueprint.ore_robot_count)
            clay_minutes_from_now = math.ceil(
                (blueprint.obsidian_robot_clay_cost - blueprint.clay) / blueprint.clay_robot_count)
            minutes_from_now = max(ore_minutes_from_now, clay_minutes_from_now)
            # minutes_from_now = max(blueprint.obsidian_robot_ore_cost - blueprint.ore, blueprint.obsidian_robot_clay_cost - blueprint.clay)
            if minute + minutes_from_now <= max_minutes:
                obsidian_blueprint = copy.deepcopy(blueprint)

                obsidian_blueprint.ore += blueprint.ore_robot_count * (minutes_from_now+1)
                obsidian_blueprint.clay += blueprint.clay_robot_count * (minutes_from_now+1)
                obsidian_blueprint.obsidian += blueprint.obsidian_robot_count * (minutes_from_now+1)
                obsidian_blueprint.geodes += blueprint.geode_robot_count * (minutes_from_now+1)

                obsidian_blueprint.ore -= blueprint.obsidian_robot_ore_cost
                obsidian_blueprint.clay -= blueprint.obsidian_robot_clay_cost
                obsidian_blueprint.obsidian_robot_count += 1
                build_obsidian = run_blueprint(obsidian_blueprint, minute + (minutes_from_now+1))


    # print(minute, "  best", max(nothing, build_ore, build_clay, build_obsidian))
    # print("max of :", build_ore, build_clay, build_obsidian, build_geode)
    return max(build_ore, build_clay, build_obsidian, build_geode)


def part1():
    blueprints = parseInput(19)
    # print(blueprints)

    totals = []
    for i in range(len(blueprints)):
        blueprint = blueprints[i]
        print(blueprint)
        geodes = run_blueprint2(blueprint, {}, 0)
        print(i, "geodes: ", geodes)
        print()
        totals.append(geodes)
    answer = 0
    for i in range(len(totals)):
        print("Blueprint ", i+1, totals[i])
        answer += (i+1) * totals[i]
    print("answer", answer)





def part2():
    lines = parseInput(19)
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
