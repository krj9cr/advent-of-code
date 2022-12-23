import copy
import math
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [int(line.strip()) for line in file]
        return lines

def part1():
    lines = parseInput(20)
    print(lines)
    size = len(lines)

    original_lines = copy.deepcopy(lines)

    for num in original_lines:
        if num != 0:
            index = lines.index(num) # if this is 1
            new_index = index + num # if this is -10, which is more then the size
            if new_index < 0:
                while new_index < 0:
                    new_index = size + new_index - 1
            else:
                new_index = new_index % size
            del lines[index]
            print(lines)
            print("moving num:", num, "to", new_index)
            lines.insert(new_index, num)
        print(lines)
        print()

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




def part2():
    lines = parseInput(20)
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
