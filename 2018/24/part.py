

class Group:
    def __init__(self, u=0, h=0, ad=0, at="", i=0):
        self.units = u
        self.hp = h
        self.attack_damage = ad
        self.attack_type = at
        self.initiative = i
        self.weaknesses = set()
        self.immunities = set()
        self.effective_power = self.units * self.attack_damage


def parseInput(path: str):
    armies = {}
    with open(path, 'r') as file:
        currentType = ""
        currentArmy = []
        for line in file:
            line = line.strip()
            if line == "Immune System:":
                currentType = "immune"
                currentArmy = []
                continue
            elif line == "Infection:":
                # add immune
                armies[currentType] = currentArmy
                currentType = "infection"
                currentArmy = []
                continue
            elif line == "":
                continue
            else:
                currentArmy.append(parseGroup(line))
        # add infection
        armies[currentType] = currentArmy


def parseGroup(line: str):
    # 17 units each with
    # 5390 hit points
    # (weak to radiation, bludgeoning)
    # with an attack that does 4507 fire damage
    # at initiative 2
    return line.strip()


def part1(path: str):
    lines = parseInput(path)
    print(lines)


def part2(path: str):
    lines = parseInput(path)
    print(lines)
