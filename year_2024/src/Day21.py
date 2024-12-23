import functools
import sys
import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            lines.append(line)
        return lines

def get_directions(code, pad):
    directions = ""
    for i in range(len(code) - 1):
        c1 = code[i]
        c2 = code[i + 1]
        sub_directions = ""
        if c1 != c2:
            sub_directions = ''.join(pad[(c1, c2)])
        directions += sub_directions + "A"
    return directions

numeric_keypad = [
    [ '7',  '8',  '9'],
    [ '4',  '5',  '6'],
    [ '1',  '2',  '3'],
    [-1,  '0', 'A'],
]

directional_keypad = [
    [-1, '^', 'A'],
    ['<', 'v', '>']
]

num_pad = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
           '4': (0, 1), '5': (1, 1), '6': (2, 1),
           '1': (0, 2), '2': (1, 2), '3': (2, 2),
                        '0': (1, 3), 'A': (2, 3)}

dir_pad = {             '^': (1, 0), 'A': (2, 0),
           '<': (0, 1), 'v': (1, 1), '>': (2, 1)}

num_pad_directions = {
    ('7', '8'): ['>'], ('8', '7'): ['<'], ('7', '9'): ['>', '>'], ('9', '7'): ['<', '<'], ('7', '4'): ['v'],
    ('4', '7'): ['^'], ('7', '5'): ['v', '>'], ('5', '7'): ['<', '^'],
    ('7', '6'): ['v', '>', '>'], ('6', '7'): ['<', '<', '^'], ('7', '1'): ['v', 'v'], ('1', '7'): ['^', '^'],
    ('7', '2'): ['v', 'v', '>'], ('2', '7'): ['<', '^', '^'], ('7', '3'): ['v', 'v', '>', '>'],
    ('3', '7'): ['<', '<', '^', '^'],
    ('7', '0'): ['>', 'v', 'v', 'v'],
    ('0', '7'): ['^', '^', '^', '<'],
    ('7', 'A'): ['>', '>', 'v', 'v', 'v'],
    ('A', '7'): ['^', '^', '^', '<', '<'],
    ('8', '9'): ['>'], ('9', '8'): ['<'], ('8', '4'): ['<', 'v'], ('4', '8'): ['^', '>'], ('8', '5'): ['v'],
    ('5', '8'): ['^'], ('8', '6'): ['v', '>'], ('6', '8'): ['<', '^'],
    ('8', '1'): ['<', 'v', 'v'], ('1', '8'): ['^', '^', '>'], ('8', '2'): ['v', 'v'], ('2', '8'): ['^', '^'],
    ('8', '3'): ['v', 'v', '>'], ('3', '8'): ['<', '^', '^'], ('8', '0'): ['v', 'v', 'v'],
    ('0', '8'): ['^', '^', '^'], ('8', 'A'): ['v', 'v', 'v', '>'], ('A', '8'): ['<', '^', '^', '^'],
    ('9', '4'): ['<', '<', 'v'], ('4', '9'): ['^', '>', '>'], ('9', '5'): ['<', 'v'],
    ('5', '9'): ['^', '>'], ('9', '6'): ['v'], ('6', '9'): ['^'], ('9', '1'): ['<', '<', 'v', 'v'],
    ('1', '9'): ['^', '^', '>', '>'], ('9', '2'): ['<', 'v', 'v'], ('2', '9'): ['^', '^', '>'],
    ('9', '3'): ['v', 'v'], ('3', '9'): ['^', '^'], ('9', '0'): ['<', 'v', 'v', 'v'],
    ('0', '9'): ['^', '^', '^', '>'], ('9', 'A'): ['v', 'v', 'v'], ('A', '9'): ['^', '^', '^'], ('4', '5'): ['>'],
    ('5', '4'): ['<'], ('4', '6'): ['>', '>'], ('6', '4'): ['<', '<'], ('4', '1'): ['v'], ('1', '4'): ['^'],
    ('4', '2'): ['v', '>'], ('2', '4'): ['<', '^'], ('4', '3'): ['v', '>', '>'], ('3', '4'): ['<', '<', '^'],
    ('4', '0'): ['>', 'v', 'v'], ('0', '4'): ['^', '^', '<'], ('4', 'A'): ['v', 'v', '>', '>'],
    ('A', '4'): ['^', '^', '<', '<'], ('5', '6'): ['>'], ('6', '5'): ['<'], ('5', '1'): ['<', 'v'],
    ('1', '5'): ['^', '>'], ('5', '2'): ['v'], ('2', '5'): ['^'], ('5', '3'): ['v', '>'], ('3', '5'): ['<', '^'],
    ('5', '0'): ['v', 'v'], ('0', '5'): ['^', '^'], ('5', 'A'): ['v', 'v', '>'], ('A', '5'): ['^', '^', '<'],
    ('6', '1'): ['<', '<', 'v'], ('1', '6'): ['^', '>', '>'], ('6', '2'): ['<', 'v'], ('2', '6'): ['^', '>'],
    ('6', '3'): ['v'], ('3', '6'): ['^'], ('6', '0'): ['<', 'v', 'v'], ('0', '6'): ['^', '^', '>'],
    ('6', 'A'): ['v', 'v'], ('A', '6'): ['^', '^'], ('1', '2'): ['>'], ('2', '1'): ['<'], ('1', '3'): ['>', '>'],
    ('3', '1'): ['<', '<'], ('1', '0'): ['>', 'v'], ('0', '1'): ['^', '<'], ('1', 'A'): ['>', '>', 'v'],
    ('A', '1'): ['^', '<', '<'], ('2', '3'): ['>'], ('3', '2'): ['<'], ('2', '0'): ['v'], ('0', '2'): ['^'],
    ('2', 'A'): ['v', '>'], ('A', '2'): ['<', '^'], ('3', '0'): ['<', 'v'], ('0', '3'): ['^', '>'],
    ('3', 'A'): ['v'], ('A', '3'): ['^'], ('0', 'A'): ['>'], ('A', '0'): ['<']
}

