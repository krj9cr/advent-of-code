import copy
import math
import time

# this helps deal with duplicate values
class Item:
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return str(self.value)

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [int(line.strip()) for line in file]
        size = len(lines)
        items = []
        zero_item = None
        for i in range(size):
            item = Item(lines[i], i)
            if item.value == 0:
                zero_item = item
            items.append(item)
        return items, size, zero_item

def get_new_index(item, sequence, size):
    index = sequence.index(item)
    new_index = index + item.value
    new_index = new_index % (size - 1)
    return index, new_index

def mix(original_items, items, size):
    for item in original_items:
        if item.value == 0: # ignore 0 since it doesn't move
            continue
        index, new_index = get_new_index(item, items, size)
        old_item = items.pop(index)
        items.insert(new_index, old_item)

def find_answer(items, size, zero_item):
    zero_index = items.index(zero_item)
    first_index = (zero_index + 1000) % size
    second_index = (zero_index + 2000) % size
    third_index = (zero_index + 3000) % size

    # get
    first = items[first_index].value
    second = items[second_index].value
    third = items[third_index].value
    print("result:", first, second, third)
    print("answer:", first + second + third)


def part1():
    items, size, zero_item = parseInput(20)
    original_items = copy.copy(items)
    mix(original_items, items, size)
    find_answer(items, size, zero_item)

def part2():
    items, size, zero_item = parseInput(20)

    multiplier = 811589153
    for item in items:
        item.value = item.value * multiplier
    # print(items)
    original_items = copy.copy(items)

    for i in range(10):
        mix(original_items, items, size)

    find_answer(items, size, zero_item)





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
