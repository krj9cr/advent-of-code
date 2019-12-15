import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from intcode import Intcode

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [ int(num) for num in [ line.split(",") for line in file ][0] ]

def parseInput(lines):
    return [ int(line) for line in str(lines).split(",") ]

def parseLine(line: str):
    return line.strip()

###########################
# part1
###########################
def turnRobot(robotdir, newdir):
    if robotdir == "up":
        if newdir == 0:
            return "left"
        else:
            return "right"
    elif robotdir == "left":
        if newdir == 0:
            return "down"
        else:
            return "up"
    elif robotdir == "right":
        if newdir == 0:
            return "up"
        else:
            return "down"
    elif robotdir == "down":
        if newdir == 0:
            return "right"
        else:
            return "left"
    else:
        print("BAD ROBOT DIR", robotdir)
        exit(1)

def moveRobot(loc, robotdir, newdir):
    newrobotdir = turnRobot(robotdir, newdir)
    if newrobotdir == "up":
        return loc[0], loc[1]+1, newrobotdir
    elif newrobotdir == "left":
        return loc[0]-1, loc[1], newrobotdir
    elif newrobotdir == "right":
        return loc[0]+1, loc[1], newrobotdir
    elif newrobotdir == "down":
        return loc[0], loc[1]-1, newrobotdir
    else:
        print("BAD NEW ROBOT DIR", newrobotdir)
        exit(1)

def part1(data):
    print(data)
    panels = {(0,0):0}
    loc = (0,0)
    robotdir = "up"
    robotsteps = 0

    intcode_input = [0]
    intcode = Intcode(initial_state=data, intcode_input=intcode_input)

    while intcode.running:
        # check for outputs
        if len(intcode.output) >= 2:
            print("robot outputs:",intcode.output)
            # get output
            paintColor = intcode.output[0]
            newdir = intcode.output[1]

            # paint the current spot
            panels[loc] = paintColor
            print("painted ", loc, " ", paintColor)
            print("panels", panels)

            # move the robot
            print("robot was at:",loc, robotdir)
            loc1, loc2, robotdir = moveRobot(loc, robotdir, newdir)
            loc = (loc1, loc2)
            robotsteps += 1
            if robotsteps > 20000:
                print("ROBOT WENT TOO FAR")
                exit(0)

            # set the color for the new spot
            if panels.get(loc) is not None:
                intcode_input.append(panels[loc])
            else:
                intcode_input.append(0) # black by default
            print("robot now at:", loc, robotdir)
            intcode.output = []
        intcode.step()

    print("panels",panels)
    print(len(panels))

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
