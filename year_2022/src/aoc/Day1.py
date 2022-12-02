
def parseInput(day):
    path = __file__.rstrip(f"Day{day}.py") + f"../../input/day{day}.txt"
    print("Input file:", path)
    with open(path, 'r') as file:
        lines = [line.strip() for line in file]
        groups = []
        currGroup = 0
        for line in lines:
            if line == "":
                groups.append(currGroup)
                currGroup = 0
            else:
                currGroup += int(line)
        return groups

# def part1():
#     True
#
# def part2():
#     lines = parseInput(1)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    lines = parseInput(1)
    print(max(lines))

    print("\nPART 2 RESULT")
    print(sum(sorted(lines,reverse=True)[0:3]))
