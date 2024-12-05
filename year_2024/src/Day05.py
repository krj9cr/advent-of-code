import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        # rules are kinda backwards
        # key is a page
        # values are all the pages that are supposed to come before it
        rules = {}
        updates = []
        processRules = True
        for line in file:
            line = line.strip()
            print(line)
            if line == "":
                processRules = False
                continue
            if processRules:
                linesplit = line.split("|")
                key = int(linesplit[1])
                value = int(linesplit[0])
                if rules.get(key):
                    rules[key].add(value)
                else:
                    rules[key] = set([value])
            else:
                linesplit = line.split(",")
                updates.append([int(item) for item in linesplit])
        return rules, updates

def part1():
    rules, updates = parseInput(5)
    print(rules)
    print(updates)

    # for each update
    update = updates[0]
    # keep list of seen pages
    seen = set()
    # for each item in update
    for item in update:
        print("ITEM", item)
        print("seen: ", seen)
        # check dict, have we seen any pages in the list? do they intersect?
        rulePages = rules.get(item)
        if rulePages:
            print("rulepages", rulePages)
            intersection = seen.intersection(rulePages)
            print("intersection", intersection)
            if len(intersection) > 0:
                # rule is violated
                break
            else:
                # rule is good, keep going
                seen.add(item)
                continue

def part2():
    lines = parseInput(5)
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
