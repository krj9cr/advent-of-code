from copy import deepcopy
import numpy as np

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return [[int(num.strip("<x=").strip(" y=").strip("z=").strip(">")),0] for num in line.strip().split(",")]

###########################
# part1
###########################
def getVelocityForAxis(a1, a2):
    if a1[0] > a2[0]:
        a1[1] = a1[1] - 1
        a2[1] = a2[1] + 1
    elif a1[0] < a2[0]:
        a1[1] = a1[1] + 1
        a2[1] = a2[1] - 1
    return a1, a2

def applyGravity(moons):
    # for each pair of moons, a b
    for p1 in range(len(moons)):
        for p2 in range(p1 + 1, len(moons)):
            x1,y1,z1 = moons[p1]
            x2,y2,z2 = moons[p2]
            x1, x2 = getVelocityForAxis(x1,x2)
            y1, y2 = getVelocityForAxis(y1,y2)
            z1, z2 = getVelocityForAxis(z1,z2)
            moons[p1] = [x1,y1,z1]
            moons[p2] = [x2,y2,z2]
    return moons

def applyVelocity(moons):
    # for each moon
    for i in range(len(moons)):
        moons[i] = [
            [moons[i][0][0] + moons[i][0][1], moons[i][0][1]],
            [moons[i][1][0] + moons[i][1][1], moons[i][1][1]],
            [moons[i][2][0] + moons[i][2][1],moons[i][2][1]]
        ]
    return moons

def calcPotentialEnergy(moon):
    return abs(moon[0][0]) + abs(moon[1][0]) + abs(moon[2][0])

def calcKineticEnergy(moon):
    return abs(moon[0][1]) + abs(moon[1][1]) + abs(moon[2][1])

def part1(moons):
    print(moons)
    # time steps
    steps = 1000
    # for each step
    for t in range(0,steps):
        #  apply gravity to each moon, to calc velocities
        moons = applyGravity(moons)
        print(moons)
        #  apply velocities to update positions
        moons = applyVelocity(moons)
        print(moons)

    # calculate total energy for the system
    total = 0
    # for each moon
    for moon in moons:
        #   get potential energy
        pot = calcPotentialEnergy(moon)
        #   get kinetic energy
        kin = calcKineticEnergy(moon)
        #   multiply them
        total += pot * kin
    # sum all moon's energies
    print("total energy",total)

# 940 too low

def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

def getPosition(moon):
    return [moon[0][0], moon[1][0], moon[2][0]]

def getPositions(ms):
    moons = deepcopy(ms)
    l = [ getPosition(moon) for moon in moons]
    res = ""
    for moon in l:
        for pos in moon:
            res += str(pos) + " "
    return res

def getCoordPositions(moons, coord):
    res = ""
    for moon in moons:
        res += str(moon[coord][0]) + " " + str(moon[coord][1]) + " "
    return res

###########################
# part2
###########################
def part2(data):

    coordsteps = [0, 0, 0]

    # x = 0, y = 1, z = 2
    for coord in range(0,3):
        moons = deepcopy(data)
        # time steps
        steps = 0
        states = []
        # for each step
        while True:
            # if steps > 10:
            #     break
            # save state
            coordpositions = getCoordPositions(moons, coord)
            if coordpositions in states:
                coordsteps[coord] = steps
                print("coord",coord,"pos",coordpositions, "states",states)
                print(moons)
                break
            else:
                states.append(coordpositions)
            # print("moons:",moons)
            # print("coord",coord,"Coordpos:",coordpositions, )
            #  apply gravity to each moon, to calc velocities
            moons = applyGravity(moons)
            #  apply velocities to update positions
            moons = applyVelocity(moons)
            print("steps",steps, "coord",coord, "statelen",len(states))

            steps += 1
    print("x",coordsteps[0])
    print("y",coordsteps[1])
    print("z",coordsteps[2])
    wow = np.lcm.reduce(coordsteps)
    print("answer?",wow)

# 2,000,000 too low

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

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
