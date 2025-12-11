import time, os

def parseInput():
    # Get the day number from the current file
    full_path = __file__
    file_name = os.path.basename(full_path)
    dayf = file_name.strip("Day").strip(".py")

    # Find the input file for this day and read in its lines
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = []
        for line in file:
            line = line.strip()
            for l in line.split(','):
                items = l.split('-')
                lines.append(tuple([int(i) for i in items]))
        return lines

def isInvalid(num):
    s = str(num)
    midpoint = len(s) // 2  # Calculate the midpoint index
    first_half = s[:midpoint] # Slice from start to midpoint
    second_half = s[midpoint:] # Slice from midpoint to end
    if first_half == second_half:
        return True
    return False

def part1():
    lines = parseInput()
    # print(lines)
    total = 0
    for start, end in lines:
        # print(start, end)
        for i in range(start, end + 1):
            # print(i)
            if isInvalid(i):
                # print("INVALID", i)
                total += i
    print("total", total)

def isInvalid2(num):
    s = str(num)
    # Concatenate the string with itself
    doubled_s = s + s
    # Search for the original string within the doubled string, starting from index 1
    # If found before the original string's length, a repeating pattern exists.
    return doubled_s.find(s, 1) < len(s)

def part2():
    lines = parseInput()
    # print(lines)
    total = 0
    for start, end in lines:
        # print(start, end)
        for i in range(start, end + 1):
            # print(i)
            if isInvalid2(i):
                # print("INVALID", i)
                total += i
    print("total", total)

if __name__ == "__main__":
    print("\nPART 1 RESULT")
    start = time.perf_counter()
    part1()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time (ms):", (end - start) * 1000)
