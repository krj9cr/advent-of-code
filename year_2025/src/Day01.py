import time, os

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            direction = line[0]
            distance = int(line[1:])
            lines.append((direction, distance))
        return lines

def part1():
    lines = parseInput()
    print(lines)
    # because modulo works better between 1-num
    # rather than 0-num, +1 to the start and 99
    # so we treat it as 1-100 rather than 0-99
    curr_num = 51
    password = 0
    for direction, distance in lines:
        if direction == 'L':
            curr_num = curr_num - distance
        else:
            curr_num = curr_num + distance
        curr_num = (curr_num % 100)
        # check if at "1"
        print(direction, distance, "->", curr_num)
        if curr_num == 1:
            password += 1
    print(password)


def part2():
    lines = parseInput()
    print(lines)
    # because modulo works better between 1-num
    # rather than 0-num, +1 to the start and 99
    # so we treat it as 1-100 rather than 0-99
    curr_num = 51
    prev_num = None
    password = 0
    for direction, distance in lines:
        prev_num = curr_num
        print("curr_num", curr_num, "prev_num", curr_num)
        print(direction, distance)
        if direction == 'L':
            curr_num = curr_num - distance
        else:
            curr_num = curr_num + distance
        print("middle num:", curr_num)
        quotient, remainder = divmod(curr_num, 100)
        # quotient = abs(quotient)
        print("quotient", quotient, "remainder", remainder)
        # if curr_num < 0:
        #     if quotient == -1:
        #         password -= 1
        curr_num = remainder
        if curr_num == 0:
            curr_num = 100
        if prev_num == 1 and quotient < 0:
            password += abs(quotient) - 1
        elif quotient == 0 and curr_num == 1:
            password += 1
        else:
            password += abs(quotient)
        print("new num:", curr_num, "password:", password)
        print()
    print(password)

# 6065 too low
# 6149 too high
# 7047 too high

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
