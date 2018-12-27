import re
from copy import deepcopy


class Group:
    def __init__(self, index=0, army="", units=0, hp=0, attack_damage=0, attack_type="", initiative=0):
        self.index = index
        self.army = army
        self.units = units
        self.hp = hp
        self.attack_damage = attack_damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.weaknesses = set()
        self.immunities = set()
        self.effective_power = self.units * self.attack_damage

    def __str__(self):
        return "effective_power: " + str(self.effective_power) + " units: " + str(self.units) + " hp: " +\
               str(self.hp) + " attack_damage: " + str(self.attack_damage) +\
               " attack_type: " + self.attack_type + " weakness: " + str(self.weaknesses) +\
               " immunities: " + str(self.immunities) + " initiative: " + str(self.initiative)
        # return "Group " + str(self.index) + " contains " + str(self.units) + " units"


def parse_input(path: str):
    armies = {}
    with open(path, 'r') as file:
        current_type = ""
        current_army = {}
        count = 0
        for line in file:
            line = line.strip()
            if line == "Immune System:":
                current_type = "immune"
                current_army = {}
                count = 1
                continue
            elif line == "Infection:":
                # add immune
                armies[current_type] = current_army
                current_type = "infection"
                current_army = {}
                count = 1
                continue
            elif line == "":
                continue
            else:
                current_army[count] = parse_group(line, current_type, count)
            count += 1
        # add infection
        armies[current_type] = current_army
    return armies["immune"], armies["infection"]


def parse_group(line: str, currentType: str, index: int):
    pattern = re.compile(r"""(?P<units>[0-9]*) units each with (?P<hp>[0-9]*) hit points\s*(\((?P<weakness>weak to [\s,a-z,\,]+)*?;*\s*(?P<immunity>immune to [\s,a-z,\,]+)*?\))*\s*with an attack that does (?P<damage>[0-9]*) (?P<damageType>[a-z]*) damage at initiative (?P<initiative>[0-9]*)""")
    match = pattern.match(line)
    if match:
        units = int(match.group("units"))
        hp = int(match.group("hp"))
        weaknesses = match.group("weakness")
        immunities = match.group("immunity")
        attack_damage = int(match.group("damage"))
        attack_type = match.group("damageType")
        initiative = int(match.group("initiative"))

        g = Group(index, currentType, units, hp, attack_damage, attack_type, initiative)
        if weaknesses:
            weaknesses = weaknesses.replace("weak to ", "").split(", ")
            g.weaknesses = [w.strip() for w in weaknesses]
        if immunities:
            immunities = immunities.replace("immune to ", "").split(",")
            g.immunities = [i.strip() for i in immunities]
        return g


def target_selection(immune_system: dict, infection: dict):
    selections = {}  # map attacking_group -> (target_group, damage)

    # all groups are available to be targeted initially
    available_groups = list(immune_system.values()) + list(infection.values())

    # determine order for groups to perform target selection
    selection_order = deepcopy(available_groups)
    # sort by effective_power, then initiative, decreasing
    selection_order = sorted(selection_order, reverse=True, key=lambda x: (x.effective_power, x.initiative))

    for attacking_group in selection_order:
        possible_damage = []
        # calculate damage for each available group in the opposing army
        for target_group in available_groups:
            # groups must be in opposite armies
            if target_group.army != attacking_group.army:
                damage = calculate_damage(attacking_group, target_group)
                # some damage must be dealt
                if damage > 0:
                    possible_damage.append((target_group, damage))
        if len(possible_damage) > 0:
            # sort by damage, then effective_power, then initiative, decreasing
            possible_damage = sorted(possible_damage, reverse=True, key=lambda x: (x[1], x[0].effective_power, x[0].initiative))
            chosen_target = possible_damage[0]
            selections[attacking_group] = chosen_target
            available_groups.remove(chosen_target[0])

    # print info
    # for attacking_group in selections:
    #     target_group = selections[attacking_group][0]
    #     damage = selections[attacking_group][1]
    #     print(attacking_group.army + " group " + str(attacking_group.index) + " would deal defending group " +
    #           str(target_group.index) + " " + str(damage) + " damage")
    # print()

    return selections