dir_pad_directions = {
    ('^', 'A'): ['>'], ('A', '^'): ['<'],
    ('^', '<'): ['v', '<'],  # has to go this way
    ('<', '^'): ['>', '^'],  # has to go this way
    ('^', 'v'): ['v'], ('v', '^'): ['^'],
    ('^', '>'): ['v', '>'],
    ('>', '^'): ['<', '^'],
    ('A', '<'): ['v', '<', '<'],
    ('<', 'A'): ['>', '>', '^'],
    ('A', 'v'): ['<', 'v'],
    ('v', 'A'): ['^', '>'],
    ('A', '>'): ['v'], ('>', 'A'): ['^'], ('<', 'v'): ['>'], ('v', '<'): ['<'], ('<', '>'): ['>', '>'],
    ('>', '<'): ['<', '<'], ('v', '>'): ['>'], ('>', 'v'): ['<']
}

def part1():
    codes = parseInput(21)
    print(codes)

    # get all combinations and the best path between them
    # num_pad_directions = {}
    # for c1, c2 in itertools.combinations(num_pad.keys(), 2):
    #     print(c1, c2)
    #     path = find_path(num_pad, c1, c2)
    #     path2 = find_path(num_pad, c2, c1)
    #     print(path)
    #     num_pad_directions[(c1, c2)] = path
    #     num_pad_directions[(c2, c1)] = path2
    # print("num_pad_directions", num_pad_directions)


    # TODO: need to keep track of where robot arms end up after each time
    # initially they start at "A", but after that, it could end up wherever... orrr they always end up at A actually?

    total = 0
    for i in range(len(codes)):
        code = codes[i]
        # prepend A to the first code.. actually it always starts and ends at A
        # if i == 0:
        print("prepending A")
        code = "A" + code
        print("code", code)
        directions = get_directions(code, num_pad_directions)
        print("numeric pad", ''.join(directions))

        # if i == 0:
        # print("prepending A")
        directions = ["A"] + directions
        directions2 = get_directions(directions, dir_pad_directions)
        print("direction pad", ''.join(directions2))

        # if i == 0:
        # print("prepending A")
        directions2 = ["A"] + directions2
        directions3 = get_directions(directions2, dir_pad_directions)
        print("direction pad", ''.join(directions3))
        # print("answer", "       <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A")

        lengh_of_seq = len(directions3)
        numeric_code = code[:-1]
        # if i == 0:
        numeric_code = numeric_code[1:]
        numeric_code = int(numeric_code)
        print(lengh_of_seq, "*", numeric_code)
        print()
        total += lengh_of_seq * numeric_code

    print(total)
    print(memo)

