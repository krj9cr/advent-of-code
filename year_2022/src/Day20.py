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

def part1():
    items, size, zero_item = parseInput(20)
    # print(items)

    original_items = copy.copy(items)

    for item in original_items:
        if item.value == 0: # ignore 0 since it doesn't move
            continue
        index, new_index = get_new_index(item, items, size)
        old_item = items.pop(index)
        # print(lines)
        # print("moving num:", item.value, "to", new_index)
        items.insert(new_index, old_item)
        # print(items)
        # print()

    # find zero
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


# 20373 too high
# 5270 too high
# 5195 wrong


def part2():
    lines0 = parseInput(20)
    # print(lines)
    size = len(lines0)

    multiplier = 811589153
    lines = []
    for num in lines0:
        lines.append(num * multiplier)

    original_lines = copy.deepcopy(lines)

    for num in original_lines:
        if num != 0:
            index = lines.index(num)
            new_index = index + num
            math.rem
            if new_index < 0:
                while new_index < 0: # TODO: need euclidean remainder or else it's too slow
                    new_index = size + new_index - 1
            else:
                new_index = new_index % size
            del lines[index]
            # print(lines)
            # print("moving num:", num, "to", new_index)
            lines.insert(new_index, num)
        # print(lines)
        # print()

    # find zero
    zero_index = lines.index(0)
    first_index = (zero_index + 1000) % size
    second_index = (zero_index + 2000) % size
    third_index = (zero_index + 3000) % size

    # get
    first = lines[first_index]
    second = lines[second_index]
    third = lines[third_index]
    print("result:", first, second, third)
    print("answer:", first + second + third)


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
