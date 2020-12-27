import time
import random
from copy import deepcopy
from itertools import permutations, product, combinations

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseLine(line: str):
    l1 = line.strip().split(" (")
    ingredients = l1[0].split(" ")
    a1 = l1[1].replace(")", "").replace("contains ", "").split(" ")
    allergens = []
    for a in a1:
        allergens.append(a.strip(","))
    return ingredients, allergens

def checkSatisfy(data, assignments):
    for ingredients, allergens in data:
        for a in allergens:
            if not (assignments[a] in ingredients):
                # print("checking", assignments[a], "in ", ingredients)
                return False
    return True

###########################
# part1
###########################
def part1(data):
    print(data)
    allAllergens = set()
    allIngredients = set()
    for ingredients, allergens in data:
        for i in ingredients:
            allIngredients.add(i)
        for a in allergens:
            allAllergens.add(a)

    allIngredients = list(allIngredients)
    allAllergens = list(allAllergens)
    print(allIngredients)
    print(allAllergens)

    # for each allergen, get the list of all possible ingredients
    possible = {}
    for ingredients, allergens in data:
        for allergen in allergens:
            if possible.get(allergen) is None:
                possible[allergen] = set()
            for ingredient in ingredients:
                possible[allergen].add(ingredient)

    print("possible 1:",possible)

    possible2 = {}
    # eliminate possibilities that are not present everytime the allergen occurs
    for allergen in possible:
        possible2[allergen] = set()
        for ingredient in possible[allergen]:
            # check every recipe
            ye = True
            for ingredients, allergens in data:
                if allergen in allergens:
                    if not ingredient in ingredients:
                        ye = False
            if ye:
                possible2[allergen].add(ingredient)

    print("possible 2:",possible2)

    possible = possible2


    currIndexes = {}
    for allergen in possible:
        currIndexes[allergen] = 0
        possible[allergen] = list(possible[allergen])
    print(possible)

    allLists = []
    for allergen in allAllergens:
        allLists.append(possible[allergen])
    print(allLists)
    combos = product(*allLists)
    print("Starting to check combos")
    # combos = permutations(allIngredients, len(allAllergens))
    # # shortCombos = [ c[0:len(allAllergens)] for c in combos ]
    # # do better than random by generating permutations
    for combo in combos:
        # skip combos where an item appears more than once
        if len(combo) != len(set(combo)):
            # print("skipping", combo)
            continue
        print("checking", combo)
        # do an assignment of allergens to ingredients
        assignments = {}
        for ai in range(len(allAllergens)):
            assignments[allAllergens[ai]] = combo[ai]
        # if all recipes are satisfied
        if checkSatisfy(data, assignments):
            # print ingredients that do not have an allergen
            nons = list(set(allIngredients) - set(assignments.values()))
            print(assignments)
            print(nons)
            break

    # nons = []
    # count the number of times any of those ingredients appear
    count = 0
    for ingredients, allergens in data:
        for non in nons:
            if non in ingredients:
                count += 1
    print("result", count)
    return assignments

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
    assignments = part1(data)

    result = []
    for allergen in sorted(assignments.keys()):
        result.append(assignments[allergen])
    print("RESULT", ",".join(result))


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
