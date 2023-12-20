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

    def negated_rules(self):
        rules = []
        for rule in self.rules:
            next_workflow_name = self.rules[rule]
            if next_workflow_name == "A" and self.default == "A":  # we can ignore this
                continue
            if "<" in rule:
                rule = rule.replace("<", ">=")
            elif ">" in rule:
                rule = rule.replace(">", "<=")
            rules.append(rule)
        return rules

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

rule_chains = []

def get_rule_chain(workflows, workflow_name, rule_chain):
    # print(workflow_name)
    if workflow_name == "A":
        rule_chains.append(rule_chain)
    elif workflow_name == "R":
        return  # do nothing
    else:
        workflow = workflows[workflow_name]
        for rule in workflow.rules:
            get_rule_chain(workflows, workflow.rules[rule], rule_chain + [rule])
        # also take the default, after negating
        get_rule_chain(workflows, workflow.default, rule_chain + workflow.negated_rules())

def part2():
    workflows, _ = parseInput(19)

    # what is the total?
    # 4 possible numbers of 1 to 4000
    # 4000^4 = 2.56e+14 = 2.45 * 10^14 = 256,000,000,000,000

    # 256000000000000 - 167409079868000 = 88590920000000

    # just to compare
    # 256000000000000
    # 167409079868000
    #  88590920000000
    #

    # start with "in"
    # follow each path "recursively", "and"-ing the conditions
    # if we end in "A", keep that as a constraint
    # if we end in "R", throw it out
    # then we have a big set of constraints... and need to do maths

    nextWorkFlow = "in"
    get_rule_chain(workflows, nextWorkFlow, [])
    print(rule_chains)

    # first set is ['s<1351', 'a<2006', 'x<1416']
    # x has 1416 possibilites or x>2662, which is 4000-2662 = 1338
    # m has 4000 possibilities
    # a has 2006 possibilities
    # s has 1351 possibilities
    # mult = 15350040384000

    # promising? https://labix.org/doc/constraint/
    from constraint import *
    problem = Problem()
    problem.addVariables(["x", "m", "a", "s"], range(1, 4001))
    problem.addConstraint(InSetConstraint(set(range(1, 1356))), ["s"])


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
