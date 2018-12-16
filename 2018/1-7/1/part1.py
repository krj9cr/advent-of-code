def part1(path: str):
    with open(path, 'r') as file:
        print(sum([int(line) for line in file]))
