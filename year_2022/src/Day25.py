import math
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

# https://www.codespeedy.com/inter-convert-decimal-and-any-base-using-python/
def dec_to_base(num, base):  # Maximum base - 36
    base_num = ""
    while num>0:
        dig = int(num % base)
        if dig<10:
            base_num += str(dig)
        else:
            base_num += chr(ord('A')+dig-10)  # Using uppercase letters
        num //= base
    base_num = base_num[::-1]  # To reverse the string
    return base_num

def decimal_to_snafu(decimal_num):
    base_five = dec_to_base(decimal_num, 5)
    # print("base five", base_five)
    rev = [char for char in base_five[::-1]]
    snafu_num = ""
    i = 0
    while i < len(rev):
        place = int(rev[i])
        # print("i", i, "place", place)
        if place > 2:
            new_place = place - 5
            # print("newplace", new_place)
            if new_place == -1:
                snafu_num += "-"
            elif new_place == -2:
                snafu_num += "="
            else:
                snafu_num += str(new_place)
            # carry over to the next place, or add a place
            if i + 1 >= len(rev):
                snafu_num += "1"
            else:
                rev[i+1] = str(int(rev[i+1]) + 1)
        else:
            snafu_num += str(place)
        i += 1

    return snafu_num[::-1]

def snafu_to_decimal(snafu_num):
    total = 0
    # assume snafu num is most sig digit to least sig, so we flip it
    rev = snafu_num[::-1]
    for i in range(len(rev)):
        place = rev[i]
        if place == "=":
            place = -2
        elif place == "-":
            place = -1
        else:
            place = int(place)
        total += place * math.pow(5, i)
    return total

def part1():
    lines = parseInput(25)
    # print(lines)

    total = 0
    for snafu in lines:
        total += snafu_to_decimal(snafu)
    print("decimal total:", total)
    print("snafu total:", decimal_to_snafu(total))


def part2():
    lines = parseInput(25)
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
