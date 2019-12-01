import math

###########################
# part1
###########################
def part1(data):
    print(data)
    root = nextSquareRoot(data)
    sq = root * root
    print("square root:", root, "square:", sq)
    ring = findRing(root)
    print("ring:", ring)

    dist_from_corner = int(root/2) + ring
    print("dist_from_corner:", dist_from_corner)

    diff = sq - data
    from_corner = diff

    print("inital diff:", diff)
    print("from corner:", from_corner)
    while diff >= root:
        diff -= root-1
        from_corner -= diff

        print("diff:", diff)
    print("ANSWER:", from_corner)


def nextSquareRoot(n: int):
    # Find the square root of given N
    nroot = math.sqrt(n)
    # Calculate its floor value
    nroot_floor = math.floor(nroot)
    # Then add 1 to it
    sq = nroot_floor + 1
    # make it odd for this problem
    if sq % 2 == 0:
        sq += 1
    return sq

def findRing(sq: int):
    return int(sq/2)

def testpart1(data):
    part1(data)

###########################
# part2
###########################
def part2(data):
    print(data)
    board = [[0, 0, 0],
             [0, 1, 0],
             [0, 0, 0]]



def testpart2(data):
    part2(data)

###########################
# run
###########################
if __name__ == '__main__':
    # print("PART 1 TEST DATA")
    # testpart1(23)
    # testpart1(1024)

    # print("\nPART 1 RESULT")
    # testpart1(289326)

    print("\n\nPART 2 TEST DATA")
    testpart2(747)

    print("\nPART 2 RESULT")
    # testpart2(289326)
