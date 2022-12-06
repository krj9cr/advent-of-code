import time

def parseInput(day):
    dayf = "{:02d}".format(day)
    path = __file__.rstrip(f"Day{dayf}.py") + f"../input/day{dayf}.txt"
    with open(path, 'r') as file:
        lines = [line.strip("\n") for line in file]
        stacks = []
        commands = []
        for line in lines:
            if line.startswith("move"):
                # end of stacks, start of commands
                c = []
                for item in line.split(" "):
                    try:
                        c.append(int(item))
                    except:
                        continue
                commands.append(c)
            # stack
            else:
                # ignore the 2 lines in between input
                if "1" in line or line == "":
                    continue
                line = line.split(" ")
                # print(line)
                row = []
                c = 0
                for item in line:
                    if item == "":
                        c += 1
                    else:
                        row.append(item.strip("[").strip("]"))
                    if c == 4:
                        c = 0
                        row.append('')
                stacks.append(row)
        # print(stacks)
        newstacks = []
        numstacks = 0
        for row in stacks:
            if len(row) > numstacks:
                numstacks = len(row)
        # print("Num stacks:", numstacks)
        for i in range(numstacks):
            newstack = []
            # print(i)
            for row in stacks:
                # print("row:", row)
                try:
                    item = row[i]
                    if item == "":
                        continue
                    newstack.append(item)
                    # print("appending:", row[i])
                except:
                    continue
            newstacks.append(list(reversed(newstack)))

        return newstacks, commands


def part1():
    stacks, commands = parseInput(5)
    # print(stacks, commands)
    for command in commands:
        move_num = command[0]
        move_from = command[1]
        move_to = command[2]
        move_from_stack = stacks[move_from-1]
        move_to_stack = stacks[move_to-1]
        for i in range(move_num):
            item = move_from_stack.pop()
            # print("popping", item)
            move_to_stack.append(item)
        # print(stacks)
    for stack in stacks:
        print(stack[-1], end="")
    print()

def part2():
    stacks, commands = parseInput(5)
    print(stacks, commands)
    for command in commands:
        move_num = command[0]
        move_from = command[1]
        move_to = command[2]
        move_from_stack = stacks[move_from-1]
        move_to_stack = stacks[move_to-1]
        print("move num:", move_num)
        size = len(move_from_stack)
        moving = move_from_stack[size-move_num:size]
        move_from_stack = move_from_stack[:-move_num]
        print("moving", moving)
        # print("prev stack", move_from_stack)
        stacks[move_from-1] = move_from_stack
        for item in moving:
            move_to_stack.append(item)
        print(stacks)
    for stack in stacks:
        print(stack[-1], end="")
    print()

if __name__ == "__main__":
    # print("\nPART 1 RESULT")
    # start = time.perf_counter()
    # part1()
    # end = time.perf_counter()
    # print("Time:", end - start)

    print("\nPART 2 RESULT")
    start = time.perf_counter()
    part2()
    end = time.perf_counter()
    print("Time:", end - start)
