import copy
import time
import portion as P

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

def negate_rule(rule):
    if "<" in rule:
        rule = rule.replace("<", ">=")
    elif ">" in rule:
        rule = rule.replace(">", "<=")
    return rule

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
            # if next_workflow_name == "A" and self.default == "A":  # we can ignore this
            #     continue
            rule = negate_rule(rule)
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
        da_chain = copy.deepcopy(rule_chain)
        for rule in workflow.rules:
            get_rule_chain(workflows, workflow.rules[rule], da_chain + [rule])
            da_chain.append(negate_rule(rule))
        # also take the default, after negating
        get_rule_chain(workflows, workflow.default, rule_chain + workflow.negated_rules())

minValue = 1
maxValue = 4000

# NOTE: returns inclusive ranges
def rule_to_interval(rule):
    if "<=" in rule:
        parts = rule.split("<=")
        variable = parts[0]
        value = int(parts[1])
        return variable, [minValue, value]
    elif ">=" in rule:
        parts = rule.split(">=")
        variable = parts[0]
        value = int(parts[1])
        return variable, [value, maxValue]
    elif "<" in rule:
        parts = rule.split("<")
        variable = parts[0]
        value = int(parts[1])
        return variable, [minValue, value - 1]
    elif ">" in rule:
        parts = rule.split(">")
        variable = parts[0]
        value = int(parts[1])
        return variable, [value + 1, maxValue]

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
    # print(workflows)
    get_rule_chain(workflows, nextWorkFlow, [])
    for chain in rule_chains:
        print(chain)

    # first set is ['s<1351', 'a<2006', 'x<1416']
    # x has 1416 possibilities or x>2662, which is 4000-2662 = 1338
    # m has 4000 possibilities
    # a has 2006 possibilities
    # s has 1351 possibilities
    # mult = 15350040384000
    # the problem is there are potentially overlapping possibilities in each rule chain

    # convert rule_chains to intervals? for each x, m, a, s variable
    interval_chains = []
    for rule_chain in rule_chains:
        intervals = {}
        for rule in rule_chain:
            variable, interval = rule_to_interval(rule)
            if variable in intervals:
                intervals[variable].append(interval)
            else:
                intervals[variable] = [interval]
        interval_chains.append(intervals)
        # print(rule_chain)
        # print(intervals)
        # print()
    # print(interval_chains)

    # try to "and" together intervals for each variable
    for interval_chain in interval_chains:
        for variable in interval_chain:
            intervals = interval_chain[variable]
            # print(intervals)
            # intersect the intervals until there's only one left
            final = P.open(intervals[0][0], intervals[0][1])
            if len(intervals) > 1:
                for i in range(1, len(intervals)):
                    interval = intervals[i]
                    p = P.open(interval[0], interval[1])
                    final = final.intersection(p)
            interval_chain[variable] = final
        # print(interval_chain)
        # print()

    # make sure each variable is represented?
    variables = ["x", "m", "a", "s"]
    for interval_chain in interval_chains:
        for variable in variables:
            if variable not in interval_chain:
                interval_chain[variable] = P.open(minValue, maxValue)
        # print(interval_chain)

    # try union-ing across chains?
    # base = interval_chains[0]
    # for i in range(1, len(interval_chains)):
    #     interval_chain = interval_chains[i]
    #     for variable in variables:
    #         p1 = base[variable]
    #         p2 = interval_chain[variable]
    #         p3 = p1.union(p2)
    #         base[variable] = p3
    # print(base)

    # let's just count up things to see where we're at
    s = 0
    for interval_chain in interval_chains:
        m = 1
        for variable in interval_chain:
            p = interval_chain[variable]
            m *= p.upper - p.lower + 1
        print(interval_chain, m)
        s += m
    print(s)

    # example answer
    # 167409079868000
    # 240695105228000 my answer

    # print(interval_chains)
    # merge any overlapping intervals: https://www.geeksforgeeks.org/merging-intervals/#
    # then add up the possibilities for x, m, a, s, individually
    # then multiply them together to get a count

    # promising? https://labix.org/doc/constraint/
    # problem = Problem()
    # problem.addVariables(["x", "m", "a", "s"], range(1, 4001))
    # problem.addConstraint(InSetConstraint(set(range(1, 1356))), ["s"])
    # problem.addConstraint(InSetConstraint(set(range(1, 2006+1))), ["a"])
    # problem.addConstraint(InSetConstraint(set(range(1, 1416+1))), ["x"])
    # solutions = problem.getSolutions()
    # print(solutions)
    # print(len(solutions))



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
