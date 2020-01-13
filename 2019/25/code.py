import random
from lib.intcode import Intcode, asciiToIntcodeInput

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
def part1(data):
    print(data)
    random.seed(1)
    steps = 0

    # I randomly explored rooms to draw a map of the rooms
    # then was able to manually write these instructions to
    # visit all rooms with items we might want to take
    to_pressure_plate = ["east","east","west","west", # hull breach
                         "north","east","north","south","west", # gift wrap
                         "north","north","south","south","south", # hull breach
                         "west","west", # hallway
                         "south","east","north","south","west","north", # hallway
                         "north","east","east", # pressure room
                         "inv"]
    ppi = 0
    # manually figured out which items got us the correct weight
    do_not_take = [
        # things that cause you to die if you pick it up
        "photons", "infinite loop", "giant electromagnet", "escape pod", "molten lava",
        # figuring out what weight we need
        "ornament", # is too heavy by itself
        "semiconductor",
        "asterisk",
        "dark matter",
        # "sand",
        # "wreath",
        # "loom",
        # "mutex",
    ]

    intcode_input = [] #asciiToIntcodeInput(movement[0])
    intcoder = Intcode(data, intcode_input)
    while intcoder.running:
        # check output
        if len(intcoder.output) > 0:
            # check output as string
            s = ""
            for o in intcoder.output:
                s += str(chr(o))
            if s[-8:] == "Command?":
                # provide command somehow
                print(s)

                # if we previously took something, other inputs haven't changed,
                if "You take" in s:
                    items = []
                else:
                    # parse output string
                    doors = []
                    items = []

                    doorsi = s.find("Doors here lead:")
                    itemsi = s.find("Items here:")


                    # parse movements
                    if doorsi != -1:
                        doorss = s[doorsi+16:itemsi]
                        ss = doorss.split("- ")
                        doors = ss[1:]
                        doors = [d.split("\n")[0] for d in doors]
                        print("Doors",doors)

                    # parse items
                    if itemsi != -1:
                        itemss = s[itemsi + 11:]
                        ss = itemss.split("- ")
                        items = ss[1:]
                        items = [d.split("\n")[0] for d in items]
                        print("Items",items)


                # somehow decide what to do
                nextInput = ""

                if len(items) > 0 and items[0] not in do_not_take:
                    nextInput = "take " + items[0]
                # go next direction on route
                elif len(doors) > 0:
                    # choose randomly to do initial exploration
                    # random.shuffle(doors)
                    # nextInput = doors[0]
                    nextInput = to_pressure_plate[ppi]
                    ppi += 1
                print("Providing input:",nextInput)
                intcode_input += asciiToIntcodeInput(nextInput)
                intcoder.output = []
        intcoder.step()
        steps += 1

    s = ""
    for o in intcoder.output:
        s += str(chr(o))
    print(s)

def runpart1():
    part1(parseInputFile())

# no part 2! yay

###########################
# run
###########################
if __name__ == '__main__':

    print("\nPART 1 RESULT")
    runpart1()

