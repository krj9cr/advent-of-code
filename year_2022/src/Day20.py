import copy
import math
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [int(line.strip()) for line in file]
        return lines

# https://stackoverflow.com/questions/3883004/the-modulo-operation-on-negative-numbers-in-python
def newMod(a,b):
    res = a%b
    return res if not res else res-b if a<0 else res

def part1():
    lines = parseInput(20)
    print(lines)
    size = len(lines)

    original_lines = copy.deepcopy(lines)

    for num in original_lines:
        if num != 0:
            index = lines.index(num)
            new_index = index + num
            new_index = newMod(new_index, size)
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


# 20373 too high
# 5270 too high



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
