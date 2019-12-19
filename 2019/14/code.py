import math

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



formulas = []
fuelformula = None
onhand = {}
use = {}

def findTotalChemicalInputAmount(chemicalname, usedformulas):
    count = 0
    for formula in usedformulas:
        for i in formula.inputs:
            if i == chemicalname:
                count += formula.inputs[i].amount
    return count

def findFormulaWithInputChemical(chemicalname):
    for formula in formulas:
        for i in formula.inputs:
            if i == chemicalname:
                return formula
    return None

def findFormulaWithOutputChemical(chemicalname):
    for formula in formulas:
        if formula.output.name == chemicalname:
            return formula
    return None

def satisfyFormula(formula, outputAmount):
    # account for what we might have onhand
    if formula.output.name in onhand:
        outputAmount -= onhand[formula.output.name]
    mult = 1
    # check if we need to multiply the amounts
    if formula.output.amount < outputAmount:
        mult = math.ceil(outputAmount / formula.output.amount)
        outputAmount = formula.output.amount * mult
    else:
        outputAmount = formula.output.amount

    print("onhand", onhand)
    print("Making",outputAmount, "of",formula.output.name)
    print("mult",mult)
    # for each input, use what we have, or make it
    for inputName in formula.inputs:
        inputAmount = formula.inputs[inputName].amount * mult
        print("checking input amount",inputAmount,"for",inputName)
        # if ORE, just summon the amount we need
        if inputName == "ORE":
            print("inputname is ORE")
            if inputName in onhand:
                onhand[inputName] += inputAmount
            else:
                onhand[inputName] = inputAmount
            continue
        # check if we have enough on hand or not
        if inputName in onhand and onhand[inputName] >= inputAmount:
            onhand[inputName] -= inputAmount
        else:
            f2 = findFormulaWithOutputChemical(inputName)
            satisfyFormula(f2, inputAmount)
            # use it
            if inputName in onhand and onhand[inputName] >= inputAmount:
                onhand[inputName] -= inputAmount
    print("onhand", onhand)
    # once everything is satisfied, we can make the output
    if formula.output.name in onhand:
        onhand[formula.output.name] += outputAmount
    else:
        onhand[formula.output.name] = outputAmount


###########################
# part1
###########################
def part1(data):
    # find starting formula with FUEL
    for formula in data:
        if formula.output.name == "FUEL":
            fuelformula = formula
        else:
            formulas.append(formula)
    print("REST")
    [print(formula) for formula in formulas]

    satisfyFormula(fuelformula, 1)
    print("ORE",onhand["ORE"])


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
