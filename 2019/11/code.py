from lib.intcode import Intcode

import plotly.graph_objects as go

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

def controlRobot(data, startPanelColor=0):
    panels = {(0, 0): startPanelColor}
    loc = (0, 0)
    robotdir = "up"
    robotsteps = 0

    intcode_input = [startPanelColor]
    intcode = Intcode(data, intcode_input, debug=False)

    while intcode.running:
        # check for outputs
        if len(intcode.output) >= 2:
            print("robot outputs:", intcode.output)
            # get output
            paintColor = intcode.output[0]
            newdir = intcode.output[1]

            # paint the current spot
            panels[loc] = paintColor
            print("painted ", loc, " ", paintColor)
            print("panels", panels)

            # move the robot
            print("robot was at:", loc, robotdir)
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
                intcode_input.append(0)  # black by default
            print("robot now at:", loc, robotdir)
            intcode.output = []
        intcode.step()
    return panels

def part1(data):
    print(data)
    panels = controlRobot(data, 0)
    print("panels", panels)
    print(len(panels))

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def printPanels(panels):
    maxx = 0
    maxy = 0
    # find dimensions
    for panel in panels:
        maxx = max(maxx, panel[0])
        maxy = max(maxy, panel[1])
    print("maxx",maxx,"maxy",maxy)
    # make grid
    grid = []
    for y in range(maxy+1):
        row = []
        for x in range(maxx+1):
            row.append(" . ")
        grid.append(row)
    # populate grid cells
    for panel in panels:
        # if white
        if panels[panel] == 1:
            grid[panel[1]][panel[0]] = " # "
    # print
    for row in grid:
        for item in row:
            print(item)

def plotPanels(panels):
    x = []
    y = []
    for panel in panels:
        # if white
        if panels[panel] == 1:
            x.append(panel[0])
            y.append(panel[1])
    fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers'))
    fig.show()

def part2(data):
    print(data)
    panels = controlRobot(data, 1)
    plotPanels(panels)

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

    # print("\nPART 2 RESULT")
    # runpart2()