memo = {}

'''
Here are all the counts for 029A all the way to 25: 
4, 12, 28, 68, 164, 404, 998, 2482, 6166, 15340, 38154, 94910, 236104, 587312, 1461046, 3634472, 9041286, 22491236, 55949852, 139182252, 346233228, 861298954, 2142588658, 5329959430, 13258941912, 32983284966, 82050061710 
'''

def try_again(directions):
    # if directions == "":
    #     return ""
    if memo.get(directions) is not None:
        # print("memo'd", directions, "=>", memo[directions])
        return memo[directions]
    if directions.count("A") <= 2:
        sub_directions = get_directions("A"+directions, dir_pad_directions)
        memo[directions] = sub_directions
        return sub_directions

    i = 0
    num_directions = len(directions)
    # split on the first A
    while i < num_directions:
        if directions[i] == "A":
            first = directions[:i+1]
            second = directions[i+1:]
            # print("splitting", first, second)
            first_directions = try_again(first)
            second_directions = try_again(second)

            # memoize?
            memo[first] = first_directions
            memo[second] = second_directions
            # print("memo'd", first, "=>", first_directions)
            # print("memo'd", second, "=>", second_directions)

            result = first_directions + second_directions
            memo[first+second] = result
            # print("memo'd", first+second, "=>", result)
            return result

        i += 1

    # memo[directions] = result
    # print("result", len(result), result)
    print("UH OH idk")
    sys.exit(1)
    # return result

def split_directions_in_half(directions):
    mid = len(directions) // 2
    # find the closest "A" and split on that
    while directions[mid] != "A":
        mid -= 1
    mid += 1
    first = directions[:mid]
    second = directions[mid:]
    if first == "" or second == "":
        if directions.count("A") == 2:
            substring = ""
            substrings = []
            for i in range(len(directions)):
                char = directions[i]
                substring += char
                if char == "A":
                    substrings.append(substring)
                    substring = ""
            return substrings
        else:
            print("UH OH, coudln't split", directions)
            sys.exit(1)

    return first, second

def try_again2(directions):
    if memo.get(directions) is not None:
        # print("memo'd", directions, "=>", memo[directions])
        return memo[directions]
    if directions.count("A") <= 2:
        sub_directions = get_directions("A"+directions, dir_pad_directions)
        memo[directions] = sub_directions
        return sub_directions

    # split in half
    first_half, second_half = split_directions_in_half(directions)
    # print("splitting", first_half, second_half)
    first_result = try_again2(first_half)
    second_result = try_again2(second_half)

    result = first_result + second_result
    if len(directions) <= 100000000:
        memo[first_half] = first_result
        memo[second_half] = second_result
        memo[directions] = result
    return result

def get_directions2(directions, level=2):
    if memo.get(directions) is not None:
        return memo[directions]
    # get the new directions
    new_directions = ""
    for i in range(len(directions) - 1):
        c1 = directions[i]
        c2 = directions[i + 1]
        sub_directions = ""
        if c1 != c2:
            sub_directions = ''.join(dir_pad_directions[(c1, c2)])
        new_directions += sub_directions + "A"
    print(level, len(new_directions))

    if level == 0:
        return len(new_directions)

    # recursive cost for this
    res = get_directions2(new_directions, level-1)
    memo[directions] = res
    return res

def part2():
    sys.setrecursionlimit(5000)
    codes = parseInput(21)

    total = 0
    for i in range(len(codes)):
        code = codes[i]
        # it always starts and ends at A
        code = "A" + code
        print("code", code)
        directions = get_directions(code, num_pad_directions)
        print("numeric pad", directions)

        # IDK
        directions = get_directions2(directions, 25)
        print("wow", directions)

        # OLD
        # for d in range(25):
        #     # memo_keys = list(memo.keys())
        #     # memo_keys.sort(key=lambda x: len(x))
        #     new_directions = try_again2(directions)
        #     print(d, len(new_directions))
        #     directions = new_directions
            # print(memo)

        # print(len(ya))

        # lengh_of_seq = len(ya)
        # numeric_code = int(code[1:-1])
        # print(lengh_of_seq, "*", numeric_code)
        # print()
        # total += lengh_of_seq * numeric_code

    print(total)

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
