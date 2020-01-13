import sys

###########################
# helpers
###########################
def parseInputFile():
    with open((__file__.rstrip("code.py") + "input.txt"), 'r') as file:
        return [parseLine(line) for line in file][0]

def parseInput(lines):
    return [parseLine(line) for line in lines][0]

def parseLine(line: str):
    return [int(c) for c in line.strip()]

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

###########################
# part1
###########################
def part1(data, w, h):
    flatlayers = chunkIt(data, len(data)/(w*h))
    print("flatlayers",flatlayers)

    # find the one with least # 0's
    min0 = sys.maxsize
    minlayer = None
    for layer in flatlayers:
        count0 = layer.count(0)
        if count0 < min0:
            min0 = count0
            minlayer = layer
    print("minlayer:", minlayer)
    num1 = minlayer.count(1)
    num2 = minlayer.count(2)
    print("ones: ", num1, " twos: ", num2)
    print(num1*num2)

def testpart1(data,w,h):
    lines = parseInput(data)
    part1(lines,w,h)

def runpart1():
    part1(parseInputFile(), 25, 6)

def renderPicture(picture):
    for row in picture:
        for item in row:
            if item == 0:
                print(" ",end='')
            else:
                print(item,end='')
        print()

###########################
# part2
###########################
def part2(data,w,h):
    rows = chunkIt(data, len(data) /w)
    layers = chunkIt(rows, len(rows)/h)
    # print("layers",layers)

    # 0 is black
    # 1 is white
    # 2 is transparent
    # initialize with transparent
    picture = [ [ 2 for _ in range(0,w) ] for _ in range(0,h)]

    for layer in reversed(layers):
        for j in range(0,w):
            for i in range(0,h):
                pixel = layer[i][j]
                # if transparent, do nothing
                if pixel == 2:
                    continue
                picture[i][j] = pixel

    renderPicture(picture)

def testpart2(data, w,h):
    lines = parseInput(data)
    part2(lines, w,h )

def runpart2():
    part2(parseInputFile(),25,6)

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1(["123456789012"],3,2)

    # print("\nPART 1 RESULT")
    # runpart1()

    # print("\n\nPART 2 TEST DATA")
    # testpart2(["0222112222120000"],2,2)
    # testpart2("1111")

    print("\nPART 2 RESULT")
    runpart2()
