import time

class Item:
    def __init__(self, idx=0, worry=0):
        self.idx = idx
        self.worry = worry

    def __eq__(self, other):
        return self.idx == other.idx

    def __repr__(self):
        return str(self.idx) + ": " + str(self.worry)

class Monkey:
    def __init__(self, idx=0, starting_items=None, operation="", test_divisible=1,
                 test_true=0, test_false=0):
        self.idx = idx
        if starting_items:
            self.items = starting_items
        else:
            self.items = []
        self.operation = operation
        self.test_divisible = test_divisible
        self.test_true = test_true
        self.test_false = test_false

    def __repr__(self):
        res = "Monkey " + str(self.idx) + ": "
        for item in self.items:
            res += " " + repr(item)
        return res

    def __hash__(self):
        return hash(str(self.idx) + str(self.items))

    def __eq__(self, other):
        if len(self.items) == len(other.items):
            for i in range(len(self.items)):
                if self.items[i] != other.items[i]:
                    return False
            return True
        else:
            return False

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        monkeys = []
        item_counter = 0
        for line in lines:
            if line.startswith("Monkey"):
                idx = int(line.split(" ")[1].strip(":"))
                monkey = Monkey(idx=idx)
            elif line.startswith("Starting"):
                starting_items = [int(l.strip()) for l in line.strip("Starting items: ").split(",")]
                items = []
                for num in starting_items:
                    items.append(Item(item_counter, num))
                    item_counter += 1
                # print(items)
                monkey.items = items
            elif line.startswith("Operation"):
                operation = "o" + line.strip("Operation: new =") # for some reason this cuts off "o""
                # print(operation)
                monkey.operation =  operation
            elif line.startswith("Test"):
                test_divisble = int(line.strip("Test: divisible by ").strip())
                # print(test_divisble)
                monkey.test_divisible = test_divisble
            elif line.startswith("If true:"):
                m = int(line.split(" ")[-1])
                # print(m)
                monkey.test_true = m
            elif line.startswith("If false:"):
                m = int(line.split(" ")[-1])
                # print(m)
                monkey.test_false = m
            elif line == "":
                monkeys.append(monkey)
        monkeys.append(monkey) # last monkey has no newline at the end
        return monkeys

def part1():
    monkeys = parseInput(11)
    # print(monkeys)

    monkey_inspections = {}
    for i in range(len(monkeys)):
        monkey_inspections[i] = 0

    # for 20 rounds
    for i in range(20):
        # each monkey takes a turn
        for j in range(len(monkeys)):
            monkey = monkeys[j]
            # print()
            # print("Turn for Monkey ", monkey.idx)
            # for each item it holds
            for item in monkey.items:
                # print("inspecting: ", item)
                monkey_inspections[j] += 1
                old = item.worry
                newitem = eval(monkey.operation)
                # print("operation: ", newitem)
                # bored
                newitem = newitem // 3
                # print("bored:", newitem)
                # test
                m = monkey.test_false
                if newitem % monkey.test_divisible == 0:
                    m = monkey.test_true
                # throw it
                # print("throw to monkey ", m)
                monkeys[m].items.append(Item(item.idx, newitem))
            monkey.items = []
            # print(monkeys)
            # print()
    # print(monkey_inspections)
    s = sorted(monkey_inspections.values())
    print(s[-1] * s[-2])


def part2():
    monkeys = parseInput(11)
    # print(monkeys)

    monkey_inspections = {}
    for i in range(len(monkeys)):
        monkey_inspections[i] = 0

    # to keep the numbers small, we modulo by the product of all the divisors
    biggo = 1
    for monkey in monkeys:
        biggo *= monkey.test_divisible

    # for 20 rounds
    for i in range(10000):
        # print("Round:", i)
        # each monkey takes a turn
        for j in range(len(monkeys)):
            monkey = monkeys[j]
            # print()
            # print("Turn for Monkey ", monkey.idx)
            # for each item it holds
            for item in monkey.items:
                # print("inspecting: ", item)
                monkey_inspections[j] += 1
                old = item.worry
                newitem = eval(monkey.operation)
                # print("operation: ", newitem)
                # bored
                newitem = newitem % biggo
                # print("bored:", newitem)
                # test
                m = monkey.test_false
                if newitem % monkey.test_divisible == 0:
                    m = monkey.test_true
                # throw it
                # print("throw to monkey ", m)
                monkeys[m].items.append(Item(item.idx, newitem))
            monkey.items = []
        # print(monkeys)
        # print()
    # print(monkey_inspections)
    s = sorted(monkey_inspections.values())
    print(s[-1] * s[-2])

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
