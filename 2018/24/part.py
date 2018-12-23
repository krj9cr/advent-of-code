

def parseInput(path: str):
    with open(path, 'r') as file:
        return [parseLine(line) for line in file]


def parseLine(line: str):
    return line.strip()


def part1(path: str):
    lines = parseInput(path)
    print(lines)


def part2(path: str):
    lines = parseInput(path)
    print(lines)
