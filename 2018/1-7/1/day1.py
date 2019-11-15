def part1(path: str):
    with open(path, 'r') as file:
        print(sum([int(line) for line in file]))

def part2(path: str):
    with open(path, 'r') as file:
        # init
        lines = []
        freq = {0: 1}
        total = 0
        for line in file:
            lines.append(int(line.strip()))

        repeat = True
        while repeat:
            for num in lines:
                total += num
                seen = freq.get(total)
                if seen is None:
                    freq[total] = 1
                elif seen == 1:
                    freq[total] += 1
                    repeat = False
                    break
        # print(freq)
        print(total)
