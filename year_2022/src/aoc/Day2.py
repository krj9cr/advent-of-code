
def parseInput(day):
    path = __file__.rstrip(f"Day{day}.py") + f"../../input/day{day}.txt"
    # print("Input file:", path)
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        return lines

def part1():
    lines = parseInput(2)

def part2():
    lines = parseInput(2)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    part1()

    print("\nPART 2 RESULT")
    part2()
