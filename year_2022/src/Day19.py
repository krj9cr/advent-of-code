import copy
import time

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
                 geode_robot_ore_cost, geode_robot_obsidian_cost):
        self.ore_robot_count = 1
        self.clay_robot_count = 0
        self.obsidian_robot_count = 0
        self.geode_robot_count = 0

        self.ore_robot_ore_cost = ore_robot_ore_cost
        self.clay_robot_ore_cost = clay_robot_ore_cost
        self.obsidian_robot_ore_cost = obsidian_robot_ore_cost
        self.obsidian_robot_clay_cost = obsidian_robot_clay_cost
        self.geode_robot_ore_cost = geode_robot_ore_cost
        self.geode_robot_obsidian_cost = geode_robot_obsidian_cost

        self.ore = 0
        self.clay = 0
        self.obsidian = 0
        self.geodes = 0

    def hash(self, minute):
        return f"{minute}: {self.ore_robot_count}, {self.clay_robot_count}, {self.obsidian_robot_count}, " \
               f"{self.geode_robot_count}. {self.ore}, {self.clay}, {self.obsidian}, {self.geodes}"

    def __repr__(self):
        return f"Blueprint robots: {self.ore_robot_count}, {self.clay_robot_count}, {self.obsidian_robot_count}, " \
               f"{self.geode_robot_count}. Costs: {self.ore_robot_ore_cost}, {self.clay_robot_ore_cost}, " \
               f"{self.obsidian_robot_ore_cost} + {self.obsidian_robot_clay_cost}, {self.geode_robot_ore_cost} + " \
               f"{self.geode_robot_obsidian_cost}. Resources: {self.ore}, {self.clay}, {self.obsidian}, {self.geodes}"


max_minutes = 24
cache =  {}

def run_blueprint(blueprint, minute):
    print(minute, "  ", blueprint)

    # check cache
    h = blueprint.hash(minute)
    if cache.get(h) is not None:
        return cache[h]
    if minute >= max_minutes:
        print("done, geodes:", blueprint.geodes)
        cache[h] = blueprint.geodes
        return blueprint.geodes

    minutes_left = max_minutes - minute

    next_blueprint = copy.deepcopy(blueprint)
    next_blueprint.ore += blueprint.ore_robot_count
    next_blueprint.clay += blueprint.clay_robot_count
    next_blueprint.obsidian += blueprint.obsidian_robot_count
    next_blueprint.geodes += blueprint.geode_robot_count

    # build geode if possible
    build_geode = 0
    if blueprint.ore >= blueprint.geode_robot_ore_cost \
        and blueprint.obsidian >= blueprint.geode_robot_obsidian_cost:
        geode_blueprint = copy.deepcopy(next_blueprint)
        geode_blueprint.geode_robot_count += 1
        geode_blueprint.ore -= blueprint.geode_robot_ore_cost
        geode_blueprint.obsidian -= blueprint.geode_robot_obsidian_cost
        # print(minute, "   making geode robot")
        build_geode = run_blueprint(geode_blueprint, minute + 1)
        return  build_geode # if you can build a geode node, don't consider other options

    # build obsidian
    build_obsidian = 0
    if blueprint.ore >= blueprint.obsidian_robot_ore_cost and \
        blueprint.clay >= blueprint.obsidian_robot_clay_cost and \
        (blueprint.obsidian_robot_count * minutes_left) + blueprint.obsidian < \
            minutes_left * blueprint.geode_robot_obsidian_cost:

        obsidian_blueprint = copy.deepcopy(next_blueprint)
        obsidian_blueprint.obsidian_robot_count += 1
        obsidian_blueprint.ore -= blueprint.obsidian_robot_ore_cost
        obsidian_blueprint.clay -= blueprint.obsidian_robot_clay_cost
        # print(minute, "    making obsidian robot")
        build_obsidian = run_blueprint(obsidian_blueprint, minute + 1)

    # build clay
    build_clay = 0
    if blueprint.ore >= blueprint.clay_robot_ore_cost and \
        (blueprint.clay_robot_count * minutes_left) + blueprint.clay < \
            minutes_left * blueprint.obsidian_robot_clay_cost:
        clay_blueprint = copy.deepcopy(next_blueprint)
        clay_blueprint.clay_robot_count += 1
        clay_blueprint.ore -= blueprint.clay_robot_ore_cost
        # print(minute, "    making clay robot")
        build_clay = run_blueprint(clay_blueprint, minute + 1)

    # build ore
    build_ore = 0
    if blueprint.ore >= blueprint.ore_robot_ore_cost and \
        (blueprint.ore_robot_count * minutes_left) + blueprint.ore  < \
        minutes_left * min(blueprint.clay_robot_ore_cost,  blueprint.obsidian_robot_ore_cost, blueprint.geode_robot_ore_cost):
        ore_blueprint = copy.deepcopy(next_blueprint)
        ore_blueprint.ore_robot_count += 1
        ore_blueprint.ore -= blueprint.ore_robot_ore_cost
        # print(minute, "    making ore robot")
        build_ore = run_blueprint(ore_blueprint, minute + 1)

    # try building noting
    # print(minute, "    nothing")
    nothing = run_blueprint(next_blueprint, minute + 1)

    print(minute, "  best", max(nothing, build_ore, build_clay, build_obsidian))
    return max(nothing, build_ore, build_clay, build_obsidian)



def part1():
    blueprints = parseInput(19)
    print(blueprints)


    for blueprint in blueprints:
        geodes = run_blueprint(blueprint, 1)
        print("Num geodes", blueprint.geodes)





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
