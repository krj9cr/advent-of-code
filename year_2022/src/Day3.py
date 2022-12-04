
def parseInput(day):
    path = __file__.rstrip(f"Day{day}.py") + f"../input/day{day}.txt"
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

def part1():
    lines = parseInput(3)
    print(lines)
    letters = []
    for line in lines:
        half = len(line) // 2
        # print("half: ", half)
        first = line[:half]
        second = line[half:]
        for char in first:
            if char in second:
                letters.append(char)
                break
    score = 0
    for letter in letters:
        if letter.islower():
            o = ord(letter) - 96
            score += o
            print(letter, o)
        else:
            o = ord(letter) - 64 + 27 - 1
            score += o
            print(letter, o)

    print(score)

def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def part2():
    lines = parseInput(3)
    groups = divide_chunks(lines, 3)
    # print(lines)
    letters = []
    for group in groups:
        print(group)
        common = None
        for line in group:
            for char in line:
                in_all = True
                for line2 in group:
                    if line != line2 and char not in line2:
                        in_all = False
                        break
                if in_all:
                    common = char
                    break
            if common:
                break
        letters.append(common)

    score = 0
    for letter in letters:
        if letter.islower():
            o = ord(letter) - 96
            score += o
            print(letter, o)
        else:
            o = ord(letter) - 64 + 27 - 1
            score += o
            print(letter, o)

    print(score)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # part1()

    print("\nPART 2 RESULT")
    part2()
