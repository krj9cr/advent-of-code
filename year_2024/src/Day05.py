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
            # print(line)
            if line == "":
                processRules = False
                continue
            if processRules:
                linesplit = line.split("|")
                key = int(linesplit[0])
                value = int(linesplit[1])
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
    # print(rules)
    # print(updates)

    good = []
    # for each update
    for update in updates:
        # keep list of seen pages
        seen = set()
        violated = False
        # for each item in update
        for item in update:
            # print("ITEM", item)
            seen.add(item)
            # print("seen: ", seen)
            # check dict, have we seen any pages in the list? do they intersect?
            rulePages = rules.get(item)
            if rulePages:
                # print("rulepages", rulePages)
                intersection = seen.intersection(rulePages)
                # print("intersection", intersection)
                if len(intersection) > 0:
                    # rule is violated
                    # print("VIOLATED")
                    violated = True
                    break
                else:
                    # rule is good, keep going
                    continue
        if not violated:
            middleIndex = int((len(update) - 1) / 2)
            good.append(update[middleIndex])
            # print("GOOD TO GO")
    # print(good)
    print(sum(good))

def checkUpdate(update, rules):
    # keep list of seen pages
    seen = set()
    # for each item in update
    for item in update:
        seen.add(item)
        # check dict, have we seen any pages in the list? do they intersect?
        rulePages = rules.get(item)
        if rulePages:
            intersection = seen.intersection(rulePages)
            if len(intersection) > 0:
                # rule is violated on this item (could be multiple items...)
                return False
            else:
                # rule is good, keep going
                continue
    return True

def fixFirstItem(update, rules):
    newUpdate = update[:]
    # keep list of seen pages
    seen = set()
    # for each item in update
    for i in range(0, len(update)):
        item = update[i]
        seen.add(item)
        # check dict, have we seen any pages in the list? do they intersect?
        rulePages = rules.get(item)
        if rulePages:
            intersection = seen.intersection(rulePages)
            if len(intersection) > 0:
                # print("BAD ITEM", item)
                # move it back one
                sliced = update[:i+1]
                # print(sliced)
                sliced[-1], sliced[-2] = sliced[-2], sliced[-1]
                # print(sliced)
                intermediateUpdate = sliced + update[i+1:]
                # print(intermediateUpdate)
                return intermediateUpdate
    print("NOTHING WAS WRONG???")
    return update

def part2():
    rules, updates = parseInput(5)
    # find bad updates
    bad = []
    for update in updates:
        update_good = checkUpdate(update, rules)
        if not update_good:
            bad.append(update)
    # print(bad)
    good = []
    # try to fix the updates
    for update in bad:
        newUpdate = update[:]
        while True:
            # find the first item in error
            newUpdate = fixFirstItem(newUpdate, rules)
            # print(newUpdate)
            # check if this passes
            is_good = checkUpdate(newUpdate, rules)
            if is_good:
                good.append(newUpdate)
                break
            # repeat the process for the rest of the list
    # print(good)
    total = 0
    for update in good:
        middleIndex = int((len(update) - 1) / 2)
        total += update[middleIndex]
    print(total)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
