import time

class Part:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __str__(self):
        return "{{x={x},m={m},a={a},s={s}}}".format(x=self.x, m=self.m, a=self.a, s=self.s)

    def sum(self):
        return self.x + self.m + self.a + self.s

class Workflow:
    def __init__(self, name, rules, default):
        self.name = name
        self.rules = rules  # a dict?
        self.default = default

    def __str__(self):
        return self.name + "{" + str(self.rules) + "," + self.default + "}"

    def check_rules(self, part: Part):
        x = part.x
        m = part.m
        a = part.a
        s = part.s
        for rule in self.rules:
            if eval(rule):
                return self.rules[rule]
        return self.default

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        workflows = {}
        parts = []
        processingWorkflows = True
        for line in file:
            line = line.strip()
            # workflows change to parts
            if line == "":
                processingWorkflows = False
                continue
            if processingWorkflows:
                s = line.split("{")
                name = s[0]
                rules = s[1].strip("}").split(",")
                default = rules.pop()
                rulesDict = {}
                for rule in rules:
                    rule = rule.split(":")
                    rulesDict[rule[0]] = rule[1]
                # print(name, rules, default)
                workflows[name] = Workflow(name, rulesDict, default)
            else:
                line = line.strip("{").strip("}")
                line = line.split(",")
                args = [int(item[2:]) for item in line]
                parts.append(Part(args[0], args[1], args[2], args[3]))

        return workflows, parts

def part1():
    workflows, parts = parseInput(19)
    answer = 0
    for part in parts:
        # print(part)
        nextWorkFlow = "in"
        while True:
            workflow = workflows[nextWorkFlow]
            nextWorkFlow = workflow.check_rules(part)
            if nextWorkFlow == "A":
                result = part.sum()
                # print(result)
                answer += result
                break
            elif nextWorkFlow == "R":
                break
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
