import time
import sys
from copy import deepcopy

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
    # print("evaluating",message,"against",rule)
    if len(message) == 0:
        return True, ""
    # single character rule
    if isinstance(rule, str):
        if len(message) > 0:
            return message[0] == rule, message[1:]
        else:
            return False, ""
    # just a rule idx
    elif isinstance(rule, int):
        return match(rules, message, rules[rule])
    # no OR in rule
    elif isinstance(rule, list):
        nextMessage = deepcopy(message)
        for i in range(len(rule)):
            nextRule = rule[i]
            nextRuleMatch, nextMessage = match(rules, nextMessage, nextRule)
            if not nextRuleMatch:
                return False, ""
        return True, nextMessage
    # OR in rule
    elif isinstance(rule, tuple):
        firstRule = rule[0]
        secondRule = rule[1]

        # there's only ever 2 rules, so check both
        firstMatch, firstMessage = match(rules, message, firstRule)
        secondMatch, secondMessage = match(rules, message, secondRule)

        if firstMatch and secondMatch:
            # print(message, "on",firstRule,"now",firstMessage)
            # print(message, "on", secondRule,"now",secondMessage)
            # print("BOTH MATCH???")
            # if we match but both end up empty, that bad
            if firstMessage == "" and secondMessage == "":
                return False, ""
            # return whichever match is not empty to continue with
            if firstMessage == "":
                return secondMatch, secondMessage
            if secondMessage == "":
                return firstMatch, firstMessage
        # return whichever one actually matched
        if firstMatch:
            return True, firstMessage
        if secondMatch:
            return True, secondMessage
        return False, ""
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
        messageMatch, messageRes = match(rules, message, rules[0])
        if len(messageRes) == 0 and messageMatch:
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
    rules, messages = data

    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    rules[8] = tuple([[42], [42, 8]])
    rules[11] = tuple([[42, 31], [42, 11, 31]])

    result = 0
    for message in messages:
        messageMatch, messageRes = match(rules, message, rules[0])
        if len(messageRes) == 0 and messageMatch:
            print("Matches", message)
            result += 1
    print("Result: ", result, "of",len(messages))


def runpart2():
    start = time.perf_counter()
    part2(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# run
###########################
if __name__ == '__main__':

    # print("\nPART 1 RESULT")
    # runpart1()

    print("\nPART 2 RESULT")
    runpart2()
