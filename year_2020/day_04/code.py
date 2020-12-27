import re

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

        # parse each string into a passport dict
        passports = []
        for batch in batchedlines:
            currPassport = {}
            batch = str.join(' ', batch)
            passport = batch.split(' ')
            for pair in passport:
                keyvalue = pair.split(':')
                key = keyvalue[0]
                value = keyvalue[1]
                currPassport[key] = value
            passports.append(currPassport)
        return passports

requiredFields = [ 'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid' ]

###########################
# part1
###########################
def part1(data):
    print(data)
    valid = len(data)
    invalid = 0
    for passport in data:
        for field in requiredFields:
            if passport.get(field) is None:
                invalid += 1
                break
    print(valid - invalid)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)
    valid = len(data)
    invalid = 0
    for passport in data:
        # check that each field is present
        missingFields = False
        for field in requiredFields:
            if passport.get(field) is None:
                missingFields = True
                invalid += 1
                break
        if missingFields:
            continue
        # check byr
        byr = passport['byr']
        if len(byr) != 4 or int(byr) < 1920 or int(byr) > 2002:
            invalid += 1
            continue
        # check iyr
        iyr = passport['iyr']
        if len(iyr) != 4 or int(iyr) < 2010 or int(iyr) > 2020:
            invalid +=1
            continue
        # check eyr
        eyr = passport['eyr']
        if len(eyr) != 4 or int(eyr) < 2020 or int(eyr) > 2030:
            invalid +=1
            continue
        # check hgt
        hgt = passport['hgt']
        if re.fullmatch('[0-9]*cm', hgt):
            h = hgt.replace('cm', '')
            if int(h) < 150 or int(h) > 193:
                invalid += 1
                continue
        elif re.fullmatch('[0-9]*in', hgt):
            h = hgt.replace('in', '')
            if int(h) < 59 or int(h) > 76:
                invalid += 1
                continue
        else:
            invalid += 1
            continue
        # check hcl
        hcl = passport['hcl']
        if not re.fullmatch('#[0-9a-f]{6}', hcl):
            invalid += 1
            continue
        # check ecl
        ecl = passport['ecl']
        if not re.fullmatch('(amb|blu|brn|gry|grn|hzl|oth)', ecl):
            invalid += 1
            continue
        # check pid
        pid = passport['pid']
        if not re.fullmatch('[0-9]{9}', pid):
            invalid += 1
            continue
    print(valid - invalid)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1("1111")
    # testpart1("1234")

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
