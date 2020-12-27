import time

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        biggo = {}
        for line in file:
            root, blah = parseLine(line)
            biggo[root] = blah
        return biggo

def parseLine(line: str):
    s1 =  line.strip().split(" contain ")
    root = s1[0].split(" bags")[0]
    nodes = [ n.replace(" bags", "").replace(" bag", "") for n in s1[1].strip('.').split(', ') ]
    blah = {}
    for n in nodes:
        if n == "no other":
            break
        b = n.split(" ")
        num = int(b[0])
        name = " ".join([ n for n in b[1:] ])

        blah[name] = num
    return root, blah

###########################
# part1
###########################
def findpath(start, d, goal):
    result = 0
    nodes = d.get(start)
    if nodes is not None:
        for n in nodes:
            if n == goal:
                return 1
            else:
                result += findpath(n, d, goal)
    return min(result, 1)

def part1(data):
    # print(data)

    result = 0
    for root in data:
        if root != "shiny gold":
            result += findpath(root, data, "shiny gold")
    print(result)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def lookup(bag, d):
    result = 0
    nexts = d.get(bag)
    if nexts is not None:
        result += 1
        for item in nexts:
            result += nexts[item] * lookup(item, d)
    return result

def part2(data):
    # print(data)

    result = lookup("shiny gold", data)
    print(result-1) # minus one to not count "shiny gold"

def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    print("\nPART 2 RESULT")
    runpart2()
