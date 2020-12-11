from copy import deepcopy

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    s = line.strip().split(" ")
    return s[0], int(s[1])

def detectloop(data, cmdidx):
    acc = 0
    i = 0
    iter = 0
    m = 100000
    seen = set()
    while i not in seen:
        oldi = i
        seen.add(i)
        cmd, v = data[i]
        if cmdidx == i:
            if cmd == "jmp":
                cmd = "nop"
            elif cmd == "nop":
                cmd = "jmp"
        if cmd == "acc":
            acc += v
            i += 1
        elif cmd == "jmp":
            i += v
            i %= len(data)
        else:
            i += 1
        iter += 1
        # print("i", oldi, "acc", acc, "newi", i)
    if i == len(seen):
        print("ACC:",acc)
        return False
    else:
        print("ISLOOP:",acc)
        return True

###########################
# part1
###########################
def part1(data):
    # print(data)
    acc = 0
    i = 0
    seen = set()
    while i < len(data):
        oldi = i
        if i in seen:
            print("ACC:", acc, "; ended on", i)
            return False
        seen.add(i)
        cmd = data[i]
        if cmd[0] == "acc":
            acc += cmd[1]
            i += 1
        elif cmd[0] == "jmp":
            i += cmd[1]
            i %= len(data)
        else:
            i += 1
        # print("i", oldi, "acc", acc)
    print("ACC:", acc, "; ended on", i)
    return True


def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)

    for i in range(len(data)):
        cmd, v = data[i]
        if cmd == "jmp" or cmd == "nop":
            print("Trying line", i)
            newdata = parseInputFile()
            if cmd == "nop":
                newdata[i] = ("jmp", v)
            elif cmd == "jmp":
                newdata[i] = ("nop", v)
            if part1(newdata):
                return



def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
