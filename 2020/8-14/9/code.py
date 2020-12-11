

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    return int(line.strip())

def check(i, data, pre):
    v = data[i]
    first = i-pre
    last = i
    # check if any two numbers sum
    for j in range(first, last):
        for k in range(first, last):
            if j != k:
                if data[j] + data[k] == v:
                    # print(data[j], data[k], "at", j, k, "equal", v)
                    return True
    return False

###########################
# part1
###########################
def part1(data):
    print(data)
    pre = 25
    for i in range(pre, len(data)):
        # print("checking", data[i], "at", i)
        if not check(i, data, pre):
            print("bruh bro", data[i], "at", i)
            return data[i], i

def runpart1():
    part1(parseInputFile())

def findContiguous(data, lookfor):

    for i in range(0, len(data)-1):
        l = []
        res = data[i] + data[i+1]
        l.append(data[i])
        l.append(data[i+1])
        # print(l)
        if res == lookfor:
            print("DONE", l, min(l) + max(l))
            return True
        j = i+2
        while res < lookfor and j < len(data):
            res += data[j]
            l.append(data[j])
            # print(l)
            if res == lookfor:
                print("DONE", l, min(l) + max(l))
                return True
            j += 1
    return False

###########################
# part2
###########################
def part2(data):
    # print(data)
    lookfor, lookfori = part1(data)
    chunk1 = data[:lookfori]
    chunk2 = data[lookfori+1:]
    print(chunk1, chunk2)
    findContiguous(chunk1, lookfor)
    findContiguous(chunk2, lookfor)

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
