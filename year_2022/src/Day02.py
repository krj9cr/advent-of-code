import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip().split(" ") for line in file]
        return lines
'''
X : Rock, Y: Paper, Z Scissors
A        B          C
'''
shape_score = { 'X': 1, 'Y': 2, 'Z': 3}
beats = { 'X': 'C', 'Y': 'A', 'Z': 'B', 'A': 'Y', 'B': 'Z', 'C': 'X'}
same  = {'X': 'A', 'Y': 'B', 'Z': 'C', 'A': 'X', 'B': 'Y', 'C': 'Z'}
elf_wins = { 'A': 'Z', 'B': 'X', 'C': 'Y'}

def part1():
    lines = parseInput(2)
    # print(lines)
    total_score = 0
    for line in lines:
        elf = line[0]
        me = line[1]
        # print("Elf: ", elf, "Me: ", me)
        score = shape_score[me]
        # print("Shapescore:", score)
        if beats[me] == elf:
            score += 6
        elif same[me] == elf:
            score += 3
        # print("Score:", score)
        total_score += score
    print(total_score)

def part2():
    lines = parseInput(2)
    # print(lines)
    total_score = 0
    for line in lines:
        elf = line[0]
        me = line[1]
        # print("Elf: ", elf, "Me: ", me)
        score = 0
        if me == 'X': # lose
            choose = elf_wins[elf]
        elif me == 'Y': # draw
            choose = same[elf]
            score += 3
        elif me == 'Z': # win
            choose = beats[elf]
            score += 6
        # print("Choose:", choose)
        score += shape_score[choose]
        # print("Shapescore:", shape_score[choose])
        # print("Score:", score)
        # print()
        total_score += score
    print(total_score)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time:", end - start)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time:", end - start)
