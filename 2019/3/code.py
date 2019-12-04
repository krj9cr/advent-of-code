import sys

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file]

def parseInput(lines):
    return [parseLine(line) for line in lines]

def parseLine(line: str):
    return [ parseDirection(dir) for dir in line.strip().split(',')]

def parseDirection(dir: str):
    d = dir[0]
    num = int(dir[1:])
    return d, num

def findMaxSize(wires):
    size = 0
    for wire in wires:
        sumr = 0
        sumd = 0
        sumu = 0
        suml = 0
        for dir in wire:
            if dir[0] == "R":
                sumr += dir[1]
            elif dir[0] == "D":
                sumd += dir[1]
            elif dir[0] == "U":
                sumu += dir[1]
            else:
                suml += dir[1]
        size = max(size, sumr, sumd, sumu, suml) * 2
    return size

def drawWire(xcenter, ycenter, wire):
    x = xcenter
    y = ycenter
    spots = []
    for dir in wire:
        if dir[0] == "R":
            newy = y + dir[1]
            for j in range(y,newy+1):
                spots.append((x,j))
            y = newy
        elif dir[0] == "D":
            newx = x + dir[1]
            for i in range(x, newx+1):
                spots.append((i,y))
            x = newx
        elif dir[0] == "U":
            newx = x - dir[1]
            for i in range(newx, x+1):
                spots.append((i,y))
            x = newx
        else:
            newy = y - dir[1]
            for j in range(newy,y+1):
                spots.append((x,j))
            y = newy
    return spots

def manhattan(one, two):
    return abs(one[0] - two[0]) + abs(one[1] - two[1])

###########################
# part1
###########################
def part1(data):
    print(data)
    # get dimensions
    size = findMaxSize(data)
    xcenter = ycenter = int(size / 2)

    # draw wires
    wire1 = drawWire(xcenter, ycenter, data[0])
    wire2 = drawWire(xcenter, ycenter, data[1])

    # find intersections
    intersections = set()
    for spot in wire1:
        if spot in wire2:
            intersections.add(spot)
    intersections.remove((xcenter, ycenter))
    print(intersections)

    # find closest to center
    m = sys.maxsize
    for i in intersections:
        dist = manhattan((xcenter, ycenter), i)
        m = min (dist, m)
    print(m)


def testpart1(data):
    lines = parseInput(data)
    part1(lines)

def runpart1():
    part1(parseInputFile())

###########################
# part2
###########################
def singleWireSteps(intersection, wire, xcenter, ycenter):
    x = xcenter
    y = ycenter
    steps = 0
    for dir in wire:
        if dir[0] == "R":
            if intersection[0] == x and intersection[1] >= y and intersection[1] < y + dir[1]:
                steps += intersection[1] - y
                return steps
            else:
                y += dir[1]
                steps += dir[1]
        elif dir[0] == "D":
            if intersection[1] == y and intersection[0] >= x and intersection[0] < x + dir[1]:
                steps += intersection[0] - x
                return steps
            else:
                x += dir[1]
                steps += dir[1]
        elif dir[0] == "U":
            if intersection[1] == y and intersection[0] >= x - dir[1] and intersection[0] < x:
                steps += x - intersection[0]
                return steps
            else:
                x -= dir[1]
                steps += dir[1]
        else:
            if intersection[0] == x and intersection[1] >= y - dir[1] and intersection[1] < y:
                steps += y - intersection[1]
                return steps
            else:
                y -= dir[1]
                steps += dir[1]
    return sys.maxsize

def stepsToIntersection(intersection, wires, xcenter, ycenter):
    return singleWireSteps(intersection, wires[0], xcenter, ycenter) + singleWireSteps(intersection, wires[1], xcenter, ycenter)