def calculate_damage(attacking_group: Group, other_group: Group) -> int:
    if attacking_group.attack_type in other_group.immunities:
        return 0
    if attacking_group.attack_type in other_group.weaknesses:
        return attacking_group.effective_power * 2
    return attacking_group.effective_power


def take_damage(target_group: Group, damage: int):
    killed = min(int(damage / target_group.hp), target_group.units)
    target_group.units -= killed
    target_group.effective_power = target_group.units * target_group.attack_damage
    return killed


def attack(immune_system: dict, infection: dict, targets: dict):
    attack_order = list(targets.keys())
    # sort by initiative, decreasing
    attack_order = sorted(attack_order, reverse=True, key=lambda x: x.initiative)

    # attack
    for group in attack_order:
        if group.army == "immune":
            attacking_group = immune_system.get(group.index)
        else:
            attacking_group = infection.get(group.index)
        if attacking_group and targets[group] and attacking_group.units > 0:
            target_group, damage = targets[group]
            if target_group:
                if target_group.army == "immune":
                    target_group = immune_system[target_group.index]
                else:
                    target_group = infection[target_group.index]
                if target_group:
                    damage = calculate_damage(attacking_group, target_group)
                    killed = take_damage(target_group, damage)
                    # print(attacking_group.army + " group " + str(attacking_group.index) + " attacks defending group " +
                    #       str(target_group.index) + ", with " + str(damage) + " damage, killing " +
                    #       str(killed))
                    if target_group.units > 0:
                        if target_group.army == "immune":
                            immune_system[target_group.index] = target_group
                        else:
                            infection[target_group.index] = target_group
                    else:
                        if target_group.army == "immune":
                            del immune_system[target_group.index]
                        else:
                            del infection[target_group.index]
    # print()
    return immune_system, infection


def print_army(army):
    for group in army:
        print(army[group])
    print()


def print_armies(immune_system, infection):
    print("Immune System:")
    print_army(immune_system)
    print("Infection:")
    print_army(infection)


def fight(immune_system, infection):
    # print_armies(immune_system, infection)
    stalemate_iterations = 10000
    iteration = 0

    # fight until one side has no units left
    while len(immune_system) > 0 and len(infection) > 0:
        immune_system_size = len(immune_system)
        infection_size = len(infection)

        # print_armies(immune_system, infection)
        # target selection phase
        targets = target_selection(immune_system, infection)
        # attacking phase
        immune_system, infection = attack(immune_system, infection, targets)

        # detect stalemates
        new_immune_system_size = len(immune_system)
        new_infection_size = len(infection)
        # if sizes are unchanged
        if new_immune_system_size == immune_system_size and new_infection_size == infection_size:
            iteration += 1
            # print("iter", iteration)
            if iteration > stalemate_iterations:
                print("STALEMATE")
                break


def part1(path: str):
    immune_system, infection = parse_input(path)

    fight(immune_system, infection)

    # add up total remaining units
    total_units = 0
    for group in list(immune_system.values()) + list(infection.values()):
        total_units += group.units
    print("part1:", total_units)


def part2(path: str):
    immune_system, infection = parse_input(path)

    boost = 1
    while True:
        print(boost)
        # copy armies
        immune_system_test = deepcopy(immune_system)
        infection_test = deepcopy(infection)

        # boost immune system
        for i in immune_system_test:
            group = immune_system_test[i]
            group.attack_damage += boost
            group.effective_power = group.attack_damage * group.units

        # print_armies(immune_system_test, infection_test)

        # simulate fight
        fight(immune_system_test, infection_test)

        if len(infection_test) == 0 and len(immune_system_test) > 0:
            break
        boost += 1

    # done
    print_armies(immune_system_test, infection_test)

    # add up total remaining units
    total_units = 0
    for group in list(immune_system_test.values()) + list(infection_test.values()):
        total_units += group.units
    print("part2:", total_units)
