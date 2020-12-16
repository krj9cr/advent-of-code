import time
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
        # print(batchedlines)

        rawRules = batchedlines[0]
        rules = []
        for r in rawRules:
            r2 = r.split(":")
            s = r2[0].strip()
            vals = r2[1].strip().split(" or ")
            intvals = []
            for v in vals:
                intvals.append([ int(s) for s in v.split("-")])
            rules.append(tuple([s, intvals]))


        myTicket = [ int(s) for s in batchedlines[1][1].split(',')]
        rawNearbyTickets = batchedlines[2][1:]
        nearbyTickets = []
        for t in rawNearbyTickets:
            nearbyTickets.append([int(s) for s in t.split(',')])
        return rules, myTicket, nearbyTickets

def parseLine(line: str):
    return line.strip()

def numIsValid(num, rules):
    # print("checking", num)
    valid = False
    for _, nums in rules:
        for pair in nums:
            rulemin = pair[0]
            rulemax = pair[1]
            # print(rulemin, rulemax)
            valid = valid or (rulemin <= num <= rulemax)
    return valid


###########################
# part1
###########################
def part1(data):
    # print(data)
    rules, myTicket, nearbyTickets = data

    invalid = []
    validtickets = []
    for ticket in nearbyTickets:
        # validate each number
        valid = True
        for num in ticket:
            if not numIsValid(num, rules):
                invalid.append(num)
                valid = False
        if valid:
            validtickets.append(ticket)

    # sum the invalid numbers
    # print(invalid)
    print("PART1", sum(invalid))
    return validtickets


def runpart1():
    start = time.perf_counter()
    part1(parseInputFile())
    end = time.perf_counter()
    print(f"Time: {end-start:0.4f}")

###########################
# part2
###########################

def numIsValid2(num, rule):
    # print("checking", num)
    valid = False
    for pair in rule:
        rulemin = pair[0]
        rulemax = pair[1]
        # print(rulemin, rulemax)
        valid = valid or (rulemin <= num <= rulemax)
    return valid


def part2(data):
    print(data)
    rules, myTicket, nearbyTickets = data
    validNearbyTickets = part1(data)
    validNearbyTickets.append(myTicket)
    print(validNearbyTickets)

    possibleFields = {}

    for name, rule in rules:
        for field in range(0, len(validNearbyTickets[0])):
            allSatisfy = True
            for ticket in validNearbyTickets:
                # validate the field number
                num = ticket[field]
                # print("checking",num, "in field",field)
                allSatisfy = allSatisfy and numIsValid2(num, rule)
            if allSatisfy:
                if possibleFields.get(field) is not None:
                    l = possibleFields.get(field)
                    l.append(name)
                    possibleFields[field] = l
                else:
                    possibleFields[field] = [name]
                # print(name, " could be field:", field)
    print(possibleFields)

    # process of elimination?
    finalFields = {}
    nextFields = deepcopy(possibleFields)
    while len(nextFields) > 0:
        possibleFields = deepcopy(nextFields)
        nextFields = {}
        for field in possibleFields:
            if len(possibleFields[field]) == 1:
                finalFields[possibleFields[field][0]] = field
                nextFields.pop(field, None)
                # remove name from other fields
                for otherField in possibleFields:
                    if otherField != field:
                        # if possibleFields[field] in possibleFields[otherField]:
                        l = possibleFields.get(otherField)
                        # print("removing",possibleFields[field], "From",l )
                        try:
                            l.remove(possibleFields[field][0])
                        except Exception:
                            pass
                        nextFields[otherField] = l
            else:
                nextFields[field] = possibleFields[field]

        # check if name is only in one field
        for name, _ in rules:
            appearances = []
            for field in possibleFields:
                names = possibleFields[field]
                if name in names:
                    appearances.append(field)
            if len(appearances) == 1:
                finalFields[name] = appearances[0]
                nextFields.pop(appearances[0], None)
        # print(nextFields)
    print("final",finalFields)

    # check which fields start with 'departure'
    fieldIndexes = []
    for name in finalFields:
        if 'departure' in name:
            fieldIndexes.append(finalFields[name])
    print(fieldIndexes)

    result = 1
    for idx in fieldIndexes:
        result *= myTicket[idx]
    print("RESULT",result)


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