def part2(data):
    print(data)
    # get board dimensions
    size = findMaxSize(data)
    xcenter = ycenter = int(size / 2)

    # draw wires
    wire1 = drawWire(xcenter, ycenter, data[0])
    wire2 = drawWire(xcenter, ycenter, data[1])

    # find intersections
    # intersections = set()
    # for spot in wire1:
    #     if spot in wire2:
    #         intersections.add(spot)
    # intersections.remove((xcenter, ycenter))
    # print("intersections: ", intersections)

    intersections = [(77751, 78120), (76408, 77242), (73879, 74210), (74052, 75511), (77751, 78022), (74901, 75891),
                    (77769, 78202), (75453, 76369), (73540, 74963), (76379, 76597), (73961, 75689), (74817, 75891),
                    (73936, 74592), (72458, 75419), (75286, 75755), (78036, 75151), (74052, 76351), (78195, 75560),
                    (78456, 77712), (79080, 75039), (75453, 75755), (74434, 75447), (73885, 73718), (77853, 75363),
                    (74052, 75714), (76494, 75476), (76379, 76732), (79989, 74029), (74392, 75721), (76878, 78140),
                    (75389, 76369), (76269, 77175), (76408, 77298), (73751, 75519), (74288, 75721), (76398, 77241),
                    (75759, 75551), (76623, 71777), (75286, 75891), (72772, 76099), (77793, 73790), (75297, 75551),
                    (73090, 75367), (76379, 76801), (77929, 73576), (77695, 75363), (78708, 75249), (78946, 75249),
                    (77999, 78202), (72458, 75629), (77961, 75363), (74052, 76109), (77822, 73214), (73778, 75519),
                    (76455, 77579), (76408, 77579), (76455, 77038), (78603, 76145), (77540, 73765), (78195, 75249),
                    (73839, 75339), (77929, 72990), (75217, 76313), (77844, 72339), (76379, 76811), (78603, 75911),
                    (78603, 75582), (78035, 77597), (74673, 76359), (77540, 73106), (75596, 75755), (76269, 77086),
                    (76269, 77161), (73839, 74980), (76331, 77241), (77769, 78054), (73411, 75367), (76494, 75453),
                    (74392, 75528), (77259, 78622), (73961, 75714), (73839, 75367), (74392, 75447), (73287, 75295),
                    (73651, 75519), (73839, 75256), (73936, 74314), (74434, 75721), (77961, 75560), (77507, 78676),
                    (73885, 74314), (79080, 75228), (74112, 75721), (76494, 76002), (77793, 73214), (77870, 75772),
                    (77540, 73576), (75843, 75302), (79010, 75249), (77695, 75361), (79942, 74440), (78193, 75772),
                    (77436, 73214), (77507, 78560), (78456, 77678), (78134, 75751), (77975, 75652), (74244, 75177),
                    (78467, 76534), (77148, 78467), (77258, 77263), (75480, 75246), (77853, 75361), (75230, 75891),
                    (77929, 73157), (78441, 73157), (74244, 75339), (79468, 74440), (74802, 75511), (76455, 77242),
                    (77870, 75652), (76263, 75302), (78483, 75249), (78035, 78001), (74576, 75511), (76878, 78319),
                    (78103, 75151), (77599, 78676), (77929, 73765), (76623, 72406), (74052, 75740), (74052, 75689),
                    (74052, 76201), (74434, 75528), (79080, 74912), (75230, 75755), (73090, 75629), (76987, 72548),
                    (76494, 75926), (75297, 75544), (77929, 73678), (77961, 75361), (76294, 75302), (75781, 75302),
                    (77540, 73678), (77235, 77038), (73090, 76010), (74392, 75181), (74808, 75447), (76494, 75662),
                    (77822, 73790), (77929, 73106), (79289, 74440), (74273, 75339)]

    # find shortest steps
    m = sys.maxsize
    for i in intersections:
        dist = stepsToIntersection(i, data, xcenter, ycenter)
        m = min(m, dist)
    print(m)

    # 8455 too high

def testpart2(data):
    lines = parseInput(data)
    part2(lines)

def runpart2():
    part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    print("PART 1 TEST DATA")
    # testpart1(["R8,U5,L5,D3", "U7,R6,D4,L4"])
    # testpart1(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
    # testpart1(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2(["R8,U5,L5,D3", "U7,R6,D4,L4"])
    # testpart2(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"])
    # testpart2(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"])

    print("\nPART 2 RESULT")
    runpart2()
