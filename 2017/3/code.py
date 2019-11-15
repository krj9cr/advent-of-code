import math

###########################
# part1
###########################
def part1(data):
    print(data)
    # print(math.sqrt(data))
    for i in range(537,539):
        if i % 2 == 1:
            print("bottom right corner:", i*i, "circle size:", i)
            sq = (i*i)+1
            circle = i+2
            print("start of next circle:", sq, "next circle size:", circle)
            topright = sq+(circle-2)
            print("top right corner:", topright)
            idx = circle-(data-topright)
            print("index of num:", idx)
            halfway = math.floor(circle/2)
            print((halfway-idx)+(i))

# 685 too high


def testpart1(data):
    part1(data)

###########################
# part2
###########################
def part2(data):
    print(data)

def testpart2(data):
    part2(data)

# def runpart2():
#     part2(parseInputFile())

###########################
# run
###########################
if __name__ == '__main__':
    print("PART 1 TEST DATA")
    # testpart1(6)
    # testpart1(12)
    # testpart1(26)

    print("\nPART 1 RESULT")
    testpart1(289326)

    # print("\n\nPART 2 TEST DATA")
    # testpart2(["5 9 2 8","9 4 7 3","3 8 6 5"])
    #
    # print("\nPART 2 RESULT")
    # runpart2()
