
def parseInput(day):
    path = __file__.rstrip(f"Day{day}.py") + f"../input/day{day}.txt"
    # print("Input file:", path)
    with open(path, 'r') as file:
        lines = [line.strip().split(" ") for line in file]
        return lines

shape_score = { 'X': 1, 'Y': 2, 'Z': 3}
beats = { 'X': 'C', 'Y': 'A', 'Z': 'B' }
same  = {'X': 'A', 'Y': 'B', 'Z': 'C'}
'''
X : Rock, Y: Paper, Z Scissors
A        B          C
'''

elf_is_beaten_by = { 'A': 'Y', 'B': 'Z', 'C': 'X'}
elf_wins = { 'A': 'Z', 'B': 'X', 'C': 'Y'}
elf_same  = {'A': 'X', 'B': 'Y', 'C': 'Z'}

def part1():
    lines = parseInput(2)
    print(lines)
    total = 0
    for line in lines:
        elf = line[0]
        me = line[1]
        print("Elf: ", elf, "Me: ", me)
        score = shape_score[me]
        print("Shapescore:", score)
        if beats[me] == elf:
            score += 6
        elif same[me] == elf:
            score += 3
        print("Score:", score)
        total += score
    print(total)

def part2():
    lines = parseInput(2)
    print(lines)
    total = 0
    for line in lines:
        elf = line[0]
        me = line[1]
        print("Elf: ", elf, "Me: ", me)
        score = 0
        if me == 'X': # lose
            choose = elf_wins[elf]
        elif me == 'Y': # draw
            choose = elf_same[elf]
            score += 3
        elif me == 'Z': # win
            choose = elf_is_beaten_by[elf]
            score += 6
        print("Choose:", choose)
        score += shape_score[choose]
        print("Shapescore:", shape_score[choose])
        print("Score:", score)
        print()
        total += score
    print(total)

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # part1()

    print("\nPART 2 RESULT")
    part2()
