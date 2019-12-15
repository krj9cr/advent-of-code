
class Chemical:
    name = ""
    amount = 0

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __str__(self):
        return str(self.amount) + " " + self.name

class Formula:
    inputs = {}
    output = None

    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output

    def __str__(self):
        res = ""
        for key in self.inputs:
            res += str(self.inputs[key])
            res += ", "
        res = res.strip(", ")
        res += " => "
        res += str(self.output)
        return res

    def multiply(self, m):
        self.output = Chemical(self.output.name, self.output.amount * m)
        for i in self.inputs:
            self.inputs[i] = Chemical(self.inputs[i].name, self.inputs[i].amount * m)


###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseChemical(chem):
    amount, name = chem.strip().split(" ")
    return Chemical(name, int(amount))

def parseLine(line: str):
    left, right = line.strip().split(" => ")
    output = parseChemical(right)
    ins = left.split(", ")
    inputs = {}
    for i in ins:
        chem = parseChemical(i)
        inputs[chem.name] = chem
    return Formula(inputs, output)

def findTotalChemicalInputAmount(chemicalname, usedformulas):
    count = 0
    for formula in usedformulas:
        for i in formula.inputs:
            if i == chemicalname:
                count += formula.inputs[i].amount
    return count

###########################
# part1
###########################
def part1(data):
    # check repeat outputs... because that would be harder
    # outputs = []
    # for formula in data:
    #     if formula.output.name in outputs:
    #         print("RUHROH duplicate",formula.output.name)
    #     outputs.append(formula.output.name)
    # print(outputs)

    # find starting formula with FUEL
    formulas = []
    usedformulas = []
    for formula in data:
        if formula.output.name == "FUEL":
            usedformulas.append(formula)
        else:
            formulas.append(formula)
    [print(formula) for formula in usedformulas]
    print("REST")
    [print(formula) for formula in formulas]


def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def part2(data):
    print(data)

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2("1122")
    # testpart2("1111")

    # print("\nPART 2 RESULT")
    # runpart2()
