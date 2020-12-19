import time
import sys

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        # read lines
        rawlines = [line.strip() for line in file]

        # batch them into lists separated by empty line
        batchedlines = []
        currBatch = []
        for line in rawlines:
            if line != '':
                currBatch.append(line)
            else:
                batchedlines.append(currBatch)
                currBatch = []
        batchedlines.append(currBatch)

        rawrules = batchedlines[0]
        messages = batchedlines[1]

        rules = {}
        for rule in rawrules:
            r = rule.split(": ")
            key = int(r[0])
            val1 = r[1].strip("\"")
            if val1.isalpha():
                rules[key] = val1
            else:
                vals = []
                if "|" not in val1:
                    rules[key] = [int(v) for v in val1.split(" ")]
                else:
                    val2 = val1.split("|")
                    for s in val2:
                        val3 = s.strip().split(" ")
                        vals.append([ int(v) for v in val3])

                    rules[key] = tuple(vals)

        return rules, messages

def parseLine(line: str):
    return line.strip()

def match(rules, message, rule):
    print("evaluating",message,"against",rule)
    # single character rule
    if isinstance(rule, str):
        if message == rule:
            return True
        else:
            return False
    # just a rule idx
    elif isinstance(rule, int):
        return match(rules, message, rules[rule])
    # no OR in rule
    elif isinstance(rule, list):
        m = True
        div = len(message) // len(rule)
        # more chars than we can match
        if div * len(rule) != len(message):
            return False
        for i in range(len(rule)):
            first = i * div
            last = (i+1)*div
            print(first, last, message[first:last])
            m = m and match(rules, message[first:last], rule[i])
        return m
    # OR in rule
    elif isinstance(rule, tuple):
        m = False
        for subrule in rule:
            m = m or match(rules, message, subrule)
        return m
    else:
        print("IDK")
        sys.exit(1)

###########################
# part1
###########################
def part1(data):
    print(data)
    rules, messages = data

    result = 0
    for message in messages:
        if match(rules, message, rules[0]):
            print("Matches", message)
            result += 1
        else:
            print("No match", message)
    print("Result: ", result)

def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################
def part2(data):
    print(data)

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

    # print("\nPART 2 RESULT")
    # runpart2()
