import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        pairs = []
        pair = []
        for line in lines:
            if line == "":
                pairs.append(pair)
                pair = []
            else:
                l = eval(line)
                pair.append(l)
        pairs.append(pair) # last pair has no blank line
        return pairs

# def compare(left, right, orig_left, orig_right):
#     print("comparing:", left, right)
#     if isinstance(left, int):
#         if isinstance(right, int):
#             if left <= right:
#                 return True
#             else:
#                 print("Fail on ", left, right)
#                 return False
#         else:
#             return compare([left], right, orig_left, orig_right)
#     else: # left is a list
#         if isinstance(right, int):
#             return compare(left, [right], orig_left, orig_right)
#         else: # both are lists
#             left_size = len(left)
#             right_size = len(right)
#             if left_size < right_size: # compare all nums
#                 all_good = False
#                 for i in range(left_size):
#                     all_good = compare(left[i], right[i], orig_left, orig_right)
#                     if all_good:
#                         return True
#                 return all_good
#             else: # right side has more items
#                 # TODO: compare still, but check which list runs out of items, first
#                 all_good = False
#                 for i in range(right_size):
#                     all_good = compare(left[i], right[i], orig_left, orig_right)
#                     if all_good:
#                         return True
#                 return all_good

def compare_lists(left, right):
    left_size = len(left)
    right_size = len(right)
    for i in range(left_size):
        if i >= right_size:
            print("Right ran out of items")
            return False
        left_item = left[i]
        right_item = right[i]
        print("trying to ", left_item, right_item)
        res = compare(left_item, right_item)
        if res is None:
            continue
        if res:
            return True
        else:
            return False
    print("Ran out of items")
    if left_size < right_size:
        return True
    elif left_size == right_size:
        return None
    return False

def compare(left, right):
    if isinstance(left, int):
        if isinstance(right, int):
            if left < right:
                return True
            elif left == right:
                return None
            else:
                print("fail on ", left, right)
                return False
        else:  # right is a list
            return compare_lists([left], right)
    elif isinstance(left, list): # left is a list
        if isinstance(right, int):
            return compare_lists(left, [right])
        else:  # both are lists
            return compare_lists(left, right)




def part1():
    pairs = parseInput(13)
    # print(lines)
    total = 0
    for i in range(len(pairs)):
        pair = pairs[i]
        left = pair[0]
        right = pair[1]
        print("Pair ", i+1)
        print("Comparing: ", left, "  vs  ",  right)
        res = compare(left, right)
        print(res)
        print()
        if res:
            total += i + 1
    print(total)


def part2():
    lines = parseInput(13)
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
